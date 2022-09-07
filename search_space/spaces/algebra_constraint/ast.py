from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence, check_params_type


check_natural_value = check_params_type(
    lambda: UniversalVariableNode, lambda x: NaturalValue(x))


@decorated_all_methods(check_natural_value)
class UniversalVariableNode:
    precedence = 1

    @property
    def is_self(self):
        return False

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################

    def __getattr__(self, name):
        return GetAttr(self, name)

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################

    def __getitem__(self, index):
        return GetItem(self, index)

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    def __neg__(self):
        return NegOp(self)

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

    def __div__(self, other):
        return DivOp(self, other)

    def __rdiv__(self, other):
        return DivOp(other, self)

    def __mod__(self, other):
        return ModOp(self, other)

    def __divmod__(self, other):
        return ModOp(other, self)

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    def __and__(self, other):
        return AndOp(self, other)

    def __rand__(self, other):
        return AndOp(other, self)

    def __or__(self, other):
        return OrOp(self, other)

    def __ror__(self, other):
        return OrOp(other, self)

    def __xor__(self, other):
        return XorOp(self, other)

    def __rxor__(self, other):
        return XorOp(other, self)

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
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
    #                 Binary Operations                             #
    #                                                               #
    #################################################################


class UniversalVariableBinaryOperation(UniversalVariableNode):
    def __init__(self, target, other) -> None:
        super().__init__()
        self.target = target
        self.other = other

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################


class GetAttr(UniversalVariableBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################


class GetItem(UniversalVariableBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################


class AddOp(UniversalVariableBinaryOperation):
    pass


class SubOp(UniversalVariableBinaryOperation):
    pass


class MultiOp(UniversalVariableBinaryOperation):
    pass


class DivOp(UniversalVariableBinaryOperation):
    pass


class ModOp(UniversalVariableBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################


class AndOp(UniversalVariableBinaryOperation):
    pass


class OrOp(UniversalVariableBinaryOperation):
    pass


class XorOp(UniversalVariableBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################


class EqualOp(UniversalVariableBinaryOperation):
    pass


class NotEqualOp(UniversalVariableBinaryOperation):
    pass


class GreatOrEqualOp(UniversalVariableBinaryOperation):
    pass


class GreatOp(UniversalVariableBinaryOperation):
    pass


class LessOrEqualOp(UniversalVariableBinaryOperation):
    pass


class LessOp(UniversalVariableBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Unary Operations                              #
    #                                                               #
    #################################################################


class UniversalVariableUnaryOperation(UniversalVariableNode):
    def __init__(self, target) -> None:
        super().__init__()
        self.target = target


class NegOp(UniversalVariableUnaryOperation):
    pass


class NaturalValue(UniversalVariableUnaryOperation):
    pass

    #################################################################
    #                                                               #
    #                Specials Operations                            #
    #                                                               #
    #################################################################


class SelfNode(UniversalVariableNode):
    @property
    def is_self(self):
        return True


class AstRoot(UniversalVariableNode):
    def __init__(self) -> None:
        super().__init__()
        self.asts = []

    def add_constraint(self, ast):
        self.asts.append(ast)

    def __add__(self, other):
        if other is None:
            return self

        n = AstRoot()
        n.asts = self.asts + other.asts

        return n


class NotEvaluate(UniversalVariableNode):
    pass
