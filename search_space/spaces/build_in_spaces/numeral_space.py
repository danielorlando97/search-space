from search_space.sampler.factory import SamplerFactory
from search_space.spaces import SearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.domains.continuos_domain import ContinuosDomain
from search_space.spaces.domains.natural_domain import NaturalDomain
from .space_manager import SpacesManager


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max) -> None:
        super().__init__((min, max))
        self.visitor_layers.append(visitors.DomainModifierVisitor())

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)


@SpacesManager.registry(float)
class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000) -> None:
        min = 0 if min is None else min
        max = 100000 if max is None else max
        super().__init__(min, max)

    def __domain_filter__(self, domain, context):
        c_domain = ContinuosDomain(*domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):

        clone = ContinueSearchSpace(
            self.initial_domain[0], self.initial_domain[1])
        clone.set_sampler(SamplerFactory().create_sampler(
            self._distribution.__distribute_name__, search_space=clone))
        return clone


@SpacesManager.registry(int)
class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000) -> None:
        min = 0 if min is None else min
        max = 100000 if max is None else max
        super().__init__(min, max)

    def __domain_filter__(self, domain, context):
        c_domain = NaturalDomain(*domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):

        clone = NaturalSearchSpace(
            self.initial_domain[0], self.initial_domain[1])
        clone.set_sampler(SamplerFactory().create_sampler(
            self._distribution.__distribute_name__, search_space=clone))
        return clone
