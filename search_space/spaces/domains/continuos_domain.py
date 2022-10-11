from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.spaces.domains.categorical_domain import CategoricalDomain
from search_space.spaces.domains.__base__ import NumeralDomain
from .bached_domain import BachedDomain
from search_space.sampler import Sampler


class ContinuosDomain(NumeralDomain):
    def __init__(self, _min, _max) -> None:
        self.min, self.max = _min, _max

    def __copy__(self):
        return ContinuosDomain(self.min, self.max)

    def get_sample(self, sampler: Sampler):
        return sampler.get_float(self.min, self.max)

    @property
    def limits(self):
        return (self.min, self.max)

    #################################################################
    #                                                               #
    #                     Class Operations                          #
    #                                                               #
    #################################################################

    def __getattr__(self, name):
        raise InvalidSpaceConstraint("Numeral value don't has attributes")

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################

    def __getitem__(self, index):
        raise InvalidSpaceConstraint("Numeral value isn't indexed")

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    def __eq__(self, other):
        if type(other) in [list, tuple]:
            return CategoricalDomain([item for item in other if self.min <= item and item <= self.max])

        if other > self.max or other < self.min:
            raise InvalidSpaceDefinition(
                f"{other} isn't intro the [{self.min}, {self.max}]")

        self.max = other
        self.min = other

        return self

    def __ne__(self, other):
        if type(other) in [list, tuple]:

            other = [item for item in other + [self.min, self.max] if self.min <=
                     item and item <= self.max]
            other = list(set(other))
            other.sort()

            if len(other) == 2:
                return self

            return BachedDomain(
                * [ContinuosDomain(other[i-1], other[i]) for i in range(1, len(other))]
            )

        "If other is out of current domain, it will never enter and current domain is right"
        if other > self.max or other < self.min:
            return self

        """If other is equal that one of limit, we can't limit 
           to domain only can check this condition after we sampler"""
        if other == self.max or self.min == other:
            return self

        return BachedDomain(ContinuosDomain(self.min, other), ContinuosDomain(other, self.max))

    def __lt__(self, other):
        if type(other) in [list, tuple]:
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other, self.max)
        return self

    def __gt__(self, other):
        if type(other) in [list, tuple]:
            other = max(other)

        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other, self.min)
        return self

    def __ge__(self, other):
        return self.__gt__(other)

    def __le__(self, other):
        return self.__lt__(other)

    def __or__(self, __o):
        return BachedDomain(self, __o)

    # def __mod__(self, factor):
    #     return ModuleDomain(self, factor)
