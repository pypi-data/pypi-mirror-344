from __future__ import annotations

from relationalai.early_access.metamodel import ir, factory as f, helpers
from relationalai.early_access.metamodel.compiler import Pass
from relationalai.early_access.metamodel.visitor import Visitor, DeprecatedPass
from relationalai.early_access.metamodel.util import OrderedSet, ordered_set
from typing import Optional, Any, Tuple, Iterable

class QuantifyVars(Pass):
    """
    Introduce existential quantifiers as closely as possible to the affected sub-tasks.
    """

    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        var_info = VarScopeInfo()
        model.root.accept(var_info)
        return QuantifyVarsRewriter(var_info).walk(model)

class VarScopeInfo(Visitor):
    # Keep track of variables that are still in scope for a given node.
    # Variables are introduced into scope in Var nodes and then propagated upwards.
    # The propagation stops when:
    # 1. They are explicitly quantified, or
    # 2. A node that needs to quantify them is identified.
    #    That node will be the top-most node that still has them in scope.
    _vars_in_scope: dict[ir.Node, OrderedSet[ir.Var]]

    # The top-most node that still has a given variable in scope.
    top_most_scope_for_var: dict[ir.Var, ir.Node]

    IGNORED_NODES = (ir.Type,
                    ir.Var, ir.Literal, ir.Relation, ir.Field,
                    ir.Default, ir.Output, ir.Update, ir.Aggregate,
                    ir.Annotation)

    def __init__(self):
        super().__init__()
        self.top_most_scope_for_var = {}
        self._vars_in_scope = {}

    def leave(self, node: ir.Node, parent: Optional[ir.Node]=None):
        if isinstance(node, ir.Lookup):
            self._record(node, helpers.vars(node.args))

        elif isinstance(node, ir.Data):
            self._record(node, helpers.vars(node.vars))

        elif isinstance(node, ir.Construct):
            self._record(node, helpers.vars(node.values))
            self._record(node, [node.id_var])

        elif isinstance(node, ir.Exists) or isinstance(node, ir.ForAll):
            # Exists and ForAll inherit the vars in scope from their sub-task,
            # but then remove the vars they quantify over.
            scope_vars = self._vars_in_scope.get(node.task, None)
            if scope_vars:
                self._forget(scope_vars, node.vars)
                self._record(node, scope_vars)

        elif isinstance(node, ir.Not):
            # Not inherits the vars in scope from its sub-task.
            scope_vars = self._vars_in_scope.get(node.task, None)
            if scope_vars:
                self._record(node, scope_vars)

        elif isinstance(node, (ir.Match, ir.Union)):
            # Match/Union inherits the vars in scope from its sub-tasks.
            scope_vars = ordered_set()
            for task in node.tasks:
                sub_scope_vars = self._vars_in_scope.get(task, None)
                if sub_scope_vars:
                    scope_vars.update(sub_scope_vars)
            # Don't propagate hoisted variables since they don't need to be quantified.
            self._forget(scope_vars, helpers.hoisted_vars(node.hoisted))
            if scope_vars:
                self._record(node, scope_vars)

        elif isinstance(node, ir.Logical):
            self._do_logical(node)

        else:
            assert isinstance(node, self.IGNORED_NODES), f"Unexpected node kind ({node.kind}) -> {node}"

        return node

    def _do_logical(self, node: ir.Logical):
        scope_vars = ordered_set()
        # If a variable is in scope for a logical sub-task, it's also in scope for this node iff:
        # (1) it is also in scope for some other logical sub-task or
        # (2) it is propagated by some other non-logical sub-task.
        var_supported_by: dict[ir.Var, int] = {}
        for task in node.body:
            sub_scope_vars = self._vars_in_scope.get(task, None)

            if isinstance(task, ir.Output):
                # Vars that are output don't need to be quantified.
                self._forget(scope_vars, helpers.output_vars(task.aliases))

            elif isinstance(task, ir.Update):
                # Vars that are in effects don't need to be quantified.
                self._forget(scope_vars, helpers.vars(task.args))

            elif isinstance(task, ir.Aggregate):
                # Variables that are inputs to an aggregate don't need to be quantified.
                for var in helpers.vars(task.args):
                    if helpers.is_aggregate_input(var, task):
                        self._forget_single(scope_vars, var)

                projection_vars = helpers.vars(task.projection)
                group_vars = helpers.vars(task.group)
                # Variables that are in the projections, and not in the group-by, don't need to be quantified.
                for var in projection_vars:
                    if var not in group_vars:
                        self._forget_single(scope_vars, var)
                # Variables that are in the group-by, and not in the projections, can come into scope.
                for var in group_vars:
                    if var not in projection_vars:
                        scope_vars.add(var)

            elif not sub_scope_vars:
                continue

            elif isinstance(task, ir.Logical):
                for var in sub_scope_vars:
                    var_supported_by[var] = var_supported_by.get(var, 0) + 1

            elif not isinstance(task, ir.Not):
                # For all other node kinds (except Not), just propagate the variables in scope.
                # Not nodes stop the propagation of variables coming from their sub-tasks.
                # Variables that need to be quantified higher than the Not node, will come in scope
                # from a sibling of the Not node (thus via a different path).
                scope_vars.update(sub_scope_vars)

        if scope_vars:
            for var, count in var_supported_by.items():
                if count > 1:
                    scope_vars.add(var)
            # Don't propagate hoisted variables since they don't need to be quantified.
            self._forget(scope_vars, helpers.hoisted_vars(node.hoisted))
            self._record(node, scope_vars)

    def _record(self, node: ir.Node, vars: Iterable[ir.Var]):
        if node not in self._vars_in_scope:
            self._vars_in_scope[node] = ordered_set()
        self._vars_in_scope[node].update(vars)
        for var in vars:
            self.top_most_scope_for_var[var] = node

    def _forget_single(self, var_set: OrderedSet[ir.Var], var: ir.Var):
        var_set.remove(var)
        self.top_most_scope_for_var.pop(var, None)

    def _forget(self, var_set: OrderedSet[ir.Var], vars: Iterable[ir.Var]):
        for var in vars:
            self._forget_single(var_set, var)

