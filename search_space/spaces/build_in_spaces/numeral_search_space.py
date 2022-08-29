from search_space.errors import NotEvaluateError
from search_space.spaces import SearchSpace, SearchSpaceDomain
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.spaces import visitors


class NumeralDomain(SearchSpaceDomain):
    def __init__(self, initial_domain, space: SearchSpace) -> None:
        self.min, self.max = initial_domain
        self.new_min, self.new_max = initial_domain
        self.space = space

    @property
    def initial_limits(self):
        return (self.min, self.max)

    @property
    def limits(self):
        return (self.new_min, self.new_max)

    def transform(self, node, context):
        try:
            v = visitors.NumeralRestrictionDomain(
                self.new_min, self.new_max, context, self.space)

            v.visit(node)
            self.new_min, self.new_max = v.min, v.max
        except NotEvaluateError:
            pass
        return self

    def check_sampler(self, node, sampler, context):
        visitors.ValidateSampler(context, self.space).visit(sampler, node)
        return self


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max, distribute_like, log_name) -> None:
        super().__init__((min, max), distribute_like, log_name)

    def _create_domain(self, domain) -> SearchSpaceDomain:
        return NumeralDomain(domain, self)


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
