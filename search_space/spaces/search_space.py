from .ast_constraint import UniversalVariable
from ..context_manager.sampler_context import SamplerInfo, InitSamplerInfo
from search_space.sampler import SamplerFactory, Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import InvalidSampler


class SearchSpaceDomain:
    def limits(self):
        pass

    def initial_limits(self):
        pass

    def transform(self, ast, context):
        pass

    def check_sampler(self, ast, sampler, context):
        pass


class SearchSpace:

    def __init__(self, initial_domain, distribute_like=UNIFORM, log_name=None) -> None:
        self._distribution: Sampler = SamplerFactory().create_sampler(
            distribute_like, search_space=self)
        self.initial_domain = initial_domain
        self.constraint_list = []
        self.scope = log_name if not log_name is None else self.__class__.__name__

    #################################################################
    #                                                               #
    #                     Sampler Generate                          #
    #                                                               #
    #################################################################

    def get_sampler(self, context: SamplerContext = None):
        """
            This method generate a new sampler by SearchSpace's domain and config
            This sample is unique for each instance of ContextManager
            It divide the constraint list in transforms list and conditional list
            The transforms are constraints that modification the SearchSpace's domain like <= (this reduce the domain)
            The conditionals are constraints that only can check before to generate the sampler like %2 == 0
        """
        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        domain: SearchSpaceDomain = self._create_domain(self.initial_domain)
        context.push_log(InitSamplerInfo(self, domain.initial_limits))

        for ast in self.constraint_list:
            domain = domain.transform(ast, context)

        while True:
            sample = self._get_random_value(domain)

            try:
                for ast in self.constraint_list:
                    domain = domain.check_sampler(ast, sample, context)

                context.registry_sampler(self, sample)
                context.push_log(SamplerInfo(
                    self, domain.limits, self._distribution.last_value(domain.limits), sample))

                return sample, context

            except InvalidSampler as err:
                context.push_log(err.text)

    def _get_random_value(self, domain):
        """
            For default, this method generate a new random value intro the domain
            In the inherence, each class can do override it to change the types and form
            to generate new values
            for example: the categorical Search Space override it to get the random index
            and sample the category with that index
        """
        pass

    def _create_domain(self, domain) -> SearchSpaceDomain:
        """
            For default, this method generate a new random value intro the domain
            In the inherence, each class can do override it to change the types and form
            to generate new values
            for example: the categorical Search Space override it to get the random index
            and sample the category with that index
        """
        pass

    # def _check_transform(self, constraint, domain, context: SamplerContext):
    #     """
    #     """
    #     result = constraint.transform(domain, context)
    #     context.push_log(ConstraintInfo(
    #         self, constraint.__class__.__name__, domain, result))
    #     return result

    # def _check_condition(self, constraint, sample, context: SamplerContext):
    #     """
    #     """

    #     result = constraint.check_condition(sample, context)
    #     context.push_log(ConstraintInfo(
    #         self, constraint.__class__.__name__, sample, result))
    #     return result

    def __or__(self, other):
        """
        """
        if isinstance(other, SearchSpace):
            return OpSearchSpace(lambda x, y: x | y, self, other)

        if isinstance(other, UniversalVariable):
            self.constraint_list.append(other)
        else:
            for f in other:
                self.constraint_list.append(f)
        return self

    def __hash__(self) -> int:
        return id(self)

    def is_equal(self, other):
        try:
            return self._distribution == other._distribution
        except AttributeError:
            return False

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################

    def __getattr__(self, name):
        return OpSearchSpace(lambda x: x.__dict__[name], self)

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################

    def __getitem__(self, index):
        return OpSearchSpace(lambda x: x[index], self)

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    def __neg__(self):
        return OpSearchSpace(lambda x: -x, self)

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

    def __add__(self, other):
        return OpSearchSpace(lambda x, y: x+y, self, other)

    def __radd__(self, other):
        return OpSearchSpace(lambda x, y: x+y, self, other)

    def __mul__(self, other):
        return OpSearchSpace(lambda x, y: x*y, self, other)

    def __rmul__(self, other):
        return OpSearchSpace(lambda x, y: x*y, self, other)

    def __sub__(self, other):
        return OpSearchSpace(lambda x, y: x-y, self, other)

    def __rsub__(self, other):
        return OpSearchSpace(lambda x, y: x-y, other, self)

    def __div__(self, other):
        return OpSearchSpace(lambda x, y: x/y, self, other)

    def __rdiv__(self, other):
        return OpSearchSpace(lambda x, y: x/y, other, self)

    def __mod__(self, other):
        return OpSearchSpace(lambda x, y: x % y, self, other)

    def __divmod__(self, other):
        return OpSearchSpace(lambda x, y: x % y, other, self)

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    def __and__(self, other):
        return OpSearchSpace(lambda x, y: x & y, self, other)

    def __rand__(self, other):
        return OpSearchSpace(lambda x, y: x & y, self, other)

    def __ror__(self, other):
        return OpSearchSpace(lambda x, y: x | y, self, other)

    def __xor__(self, other):
        return OpSearchSpace(lambda x, y: x ^ y, self, other)

    def __rxor__(self, other):
        return OpSearchSpace(lambda x, y: x ^ y, self, other)

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    def __eq__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__eq__(self)

        return OpSearchSpace(lambda x, y: x == y, self, other)

    def __req__(self, other):
        return OpSearchSpace(lambda x, y: x == y, self, other)

    def __ne__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__ne__(self)

        return OpSearchSpace(lambda x, y: x != y, self, other)

    def __rne__(self, other):
        return OpSearchSpace(lambda x, y: x != y, self, other)

    def __lt__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__rlt__(self)

        return OpSearchSpace(lambda x, y: x < y, self, other)

    def __rlt__(self, other):
        return OpSearchSpace(lambda x, y: x > y, self, other)

    def __gt__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__rgt__(self)

        return OpSearchSpace(lambda x, y: x > y, self, other)

    def __rgt__(self, other):
        return OpSearchSpace(lambda x, y: x < y, self, other)

    def __ge__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__rge__(self)

        return OpSearchSpace(lambda x, y: x >= y, self, other)

    def __rge__(self, other):
        return OpSearchSpace(lambda x, y: x <= y, self, other)

    def __le__(self, other):
        if isinstance(other, UniversalVariable):
            return other.__rle__(self)

        return OpSearchSpace(lambda x, y: x <= y, self, other)

    def __rle__(self, other):
        return OpSearchSpace(lambda x, y: x >= y, self, other)


class OpSearchSpace(SearchSpace):
    def __init__(self, func, *operators, log_name=None) -> None:
        self.func = func
        self.operators = operators
        super().__init__(None, log_name=log_name)

    def get_sampler(self, context: SamplerContext = None):
        values = []
        context = context if not context is None else SamplerContext()
        for op in self.operators:
            values.append(self.computing_real_value(op, context))

        return self.func(*values), context

    def computing_real_value(self, op, context):
        if isinstance(op, SearchSpace):
            return op.get_sampler(context=context)[0]
        else:
            return op


class Function(OpSearchSpace):
    def __init__(self, *operators, log_name=None) -> None:
        super().__init__(self.__call__, *operators, log_name=log_name)

    def __call__(self, *args, **kwd):
        raise TypeError(
            f"'{self.__class__.__name__}' isn't a callable type")
