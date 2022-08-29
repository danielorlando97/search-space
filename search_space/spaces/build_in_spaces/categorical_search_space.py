from search_space.errors import NotEvaluateError
from search_space.spaces import SearchSpace, SearchSpaceDomain
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.spaces import visitors


class CategoricalDomain(SearchSpaceDomain):
    def __init__(self, domain) -> None:
        super().__init__()
        self.domain = domain
        self.new_domain = domain

    @property
    def initial_limits(self):
        return self.domain,

    @property
    def limits(self):
        return self.new_domain,

    def transform(self, node, context):
        try:
            v = visitors.CategoricalRestrictionDomain(
                self.new_domain, context, self.space)

            v.visit(node)
            self.new_domain = self.domain
        except NotEvaluateError:
            pass
        return self

    def check_sampler(self, node, sampler, context):
        visitors.ValidateSampler(context, self.space).visit(sampler, node)
        return self


class CategoricalSearchSpace(SearchSpace):
    def __init__(self, domain, distribute_like=UNIFORM, log_name=None) -> None:
        super().__init__(domain, distribute_like, log_name)

    def _create_domain(self, domain) -> SearchSpaceDomain:
        return CategoricalDomain(domain)

    def _get_random_value(self, domain, context):
        return self._distribution.choice(domain.limits)


class BooleanSearchSpace(CategoricalSearchSpace):
    def __init__(self, distribute_like=None, log_name=None) -> None:
        super().__init__([False, True], distribute_like, log_name)
