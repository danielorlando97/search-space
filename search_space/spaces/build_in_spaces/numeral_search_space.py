from search_space.spaces import SearchSpace, SearchSpaceDomain
from search_space.sampler.distribution_names import UNIFORM
from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.errors import UnSupportOpError, InvalidSampler


class NumeralDomain(SearchSpaceDomain):
    def __init__(self, initial_domain) -> None:
        self.min, self.max = initial_domain
        self.new_min, self.new_max = initial_domain

    @property
    def initial_limits(self):
        return (self.min, self.max)

    @property
    def limits(self):
        return (self.new_min, self.new_max)

    #################################################################
    #                                                               #
    #                  Transformations                              #
    #                                                               #
    #################################################################

    @visitor.on("node")
    def transform(self, node, context):
        pass

    @visitor.when(ast.UniversalVariable)
    def transform(self, node, context: SamplerContext):
        raise UnSupportOpError(self, node, "transform")

    #################################################################
    #                                                               #
    #                  Binary Cmp Transform                         #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def transform(self, node: ast.GreatEqual, context: SamplerContext):
        _ = self.transform(node.father, context)
        limit: float = self.transform(node.other, context)

        a, b = max(self.new_min, limit), max(self.new_max, limit)
        context.push_log(ConstraintInfo(
            "Transform", "GreatEqual", (self.new_min, self.new_max), (a, b)))

        self.new_min, self.new_max = a, b
        return self

    @visitor.when(ast.Great)
    def transform(self, node: ast.Great, context: SamplerContext):
        _ = self.transform(node.father, context)
        limit: float = self.transform(node.other, context)

        a, b = max(self.new_min, limit), max(self.new_max, limit)
        context.push_log(ConstraintInfo(
            "Transform", "Great", (self.new_min, self.new_max), (a, b)))

        self.new_min, self.new_max = a, b
        return self

    @visitor.when(ast.LessEqual)
    def transform(self, node: ast.LessEqual, context: SamplerContext):
        _ = self.transform(node.father, context)
        limit: float = self.transform(node.other, context)

        a, b = min(self.new_min, limit), min(self.new_max, limit)
        context.push_log(ConstraintInfo(
            "Transform", "LessEqual", (self.new_min, self.new_max), (a, b)))

        self.new_min, self.new_max = a, b
        return self

    @visitor.when(ast.Less)
    def transform(self, node: ast.Less, context: SamplerContext):
        _ = self.transform(node.father, context)
        limit: float = self.transform(node.other, context)

        a, b = min(self.new_min, limit), min(self.new_max, limit)
        context.push_log(ConstraintInfo(
            "Transform", "Less", (self.new_min, self.new_max), (a, b)))

        self.new_min, self.new_max = a, b
        return self
    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def transform(self, node: ast.SelfValue, context: SamplerContext):
        return self

    @visitor.when(ast.NaturalValue)
    def transform(self, node: ast.NaturalValue, context: SamplerContext):
        try:
            return node.other.get_sampler(context=context)[0]
        except AttributeError:
            return node.other

    #################################################################
    #                                                               #
    #                  Check Sampler                                #
    #                                                               #
    #################################################################

    @visitor.on("node")
    def check_sampler(self, node, sampler, context):
        pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Transform                         #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def check_sampler(self, node: ast.GreatEqual, sampler, context: SamplerContext):
        _ = self.check_sampler(node.father, sampler, context)
        limit: float = self.check_sampler(node.other, sampler, context)

        if sampler >= limit:
            return self

        raise InvalidSampler(
            f"{self.__class__.__name__}[{self.limits}]: {sampler} isn't greater than or equal to {limit}")

    @visitor.when(ast.Great)
    def check_sampler(self, node: ast.Great, sampler, context: SamplerContext):
        _ = self.check_sampler(node.father, sampler, context)
        limit: float = self.check_sampler(node.other, sampler, context)

        if sampler > limit:
            return self

        raise InvalidSampler(
            f"{self.__class__.__name__}[{self.limits}]: {sampler} isn't greater than {limit}")

    @visitor.when(ast.LessEqual)
    def check_sampler(self, node: ast.LessEqual, sampler, context: SamplerContext):
        _ = self.check_sampler(node.father, sampler, context)
        limit: float = self.check_sampler(node.other, sampler, context)

        if sampler <= limit:
            return self

        raise InvalidSampler(
            f"{self.__class__.__name__}[{self.limits}]: {sampler} isn't less than or equal to {limit}")

    @visitor.when(ast.Less)
    def check_sampler(self, node: ast.Less, sampler, context: SamplerContext):
        _ = self.check_sampler(node.father, sampler, context)
        limit: float = self.check_sampler(node.other, sampler, context)

        if sampler < limit:
            return self

        raise InvalidSampler(
            f"{self.__class__.__name__}[{self.limits}]: {sampler} isn't less than {limit}")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def check_sampler(self, node: ast.SelfValue, sampler, context: SamplerContext):
        return self

    @visitor.when(ast.NaturalValue)
    def check_sampler(self, node: ast.NaturalValue, sampler, context: SamplerContext):
        try:
            return node.other.get_sampler(context=context)[0]
        except AttributeError:
            return node.other


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max, distribute_like, log_name) -> None:
        super().__init__((min, max), distribute_like, log_name)

    def _create_domain(self, domain) -> SearchSpaceDomain:
        return NumeralDomain(domain)


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like, log_name)

    def _get_random_value(self, domain: NumeralDomain, context):
        return self._distribution.get_float(*domain.limits)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like, log_name)

    def _get_random_value(self, domain: NumeralDomain, context):
        return self._distribution.get_int(*domain.limits)


# class LessEqual(SearchSpaceConstraint):
#     @property
#     def is_transformer(self):
#         return True

#     def _func_transform(self, domain):
#         a, b = domain
#         return (a, min(b, self._real_value))


# class Great(GreatEqual):
#     @property
#     def is_condition(self):
#         return True

#     def _func_condition(self, sampler):
#         return self._real_value < sampler


# class Less(LessEqual):
#     @property
#     def is_condition(self):
#         return True

#     def _func_condition(self, sampler):
#         return self._real_value > sampler


# class NotEqual(SearchSpaceConstraint):
#     @property
#     def is_condition(self):
#         return True

#     def _func_condition(self, sampler):
#         return self._real_value != sampler
