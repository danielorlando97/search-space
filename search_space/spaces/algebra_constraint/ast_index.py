from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence, check_params_type


check_natural_value = check_params_type(
    lambda: IndexNode, lambda x: NaturalValue(x))


@decorated_all_methods(check_natural_value)
class IndexNode:
    precedence = 0.5

    @property
    def is_index_node(self):
        return True

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


class IndexBinaryOperation(IndexNode):
    def __init__(self, target, other) -> None:
        super().__init__()
        self.a = target
        self.b = other

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################


class GetAttr(IndexBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################


class GetItem(IndexBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################


class AddOp(IndexBinaryOperation):
    pass


class SubOp(IndexBinaryOperation):
    pass


class MultiOp(IndexBinaryOperation):
    pass


class DivOp(IndexBinaryOperation):
    pass


class ModOp(IndexBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################


class AndOp(IndexBinaryOperation):
    pass


class OrOp(IndexBinaryOperation):
    pass


class XorOp(IndexBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################


class EqualOp(IndexBinaryOperation):
    pass


class NotEqualOp(IndexBinaryOperation):
    pass


class GreatOrEqualOp(IndexBinaryOperation):
    pass


class GreatOp(IndexBinaryOperation):
    pass


class LessOrEqualOp(IndexBinaryOperation):
    pass


class LessOp(IndexBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Unary Operations                              #
    #                                                               #
    #################################################################


class IndexUnaryOperation(IndexNode):
    def __init__(self, target) -> None:
        super().__init__()
        self.target = target


class NegOp(IndexUnaryOperation):
    pass


class NaturalValue(IndexUnaryOperation):
    pass

    #################################################################
    #                                                               #
    #                Specials Operations                            #
    #                                                               #
    #################################################################


class SelfNode(IndexNode):
    def __init__(self, shape_index) -> None:
        super().__init__()
        self.shape_index = shape_index

    def change_to_reference(self, space):
        self.space = space
        return self

    @property
    def is_index_node(self):
        return not isinstance(self.space, GetAttr)
