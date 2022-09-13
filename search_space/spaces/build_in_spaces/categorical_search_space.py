from search_space.sampler.factory import SamplerFactory
from search_space.spaces import SearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.build_in_spaces.space_manager import SpacesManager
from search_space.spaces.domains.categorical_domain import CategoricalDomain


@SpacesManager.registry(str)
class CategoricalSearchSpace(SearchSpace):
    def __init__(self, *domain) -> None:
        super().__init__(list(domain))
        self.visitor_layers.append(visitors.DomainModifierVisitor())

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)

    def __domain_filter__(self, domain, context):
        c_domain = CategoricalDomain(domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):
        clone = CategoricalSearchSpace(*self.initial_domain)
        clone.set_sampler(SamplerFactory().create_sampler(
            self._distribution.__distribute_name__, search_space=clone))
        return clone


@SpacesManager.registry(bool)
class BooleanSearchSpace(CategoricalSearchSpace):
    def __init__(self) -> None:
        super().__init__(False, True)

    def __copy__(self):
        clone = BooleanSearchSpace()
        clone.set_sampler(SamplerFactory().create_sampler(
            self._distribution.__distribute_name__, search_space=clone))
        return clone
