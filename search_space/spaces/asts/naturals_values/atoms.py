from .expr_ops import ExprOpsNode
from .__base__ import check_natural_value, NaturalValuesNode
from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence


@decorated_all_methods(check_ast_precedence)
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


NaturalValuesNode.NaturalValue = NaturalValue


class SpaceSelfNode(Atoms):
    def __init__(self, space) -> None:
        super().__init__(space)

    def __hash__(self) -> int:
        return hash(self.a)
