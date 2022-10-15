from .__base__ import NaturalValuesNodeBinaryOperation, check_natural_value
from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence


@decorated_all_methods(check_ast_precedence)
@decorated_all_methods(check_natural_value)
class LogicOpsNode(NaturalValuesNodeBinaryOperation):

    def __and__(self, other):
        return AndOp(self, other)

    def __rand__(self, other):
        return AndOp(other, self)

    def __or__(self, other):
        return OrOp(self, other)

    def __ror__(self, other):
        return OrOp(other, self)

    # def __xor__(self, other):
    #     return XorOp(self, other)

    # def __rxor__(self, other):
    #     return XorOp(other, self)


class AndOp(LogicOpsNode):

    def _suggestion(self, op):
        return f'try to change the constraint like {type(self.a).__name__} & ( {type(self.b).__name__} {op} ...'


class OrOp(LogicOpsNode):

    def _suggestion(self, op):
        return f'try to change the constraint like {type(self.a).__name__} | ( {type(self.b).__name__} {op} ...'
