from search_space.sampler.factory import SamplerFactory
from search_space.spaces import SearchSpace, BasicSearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.domains.continuos_domain import ContinuosDomain
from search_space.spaces.domains.natural_domain import NaturalDomain
from .space_manager import SpacesManager


__all__ = [
    "BasicContinueSearchSpace",
    "ContinueSearchSpace",
    "BasicNaturalSearchSpace",
    "NaturalSearchSpace"
]


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max, distribute_like=UNIFORM) -> None:
        super().__init__((min, max), distribute_like)
        self.visitor_layers.append(visitors.DomainModifierVisitor())

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)


@SpacesManager.registry(float)
class BasicContinueSearchSpace(BasicSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=UNIFORM) -> None:
        super().__init__((min, max), distribute_like)

    def __sampler__(self, domain, context):
        return self._distribution.get_float(domain[0], domain[1])

    def __advance_space__(self, ast):
        _min, _max = self.initial_domain
        advance_space = ContinueSearchSpace(
            _min, _max, distribute_like=self.__distribute_like__)

        advance_space.ast_constraint = ast
        return advance_space


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

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
class BasicNaturalSearchSpace(BasicSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=UNIFORM) -> None:
        super().__init__((min, max), distribute_like)

    def __sampler__(self, domain, context):
        return self._distribution.get_float(domain[0], domain[1])

    def __advance_space__(self, ast):
        _min, _max = self.initial_domain
        advance_space = NaturalSearchSpace(
            _min, _max, distribute_like=self.__distribute_like__)

        advance_space.ast_constraint = ast
        return advance_space


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

    def __domain_filter__(self, domain, context):
        c_domain = NaturalDomain(*domain)
        return super().__domain_filter__(c_domain, context)

    def __copy__(self):

        clone = NaturalSearchSpace(
            self.initial_domain[0], self.initial_domain[1])
        clone.set_sampler(SamplerFactory().create_sampler(
            self._distribution.__distribute_name__, search_space=clone))
        return clone
