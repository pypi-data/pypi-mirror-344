from relationalai.early_access.metamodel.util import NameCache
from relationalai.early_access.lqp.validators import assert_valid_input
from relationalai.early_access.metamodel import types
from relationalai.early_access.metamodel import ir, builtins as rel_builtins
from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.lqp.hash_utils import lqp_hash
from relationalai.early_access.lqp.primitives import relname_to_lqp_name, lqp_operator

from typing import Tuple, cast

import datetime as dt

class DebuggingCtx:
    """ Extra information only used for debugging. """
    def __init__(self, id_to_orig_name: dict[lqp.RelationId, str]):
       self.id_to_orig_name = id_to_orig_name

class TranslationCtx:
    def __init__(self, model):
        # TODO: comment these fields
        # TODO: should we have a pass to rename variables instead of this?
        self.var_name_cache = NameCache()
        self.id_to_orig_name = {}
        self.output_ids = []
        self.relname_to_sig = {}
        self.entities = []

        for relation in model.relations:
            assert isinstance(relation, ir.Relation)
            name = relation.name
            assert isinstance(name, str)
            types = []
            for field in relation.fields:
                types.append(field.type)
            sig = lqp.RelationSig(name, types)
            self.relname_to_sig[name] = sig

        for typ in model.types:
            # if its also a relation name, add it
            if isinstance(typ, ir.ScalarType):
                name = typ.name
                if name in self.relname_to_sig:
                    assert isinstance(name, str)
                    self.entities.append(name)

    def debug_ctx(self) -> DebuggingCtx:
        return DebuggingCtx(self.id_to_orig_name)

    # TODO: idk if this is actually right
    def is_entity_type(self, typ: ir.ScalarType) -> bool:
        return typ.name in self.entities

""" Main access point. Converts the model IR to an LQP program. """
def to_lqp(model: ir.Model) -> Tuple[lqp.LqpProgram, DebuggingCtx]:
    assert_valid_input(model)
    ctx = TranslationCtx(model)
    program = _translate_to_program(ctx, model)
    debugging_ctx = ctx.debug_ctx()
    return (program, debugging_ctx)

def _translate_to_program(ctx: TranslationCtx, model: ir.Model) -> lqp.LqpProgram:
    decls: list[lqp.Declaration] = []
    outputs: list[Tuple[str, lqp.RelationId]] = []

    # LQP only accepts logical tasks
    # These are asserted at init time
    root = cast(ir.Logical, model.root)

    seen_rids = set()
    for subtask in root.body:
        # TODO: when do we get more than one?
        child_l = cast(ir.Logical, subtask)
        decl = _translate_to_decl(ctx, child_l)
        for d in decl:
            assert isinstance(d, lqp.Declaration)
            assert isinstance(d, lqp.Def), "we dont do loops yet m8"
            decls.append(d)
            rid = d.name
            assert isinstance(rid, lqp.RelationId)
            assert rid not in seen_rids, f"duplicate relation id: {rid}"
            seen_rids.add(rid)

    for output_id in ctx.output_ids:
        assert isinstance(output_id, lqp.RelationId)
        outputs.append(("output", output_id))

    return lqp.LqpProgram(decls, outputs)

