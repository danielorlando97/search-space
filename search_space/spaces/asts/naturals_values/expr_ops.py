from .__base__ import check_natural_value
from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence
from .logic_ops import LogicOpsNode


@decorated_all_methods(check_ast_precedence)
@decorated_all_methods(check_natural_value)
class ExprOpsNode(LogicOpsNode):

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

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
        return ModOp(self, other)

    def __rdivmod__(self, other):
        return ModOp(other, self)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

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

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################


class AddOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.a).__name__} + ( {type(self.b).__name__} {op} ...'


class SubOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.a).__name__} + ( {type(self.b).__name__} {op} ...'


class MultiOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.a).__name__} + ( {type(self.b).__name__} {op} ...'


class DivOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.a).__name__} + ( {type(self.b).__name__} {op} ...'


class ModOp(ExprOpsNode):
    def _suggestion(self, op):
        return f'try to change the constraint like \
            {type(self.a).__name__} + ( {type(self.b).__name__} {op} ...'

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################


class EqualOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class NotEqualOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class GreatOrEqualOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class GreatOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class LessOrEqualOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class LessOp(ExprOpsNode):
    def _suggestion(self, op):
        return f"""try to change the constraint like 
                    {type(self.a).__name__} + ( {type(self.b).__name__} {op} ..."""


class IndexSelf(ExprOpsNode):
    def __init__(self, a) -> None:
        super().__init__(a, None)