class QuantifyVarsRewriter(DeprecatedPass):
    """
    Rewrite the model to quantify variables as closely as possible to the affected sub-tasks.
    """

    node_quantifies_vars: dict[ir.Node, OrderedSet[ir.Var]]

    def __init__(self, var_info: VarScopeInfo):
        super().__init__()
        self.node_quantifies_vars = {}
        for var, node in var_info.top_most_scope_for_var.items():
            if node not in self.node_quantifies_vars:
                self.node_quantifies_vars[node] = ordered_set()
            self.node_quantifies_vars[node].add(var)

    def handle_logical(self, node: ir.Logical, parent: ir.Node, ctx:Optional[Any]=None) -> ir.Logical:
        new_body = self.walk_list(node.body, node)

        if node in self.node_quantifies_vars:
            vars = self.node_quantifies_vars[node]
            effect_tasks = []
            inner_tasks = []
            aggregate_tasks = []
            for task in new_body:
                if isinstance(task, ir.Output):
                    effect_tasks.append(task)

                elif isinstance(task, ir.Update):
                    effect_tasks.append(task)
                    vars.difference_update(helpers.vars(task.args))

                elif isinstance(task, ir.Aggregate):
                    # TODO: QB shouldn't generate multiple aggregate tasks, but unit tests written
                    # in IR directly may do so and the flatten pass doesn't split them yet.
                    if len(aggregate_tasks) > 0:
                        print(f"Multiple aggregate tasks found: {aggregate_tasks} and {task}")
                    aggregate_tasks.append(task)

                else:
                    inner_tasks.append(task)

            if vars:
                var_list = list(vars)
                var_list.sort(key=lambda var: var.name)
                body = f.exists(var_list, f.logical(inner_tasks))
                # If the logical is describing an aggregate, confine the existential to the
                # aggregate's body, by wrapping it in another logical.
                if aggregate_tasks  :
                    body = f.logical([body, *aggregate_tasks])
                return f.logical([body, *effect_tasks], node.hoisted)

        return node if self._eq_tasks(node.body, new_body) else f.logical(new_body, node.hoisted)

    def handle_not(self, node: ir.Not, parent: ir.Node, ctx:Optional[Any]=None) -> ir.Not:
        new_task = self.walk(node.task)

        if node in self.node_quantifies_vars:
            vars = self.node_quantifies_vars[node]
            return f.not_(f.exists(list(vars), new_task))

        return node if node.task.id == new_task.id else f.not_(new_task)

    # To avoid unnecessary cloning of vars in the visitor.
    def handle_var(self, node: ir.Var, parent: ir.Node, ctx:Optional[Any]=None) -> ir.Var:
        return node

    def _eq_tasks(self, xs: Tuple[ir.Task, ...], ys: Tuple[ir.Task, ...]) -> bool:
        if len(xs) != len(ys):
            return False
        for x, y in zip(xs, ys):
            if x.id != y.id:
                return False
        return True