def _translate_to_decl(ctx: TranslationCtx, rule: ir.Logical) -> list[lqp.Declaration]:
    outputs = []
    updates = []
    body_tasks = []
    aggregates = []

    for task in rule.body:
        if isinstance(task, ir.Output):
            outputs.append(task)
        elif isinstance(task, ir.Lookup):
            body_tasks.append(task)
        elif isinstance(task, ir.Logical):
            body_tasks.append(task)
        elif isinstance(task, ir.Exists):
            body_tasks.append(task)
        elif isinstance(task, ir.Aggregate):
            aggregates.append(task)
        elif isinstance(task, ir.Update):
            updates.append(task)
        elif isinstance(task, ir.Construct):
            body_tasks.append(task)
        elif isinstance(task, ir.Union):
            body_tasks.append(task)
        else:
            raise NotImplementedError(f"Unknown task type: {type(task)}")

    conjuncts = []
    for task in body_tasks:
        conjunct = _translate_to_formula(ctx, task)
        conjuncts.append(conjunct)
    body = lqp.Conjunction(conjuncts) if len(conjuncts) != 1 else conjuncts[0]
    # TODO: unify all the def/rel-id generation
    if len(aggregates) > 0:
        assert len(outputs) == 0, "cannot have both outputs and aggregates"
        assert len(updates) == 1, "aggregates should derive into another relation"

        update = updates[0]
        assert isinstance(update, ir.Update)
        assert update.effect == ir.Effect.derive, "only derive supported at the moment"

        projected_args = []
        conjs = []
        for aggr in aggregates:
            assert isinstance(aggr, ir.Aggregate)
            reduce, outer_abstr_args = _translate_aggregate(ctx, aggr, body, update)
            # projected_args.extend(outer_abstr_args)
            conjs.append(reduce)

        for arg in update.args:
            assert isinstance(arg, ir.Var)
            projected_args.append(_translate_to_var(ctx, arg))

        abstraction = lqp.Abstraction(
            projected_args,
            lqp.Conjunction(conjs) if len(conjs) > 1 else conjs[0],
        )
        sig = lqp.RelationSig(update.relation.name, [arg.type for arg in projected_args])
        rel_id = sig_to_id(sig)
        ctx.id_to_orig_name[rel_id] = update.relation.name
        return [lqp.Def(rel_id, abstraction, [])]

    assert len(aggregates) == 0, "aggregates should have already been done"

    if len(outputs) > 0:
        assert len(outputs) == 1, "only one output supported at the moment"
        output = outputs[0]
        assert isinstance(output, ir.Output)
        output_vars = []
        for _, v in output.aliases:
            # TODO: we dont yet handle aliases
            assert isinstance(v, ir.Var)
            var = _translate_to_var(ctx, v)
            output_vars.append(var)
        abstraction = lqp.Abstraction(output_vars, body)
        # TODO: is this correct? might need attrs tooo?
        sig = lqp.RelationSig("output", [arg.type for arg in output_vars])
        relation_id = sig_to_id(sig)
        ctx.output_ids.append(relation_id)
        return [lqp.Def(relation_id, abstraction, [])]

    assert len(updates) == 1, "only one update supported at the moment"
    update = updates[0]
    assert isinstance(update, ir.Update)
    effect = update.effect
    assert effect == ir.Effect.derive, "only derive supported at the moment"

    args = []
    new_eqs = []
    for var in update.args:
        if isinstance(var, ir.Var):
            args.append(_translate_value_to_lqp(ctx, var))
            continue
        # TODO: gensym
        var_name = ctx.var_name_cache.get_name(1, "cvar")
        # TODO: wrong
        if isinstance(var, str):
            typ = lqp.PrimitiveType.STRING
        elif isinstance(var, int):
            typ = lqp.PrimitiveType.INT
        else:
            raise NotImplementedError(f"Unknown var type: {type(var)}")
        lqp_var = lqp.Var(var_name, typ)
        const = _translate_value_to_lqp(ctx, var)
        eq = lqp.Primitive("rel_primitive_eq", [lqp_var, const])
        new_eqs.append(eq)
        args.append(lqp_var)
        continue

    body = lqp.Conjunction(new_eqs + [body]) if len(new_eqs) > 0 else body
    abstraction = lqp.Abstraction(args, body)
    # TODO: is this correct? might need attrs tooo?
    expected_sig = lqp.RelationSig(update.relation.name, [arg.type for arg in args])
    rel_id = sig_to_id(expected_sig)
    ctx.id_to_orig_name[rel_id] = update.relation.name
    return [lqp.Def(rel_id, abstraction, [])]

