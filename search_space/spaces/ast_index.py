def natural_value_decorate(func):
    def f(self, other):
        if not isinstance(other, IndexOfList):
            other = NaturalValueIndexNode(other)

        return func(self, other)
    return f


class IndexOfList:
    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    def __neg__(self):
        return NegativeIndexNode(self)

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################
    @natural_value_decorate
    def __add__(self, other):
        return AddIndexNode(self, other)

    @natural_value_decorate
    def __radd__(self, other):
        return AddIndexNode(self, other)

    @natural_value_decorate
    def __mul__(self, other):
        return MultIndexNode(self, other)

    @natural_value_decorate
    def __rmul__(self, other):
        return MultIndexNode(self, other)

    @natural_value_decorate
    def __sub__(self, other):
        return SubIndexNode(self, other)

    @natural_value_decorate
    def __rsub__(self, other):
        return SubIndexNode(other, self)

    @natural_value_decorate
    def __div__(self, other):
        return DivIndexNode(self, other)

    @natural_value_decorate
    def __rdiv__(self, other):
        return DivIndexNode(other, self)

    @natural_value_decorate
    def __mod__(self, other):
        return ModIndexNode(self, other)

    @natural_value_decorate
    def __divmod__(self, other):
        return ModIndexNode(other, self)

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    @natural_value_decorate
    def __and__(self, other):
        return AndIndexNode(self, other)

    @natural_value_decorate
    def __rand__(self, other):
        return AndIndexNode(self, other)

    @natural_value_decorate
    def __or__(self, other):
        return OrIndexNode(self, other)

    @natural_value_decorate
    def __ror__(self, other):
        return OrIndexNode(other, self)

    @natural_value_decorate
    def __xor__(self, other):
        return XorIndexNode(self, other)

    @natural_value_decorate
    def __rxor__(self, other):
        return XorIndexNode(other, self)

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    @natural_value_decorate
    def __eq__(self, other):
        return EqualIndexNode(self, other)

    @natural_value_decorate
    def __req__(self, other):
        return EqualIndexNode(self, other)

    @natural_value_decorate
    def __ne__(self, other):
        return NotEqualIndexNode(self, other)

    @natural_value_decorate
    def __rne__(self, other):
        return NotEqualIndexNode(self, other)

    @natural_value_decorate
    def __lt__(self, other):
        return LessIndexNode(self, other)

    @natural_value_decorate
    def __rlt__(self, other):
        return LessIndexNode(other, self)

    @natural_value_decorate
    def __gt__(self, other):
        return GreatIndexNode(self, other)

    @natural_value_decorate
    def __rgt__(self, other):
        return GreatIndexNode(other, self)

    @natural_value_decorate
    def __ge__(self, other):
        return GreatEqualIndexNode(self, other)

    @natural_value_decorate
    def __rge__(self, other):
        return GreatEqualIndexNode(other, self)

    @natural_value_decorate
    def __le__(self, other):
        return LessEqualIndexNode(self, other)

    @natural_value_decorate
    def __rle__(self, other):
        return LessEqualIndexNode(other, self)


class AstIndexNode(IndexOfList):
    @property
    def is_self(self):
        return False


class SelfIndex(AstIndexNode):
    @property
    def is_self(self):
        return False

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################


class UnaryNode(AstIndexNode):
    def __init__(self, value) -> None:
        super().__init__()
        self.item = value


class NegativeIndexNode(UnaryNode):
    pass


class NaturalValueIndexNode(UnaryNode):
    pass

    #################################################################
    #                                                               #
    #                     Binary Operations                          #
    #                                                               #
    #################################################################


class BinaryNode(AstIndexNode):
    def __init__(self, a, b) -> None:
        super().__init__()
        self.a, self.b = a, b

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################


class AddIndexNode(BinaryNode):
    pass


class MultIndexNode(BinaryNode):
    pass


class SubIndexNode(BinaryNode):
    pass


class DivIndexNode(BinaryNode):
    pass


class ModIndexNode(BinaryNode):
    pass

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################


class AndIndexNode(BinaryNode):
    pass


class OrIndexNode(BinaryNode):
    pass


# class XorIndexNode(BinaryNode):
#     pass

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################


class EqualIndexNode(BinaryNode):
    pass


class NotEqualIndexNode(BinaryNode):
    pass


class LessIndexNode(BinaryNode):
    pass


class GreatIndexNode(BinaryNode):
    pass


class GreatEqualIndexNode(BinaryNode):
    pass


class LessEqualIndexNode(BinaryNode):
    pass


UniversalIndexInstance = SelfIndex()
