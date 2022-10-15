from search_space.errors import UnSupportOpError
from search_space.utils.ast_tools import check_params_type


class NaturalValuesNode:
    precedence = 0

    def _suggestion(self, op):
        return ''

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################

    def __getattr__(self, name):
        raise UnSupportOpError(self, name, 'getattr',
                               self._suggestion('getattr'))

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################

    def __getitem__(self, index):
        raise UnSupportOpError(self, index, 'getitem',
                               self._suggestion('getitem'))

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    def __neg__(self):
        raise UnSupportOpError(self, None, '-',
                               self._suggestion('-'))

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

    def __add__(self, other):
        raise UnSupportOpError(self, other, '+',
                               self._suggestion('+'))

    def __radd__(self, other):
        raise UnSupportOpError(self, other, '+',
                               self._suggestion('+'))

    def __mul__(self, other):
        raise UnSupportOpError(self, other, '*',
                               self._suggestion('*'))

    def __rmul__(self, other):
        raise UnSupportOpError(self, other, '*',
                               self._suggestion('*'))

    def __sub__(self, other):
        raise UnSupportOpError(self, other, '-',
                               self._suggestion('_'))

    def __rsub__(self, other):
        raise UnSupportOpError(self, other, '-',
                               self._suggestion('-'))

    def __div__(self, other):
        raise UnSupportOpError(self, other, '/',
                               self._suggestion('/'))

    def __rdiv__(self, other):
        raise UnSupportOpError(self, other, '/',
                               self._suggestion('/'))

    def __mod__(self, other):
        raise UnSupportOpError(self, other, '%',
                               self._suggestion('%'))

    def __divmod__(self, other):
        raise UnSupportOpError(self, other, '%',
                               self._suggestion('%'))

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    def __and__(self, other):
        raise UnSupportOpError(self, other, '&',
                               self._suggestion('&'))

    def __rand__(self, other):
        raise UnSupportOpError(self, other, '&',
                               self._suggestion('&'))

    def __or__(self, other):
        raise UnSupportOpError(self, other, '|',
                               self._suggestion('|'))

    def __ror__(self, other):
        raise UnSupportOpError(self, other, '|',
                               self._suggestion('|'))

    # def __xor__(self, other):
    #     return XorOp(self, other)

    # def __rxor__(self, other):
    #     return XorOp(other, self)

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    def __eq__(self, other):
        raise UnSupportOpError(self, other, '==',
                               self._suggestion('=='))

    def __req__(self, other):
        raise UnSupportOpError(self, other, '==',
                               self._suggestion('=='))

    def __ne__(self, other):
        raise UnSupportOpError(self, other, '!=',
                               self._suggestion('!='))

    def __rne__(self, other):
        raise UnSupportOpError(self, other, '!=',
                               self._suggestion('!='))

    def __lt__(self, other):
        raise UnSupportOpError(self, other, '<',
                               self._suggestion('<'))

    def __rlt__(self, other):
        raise UnSupportOpError(self, other, '<',
                               self._suggestion('<'))

    def __gt__(self, other):
        raise UnSupportOpError(self, other, '>',
                               self._suggestion('>'))

    def __rgt__(self, other):
        raise UnSupportOpError(self, other, '>',
                               self._suggestion('>'))

    def __ge__(self, other):
        raise UnSupportOpError(self, other, '>=',
                               self._suggestion('>='))

    def __rge__(self, other):
        raise UnSupportOpError(self, other, '>=',
                               self._suggestion('>='))

    def __le__(self, other):
        raise UnSupportOpError(self, other, '<=',
                               self._suggestion('<='))

    def __rle__(self, other):
        raise UnSupportOpError(self, other, '<=',
                               self._suggestion('<='))


class NaturalValuesNodeBinaryOperation(NaturalValuesNode):
    def __init__(self, a, b) -> None:
        super().__init__()
        self.a = a
        self.b = b


check_natural_value = check_params_type(
    lambda: NaturalValuesNode,
    lambda x: NaturalValuesNode.NaturalValue(x)
)