def _translate_aggregate(ctx: TranslationCtx, aggr: ir.Aggregate, body: lqp.Formula, update: ir.Update) -> Tuple[lqp.Reduce, list[lqp.Var]]:
    assert isinstance(aggr, ir.Aggregate)

    # TODO: handle this properly
    aggr_name = aggr.aggregation.name
    assert aggr_name == "sum" or aggr_name == "count", f"only support sum or count for now, not {aggr.aggregation.name}"

    group_bys = []
    for arg in aggr.group:
        assert isinstance(arg, ir.Var)
        group_bys.append(_translate_to_var(ctx, arg))

    projected_args = []
    for arg in aggr.projection:
        assert isinstance(arg, ir.Var)
        projected_args.append(_translate_to_var(ctx, arg))

    # TODO: differentiate between results and more args
    result_args = []

    # TODO: not sure if this si right
    translated_vars = []
    for arg in aggr.args:
        assert isinstance(arg, ir.Var)
        translated_vars.append(_translate_to_var(ctx, arg))

    # TODO: input and output should be checked using the aggr not like this
    # Last one is output arg
    output_var = translated_vars[-1]
    result_args.append(output_var)

    # The rest are input args
    input_args = []
    for arg in translated_vars[:-1]:
        assert isinstance(arg, lqp.Var)
        input_args.append(arg)

    inner_abstr_args = []
    for arg in projected_args:
        assert isinstance(arg, lqp.Var)
        inner_abstr_args.append(arg)
    for arg in input_args:
        assert isinstance(arg, lqp.Var)
        inner_abstr_args.append(arg)
    if aggr_name == "count":
        inner_abstr_args.append(lqp.Constant(1))

    outer_abstr_args = []
    for arg in group_bys:
        assert isinstance(arg, lqp.Var)
        outer_abstr_args.append(arg)
    outer_abstr_args.append(output_var)

    op = lqp_operator(aggr.aggregation)
    inner_abstr = lqp.Abstraction(
        inner_abstr_args,
        body,
    )
    reduce = lqp.Reduce(
        op,
        inner_abstr,
        result_args,
    )
    return reduce, outer_abstr_args

def _translate_to_formula(ctx: TranslationCtx, task: ir.Task) -> lqp.Formula:
    if isinstance(task, ir.Logical):
        conjuncts = []
        for child in task.body:
            conjunct = _translate_to_formula(ctx, child)
            conjuncts.append(conjunct)
        if len(conjuncts) == 1:
            return conjuncts[0]
        return lqp.Conjunction(conjuncts)
    elif isinstance(task, ir.Lookup):
        return _translate_to_atom(ctx, task)
    elif isinstance(task, ir.Exists):
        lqp_vars = []
        for var in task.vars:
            lqp_vars.append(_translate_to_var(ctx, var))
        formula = _translate_to_formula(ctx, task.task)
        return lqp.Exists(lqp_vars, formula)
    elif isinstance(task, ir.Construct):
        assert len(task.values) >= 1, "construct should have at least one value"
        # TODO: what does the first value do
        terms = []
        for arg in task.values[1:]:
            term = _translate_value_to_lqp(ctx, arg)
            terms.append(term)
        terms.append(_translate_to_var(ctx, task.id_var))
        return lqp.Primitive(
            "rel_primitive_hash_tuple_uint128",
            terms,
        )
    elif isinstance(task, ir.Union):
        # TODO: handle hoisted vars if needed
        assert len(task.hoisted) == 0, "hoisted updates not supported yet, because idk what it means"
        disjs = []
        for child in task.tasks:
            disj = _translate_to_formula(ctx, child)
            disjs.append(disj)
        if len(disjs) == 1:
            return disjs[0]
        return lqp.Disjunction(disjs)
    else:
        raise NotImplementedError(f"Unknown task type (formula): {type(task)}")

def _translate_to_var(ctx: TranslationCtx, var: ir.Var) -> lqp.Var:
    name = ctx.var_name_cache.get_name(var.id, var.name)
    t = type_from_var(var)
    return lqp.Var(name, t)

