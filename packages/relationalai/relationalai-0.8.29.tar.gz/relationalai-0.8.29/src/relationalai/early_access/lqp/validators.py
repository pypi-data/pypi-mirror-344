from relationalai.early_access.metamodel import ir
from typing import Union

CompilableType = Union[
    # Subgrouping
    ir.Logical,
    ir.Union,

    # Formulas
    ir.Lookup,
    ir.Exists,
    ir.Construct,

    # Aggregations
    ir.Aggregate,

    # Effects
    ir.Output,
    ir.Update,
]

# Preconditions
def assert_valid_input(model: ir.Model) -> None:
    task = model.root

    assert isinstance(task, ir.Logical), f"expected root to be logical task, got {type(task)}"
    for subtask in task.body:
        _assert_valid_subtask(subtask)

def _assert_valid_subtask(task: ir.Task) -> None:
    # TODO: assert what subtasks should look like
    assert isinstance(task, ir.Logical), f"expected logical task, got {type(task)}"
    _assert_task_compilable(task)

def _assert_task_compilable(task: ir.Task) -> None:
    assert isinstance(task, CompilableType), f"expected task to be compilable, got {type(task)}"
    if isinstance(task, ir.Logical):
        for subtask in task.body:
            _assert_task_compilable(subtask)
