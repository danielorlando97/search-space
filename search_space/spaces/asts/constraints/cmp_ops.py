from search_space.errors import UnSupportOpError
from .logic_ops import LogicOpsNode
from .__base__ import check_natural_value
from search_space.utils.ast_tools import decorated_all_methods


def expr_node_check(fn):
    def f(*args):
        if not isinstance(args[1], CmpOpsNode.ExprNode):
            raise UnSupportOpError(CmpOpsNode(None, None), args[1], 'cmp')

        return fn(*args)
    f.__name__ = fn.__name__
    return f


@decorated_all_methods(check_natural_value)
@decorated_all_methods(expr_node_check)
class CmpOpsNode(LogicOpsNode):
    ExprNode = None

    def __eq__(self, other):
        return EqualOp(self, other)

    def __req__(self, other):
        return EqualOp(other, self)

    def __ne__(self, other):
        return NotEqualOp(self, other)

    def __rne__(self, other):
        return NotEqualOp(other, self)

    def __lt__(self, other):
        return LessOp(self, other)

    def __rlt__(self, other):
        return LessOp(other, self)

    def __gt__(self, other):
        return GreatOp(self, other)

    def __rgt__(self, other):
        return GreatOp(other, self)

    def __ge__(self, other):
        return GreatOrEqualOp(self, other)

    def __rge__(self, other):
        return GreatOrEqualOp(other, self)

    def __le__(self, other):
        return LessOrEqualOp(self, other)

    def __rle__(self, other):
        return LessOrEqualOp(other, self)

    @staticmethod
    def setter_expr_class(cls):
        CmpOpsNode.ExprNode = cls
        return cls


class EqualOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} == ( {type(self.other).__name__} {op} ...'


class NotEqualOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} != ( {type(self.other).__name__} {op} ...'


class GreatOrEqualOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} >= ( {type(self.other).__name__} {op} ...'


class GreatOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} > ( {type(self.other).__name__} {op} ...'


class LessOrEqualOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} <= ( {type(self.other).__name__} {op} ...'


class LessOp(CmpOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.target).__name__} < ( {type(self.other).__name__} {op} ...'