def _translate_value_to_lqp(ctx: TranslationCtx, value: ir.Value) -> lqp.Term:
    if isinstance(value, ir.Var):
        return _translate_to_var(ctx, value)
    elif isinstance(value, ir.Literal):
        return lqp.Constant(value.value)
    elif isinstance(value, str):
        return lqp.Constant(value)
    elif isinstance(value, int):
        return lqp.Constant(value)
    else:
        raise NotImplementedError(f"Unknown value type: {type(value)}")

def _translate_to_atom(ctx: TranslationCtx, task: ir.Lookup) -> lqp.Formula:
    # TODO: want signature not name
    rel_name = task.relation.name
    assert isinstance(rel_name, str)
    terms = []
    sig_types = []
    for arg in task.args:
        if isinstance(arg, lqp.PrimitiveValue):
            term = lqp.Constant(arg)
            terms.append(term)
            t = type_from_constant(arg)
            sig_types.append(t)
            continue
        assert isinstance(arg, ir.Var), f"expected var, got {type(arg)}: {arg}"
        var = _translate_to_var(ctx, arg)
        terms.append(var)
        sig_types.append(var.type)

    # TODO: wrong
    if rel_builtins.is_builtin(task.relation):
        return _translate_builtin_to_primitive(task.relation, terms)

    assert relation_is_defined(ctx, rel_name, sig_types)
    rid = get_relation_id(ctx, rel_name, sig_types)
    return lqp.Atom(rid, terms)

def get_relation_id(ctx: TranslationCtx, name: str, types: list[lqp.PrimitiveType]) -> lqp.RelationId:
    assert name in ctx.relname_to_sig, f"relation {name} not defined"
    sig = ctx.relname_to_sig[name]
    relation_id = sig_to_id(sig)
    ctx.id_to_orig_name[relation_id] = name
    return relation_id

def sig_to_id(sig: lqp.RelationSig) -> lqp.RelationId:
    # TODO: purposely not putting types in yet
    return lqp.RelationId(lqp_hash(sig.name))

def relation_is_defined(ctx: TranslationCtx, name: str, types: list[lqp.PrimitiveType]) -> bool:
    if name not in ctx.relname_to_sig:
        return False
    sig = ctx.relname_to_sig[name]
    if len(sig.types) != len(types):
        return False
    # TODO: also check types?
    return True

def _translate_builtin_to_primitive(relation: ir.Relation, terms: list[lqp.Term]) -> lqp.Primitive:
    lqp_name = relname_to_lqp_name(relation.name)
    return lqp.Primitive(lqp_name, terms)

def type_from_var(arg: ir.Var) -> lqp.PrimitiveType:
    assert isinstance(arg, ir.Var)
    type = arg.type
    if isinstance(type, ir.UnionType):
        # TODO - this is WRONG! we need to fix the typer wrt overloading
        type = type.types.some()

    assert isinstance(type, ir.ScalarType)
    if types.is_builtin(type):
        # TODO: just ocompare to types.py
        if type.name == "Int":
            return lqp.PrimitiveType.INT
        elif type.name == "String":
            return lqp.PrimitiveType.STRING
        elif type.name == "Number":
            # TODO: fix this, this is wrong
            return lqp.PrimitiveType.INT
        else:
            # TODO: fix this, this is wrong
            return lqp.PrimitiveType.UNKNOWN
    elif (types.is_entity_type(type)):
        return lqp.PrimitiveType.UINT_128
    else:
        raise NotImplementedError(f"Unknown type: {type.name}")

def type_from_constant(arg: lqp.PrimitiveValue) -> lqp.PrimitiveType:
    if isinstance(arg, int):
        return lqp.PrimitiveType.INT
    elif isinstance(arg, float):
        return lqp.PrimitiveType.FLOAT
    elif isinstance(arg, str):
        return lqp.PrimitiveType.STRING
    elif isinstance(arg, dt.date):
        return lqp.PrimitiveType.DATE
    else:
        raise NotImplementedError(f"Unknown constant type: {type(arg)}")
