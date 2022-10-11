from search_space.errors import UnSupportOpError
from .logic_ops import LogicOpsNode
from .__base__ import check_natural_value
from search_space.utils.ast_tools import decorated_all_methods
from . import __namespace__ as nsp


def expr_node_check(fn):
    def f(*args):
        if not isinstance(args[1], nsp.Type[nsp.ExprNode]):
            raise UnSupportOpError(args[0], args[1], 'cmp')

        return fn(*args)
    f.__name__ = fn.__name__
    return f


@decorated_all_methods(check_natural_value)
@decorated_all_methods(expr_node_check)
class CmpOpsNode(LogicOpsNode):

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


class EqualOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} == ( {type(self.other).__name__} {op} ..."""

    def op(self):
        return lambda x, y: x == y


class NotEqualOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} != ( {type(self.other).__name__} {op} ..."""

    def op(self):
        return lambda x, y: x != y


class GreatOrEqualOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} >= ( {type(self.other).__name__} {op} ..."""

    def inverted_op(self, a, b):
        return LessOrEqualOp(a, b)

    def op(self):
        return lambda x, y: x >= y


class GreatOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} > ( {type(self.other).__name__} {op} ..."""

    def inverted_op(self, a, b):
        return LessOp(a, b)

    def op(self):
        return lambda x, y: x > y


class LessOrEqualOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} <= ( {type(self.other).__name__} {op} ..."""

    def inverted_op(self, a, b):
        return GreatOrEqualOp(a, b)

    def op(self):
        return lambda x, y: x <= y


class LessOp(LogicOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
            {type(self.target).__name__} > ( {type(self.other).__name__} {op} ..."""

    def inverted_op(self, a, b):
        return GreatOp(a, b)

    def op(self):
        return lambda x, y: x < y
