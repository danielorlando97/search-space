from search_space.spaces import SearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.domains.categorical_domain import CategoricalDomain


class CategoricalSearchSpace(SearchSpace):
    def __init__(self, *domain, distribute_like=UNIFORM, visitor_layers=[]) -> None:
        super().__init__(list(domain), distribute_like, visitor_layers=[
            visitors.DomainModifierVisitor()] + visitor_layers)

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)

    def __domain_filter__(self, domain, context):
        c_domain = CategoricalDomain(domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):
        return CategoricalSearchSpace(*self.initial_domain, distribute_like=self.__distribute_like__)


class BooleanSearchSpace(CategoricalSearchSpace):
    def __init__(self, distribute_like=UNIFORM, visitor_layers=[]) -> None:
        super().__init__(False, True, distribute_like=distribute_like,
                         visitor_layers=visitor_layers)

    def __copy__(self):
        return BooleanSearchSpace(distribute_like=self.__distribute_like__)
