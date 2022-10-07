from search_space.context_manager.sampler_context import SamplerContext
from search_space.utils.ast_tools import decorated_all_methods, check_ast_precedence, check_params_type
from .search_space_protocol import SearchSpaceProtocol

check_natural_value = check_params_type(
    lambda: SpaceOperationNode, lambda x: NaturalValue(x))


@decorated_all_methods(check_ast_precedence)
@decorated_all_methods(check_natural_value)
class SpaceOperationNode:
    precedence = 0

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


class SearchBinaryOperation(SpaceOperationNode):
    def __init__(self, target: SpaceOperationNode, other: SpaceOperationNode) -> None:
        super().__init__()
        self.target = target
        self.other = other

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################


class GetAttr(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a.__dict__[b]

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################


class GetItem(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a[b]

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################


class AddOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a + b


class SubOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a - b


class MultiOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a * b


class DivOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a / b


class ModOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a % b

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################


class AndOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a and b


class OrOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a or b


class XorOp(SearchBinaryOperation):
    pass

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################


class EqualOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a == b


class NotEqualOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a != b


class GreatOrEqualOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a >= b


class GreatOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a > b


class LessOrEqualOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a <= b


class LessOp(SearchBinaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        a = self.target.get_sample(context, local_domain)
        b = self.target.get_sample(context, local_domain)

        return a < b
    #################################################################
    #                                                               #
    #                 Unary Operations                              #
    #                                                               #
    #################################################################


class SearchUnaryOperation(SpaceOperationNode):
    def __init__(self, target) -> None:
        super().__init__()
        self.target = target


class NegOp(SearchUnaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        return - self.target.get_sample(context, local_domain)


class NaturalValue(SearchUnaryOperation):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        return self.target

    #################################################################
    #                                                               #
    #                Specials Operations                            #
    #                                                               #
    #################################################################


class SelfNode(SpaceOperationNode):
    def __init__(self, space: SearchSpaceProtocol) -> None:
        super().__init__()
        self.space = space

    def get_sample(self, context: SamplerContext = None, local_domain=None):
        return self.space.get_sample(context, local_domain)
