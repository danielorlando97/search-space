from .logic_ops import LogicOpsNode
from .__base__ import check_natural_value, UniversalVariableBinaryOperation
from search_space.utils.ast_tools import decorated_all_methods


class SegmentationExprNode(LogicOpsNode):
    def __init__(self, target, other, value) -> None:
        super().__init__(target, other)
        self.value = value


@decorated_all_methods(check_natural_value)
class SegmentationAtomNode(UniversalVariableBinaryOperation):
    def __and__(self, other):
        me = self == 0
        return me & other

    def __rand__(self, other):
        me = self == 0
        return other & me

    def __or__(self, other):
        me = self == 0
        return me | other

    def __or__(self, other):
        me = self == 0
        return other | me

    def __add__(self, other):
        return SegmentationAddOp(self, other)

    def __radd__(self, other):
        return SegmentationAddOp(other, self)

    def __mul__(self, other):
        return SegmentationMultiOp(self, other)

    def __rmul__(self, other):
        return SegmentationMultiOp(other, self)

    def __sub__(self, other):
        return SegmentationSubOp(self, other)

    def __rsub__(self, other):
        return SegmentationSubOp(other, self)

    def __truediv__(self, other):
        return SegmentationDivOp(self, other)

    def __rtruediv__(self, other):
        return SegmentationDivOp(other, self)

    def __mod__(self, other):
        return SegmentationModOp(self, other)

    def __divmod__(self, other):
        return SegmentationModOp(other, self)

    def __eq__(self, other):
        return SegmentationEqualOp(self.target, self.other, other)

    def __req__(self, other):
        return SegmentationEqualOp(self.target, self.other, other)

    def __ne__(self, other):
        return SegmentationNotEqualOp(self.target, self.other, other)

    def __rne__(self, other):
        return SegmentationNotEqualOp(self.target, self.other, other)

    def __lt__(self, other):
        return SegmentationLessOp(self.target, self.other, other)

    def __rlt__(self, other):
        return SegmentationGreatOp(self.target, self.other, other)

    def __gt__(self, other):
        return SegmentationGreatOp(self.target, self.other, other)

    def __rgt__(self, other):
        return SegmentationLessOp(self.target, self.other, other)

    def __ge__(self, other):
        return SegmentationGreatOrEqualOp(self.target, self.other, other)

    def __rge__(self, other):
        return SegmentationLessOrEqualOp(self.target, self.other, other)

    def __le__(self, other):
        return SegmentationLessOrEqualOp(self.target, self.other, other)

    def __rle__(self, other):
        return SegmentationGreatOrEqualOp(self.target, self.other, other)

    #################################################################
    #                                                               #
    #                 SegmentationExprNodes                         #
    #                                                               #
    #################################################################


class SegmentationEqualOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} == ( {type(self.value).__name__} {op} ...'


class SegmentationNotEqualOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} != ( {type(self.value).__name__} {op} ...'


class SegmentationGreatOrEqualOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} >= ( {type(self.value).__name__} {op} ...'


class SegmentationGreatOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} > ( {type(self.value).__name__} {op} ...'


class SegmentationLessOrEqualOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} <= ( {type(self.value).__name__} {op} ...'


class SegmentationLessOp(SegmentationExprNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % {type(self.other).__name__} < ( {type(self.value).__name__} {op} ...'

    #################################################################
    #                                                               #
    #                 SegmentationAtomNodes                         #
    #                                                               #
    #################################################################


class SegmentationAddOp(SegmentationAtomNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} + ( {type(self.other).__name__} {op} ...'


class SegmentationSubOp(SegmentationAtomNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} - ( {type(self.other).__name__} {op} ...'


class SegmentationMultiOp(SegmentationAtomNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} * ( {type(self.other).__name__} {op} ...'


class SegmentationDivOp(SegmentationAtomNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} / ( {type(self.other).__name__} {op} ...'


class SegmentationModOp(SegmentationAtomNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} % ( {type(self.other).__name__} {op} ...'
