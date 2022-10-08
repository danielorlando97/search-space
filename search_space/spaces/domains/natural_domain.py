from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.spaces.domains.categorical_domain import CategoricalDomain
from search_space.spaces.domains.module_domain import ModuleDomain
from .bached_domain import BachedDomain
from search_space.sampler import Sampler


class NaturalDomain:
    def __init__(self, _min, _max) -> None:
        self.min, self.max = _min, _max

    def __copy__(self):
        return NaturalDomain(self.min, self.max)

    def get_sample(self, sampler: Sampler):
        return sampler.get_int(self.min, self.max)

    @property
    def limits(self):
        return (self.min, self.max)

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

            other = [item for item in other if self.min <=
                     item and item <= self.max]

            other.sort()
            try:
                other = [other[0]] + [other[i] for i in range(1, len(other))
                                      if other[i] - other[i-1] > 1]

                while len(other) > 0 and self.min == other[0]:
                    other.pop(0)
                    self.min += 1

                while len(other) > 0 and self.max == other[-1]:
                    other.pop(-1)
                    self.max -= 1
            except IndexError:
                raise InvalidSpaceDefinition('NaturalDomain is empty')

            other = [self.min - 1] + other + [self.max + 1]
            return BachedDomain(
                * [NaturalDomain(other[i-1] + 1, other[i] - 1) for i in range(1, len(other))]
            )

        "If other is out of current domain, it will never enter and current domain is right"
        if other > self.max or other < self.min:
            return self

        return BachedDomain(NaturalDomain(self.min, other - 1), NaturalDomain(other + 1, self.max))

    def __lt__(self, other):
        if type(other) in [list, tuple]:
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other - 1, self.max)
        return self

    def __gt__(self, other):
        if type(other) in [list, tuple]:
            other = max(other)

        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other + 1, self.min)
        return self

    def __ge__(self, other):
        if type(other) in [list, tuple]:
            other = max(other)

        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other, self.min)
        return self

    def __le__(self, other):
        if type(other) in [list, tuple]:
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other, self.max)
        return self

    def __or__(self, __o):
        return BachedDomain(self, __o)

    def __mod__(self, factor):
        return ModuleDomain(self, factor)
