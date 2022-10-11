from .cmp_ops import CmpOpsNode
from .__base__ import check_natural_value
from search_space.utils.ast_tools import decorated_all_methods
from .segmentation_branch import SegmentationModOp
from . import __namespace__ as nsp


@decorated_all_methods(check_natural_value)
class ExprOpsNode(CmpOpsNode, metaclass=nsp.ExprNode):

    def __add__(self, other):
        return AddOp(self, other)

    def __radd__(self, other):
        return AddOp(other, self)

    def __mul__(self, other):
        return MultiOp(self, other)

    def __rmul__(self, other):
        return MultiOp(other, self)

    def __sub__(self, other):
        return SubOp(self, other)

    def __rsub__(self, other):
        return SubOp(other, self)

    def __truediv__(self, other):
        return DivOp(self, other)

    def __rtruediv__(self, other):
        return DivOp(other, self)

    def __mod__(self, other):
        return SegmentationModOp(self, other)

    def __rdivmod__(self, other):
        return SegmentationModOp(other, self)


class AddOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} + ( {type(self.other).__name__} {op} ...'

    def op(self):
        return lambda x, y: x + y


class SubOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} - ( {type(self.other).__name__} {op} ...'

    def op(self):
        return lambda x, y: x - y


class MultiOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} * ( {type(self.other).__name__} {op} ...'

    def op(self):
        return lambda x, y: x * y


class DivOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} / ( {type(self.other).__name__} {op} ...'

    def op(self):
        return lambda x, y: x / y
