from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
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
        if other > self.max or other < self.min:
            raise InvalidSpaceDefinition(
                f"{other} isn't intro the [{self.min}, {self.max}]")

        self.max = other
        self.min = other

        return self

    def __ne__(self, other):
        "If other is out of current domain, it will never enter and current domain is right"
        if other > self.max or other < self.min:
            return self

        """If other is equal that one of limit, we can't limit 
           to domain only can check this condition after we sampler"""
        if other == self.max or self.min == other:
            return self

        return BachedDomain(NaturalDomain(self.min, other), NaturalDomain(other, self.max))

    def __lt__(self, other):
        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other - 1, self.max)
        return self

    def __gt__(self, other):
        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other + 1, self.min)
        return self

    def __ge__(self, other):
        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other, self.min)
        return self

    def __le__(self, other):
        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other, self.max)
        return self
