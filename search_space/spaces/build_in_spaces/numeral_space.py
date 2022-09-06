from search_space.spaces import SearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.domains.continuos_domain import ContinuosDomain
from search_space.spaces.domains.natural_domain import NaturalDomain


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max, distribute_like, visitor_layers=[]) -> None:
        super().__init__((min, max), distribute_like,
                         visitor_layers=[visitors.DomainModifierVisitor()] + visitor_layers)

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

    def __domain_filter__(self, domain, context):
        c_domain = ContinuosDomain(*domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):
        return ContinueSearchSpace(self.initial_domain[0], self.initial_domain[1], self.__distribute_like)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

    def __domain_filter__(self, domain, context):
        c_domain = NaturalDomain(*domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):
        return NaturalSearchSpace(self.initial_domain[0], self.initial_domain[1], self.__distribute_like)
