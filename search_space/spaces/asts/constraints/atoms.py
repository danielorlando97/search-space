from .expr_ops import ExprOpsNode
from .__base__ import check_natural_value, UniversalVariableNode
from search_space.utils.ast_tools import decorated_all_methods


@decorated_all_methods(check_natural_value)
class AtomsOp(ExprOpsNode):

    def __getattr__(self, name):
        return GetAttr(self, name)

    def __getitem__(self, index):
        return GetItem(self, index)


class GetAttr(AtomsOp):
    pass


class GetItem(AtomsOp):
    pass


class Atoms(AtomsOp):
    def __init__(self, target) -> None:
        super().__init__(target, None)


class NaturalValue(Atoms):
    pass


UniversalVariableNode.NaturalValue = NaturalValue


class SelfNode(Atoms):
    def __init__(self) -> None:
        super().__init__(None)

    @ property
    def is_self(self):
        return True


class NotEvaluate(Atoms):
    def __init__(self) -> None:
        super().__init__(None)
