from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.spaces.domains.categorical_domain import CategoricalDomain
from search_space.spaces.domains.__base__ import NumeralDomain
from .bached_domain import BachedDomain
from search_space.sampler import Sampler
from . import __namespace__ as nsp
from typing import Iterable
from search_space.utils.itertools import is_iterable


class ContinuosDomain(NumeralDomain, metaclass=nsp.ContinuosDomain):
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
        if is_iterable(other):
            return CategoricalDomain([item for item in other if self.min <= item and item <= self.max])

        if other > self.max or other < self.min:
            raise InvalidSpaceDefinition(
                f"{other} isn't intro the [{self.min}, {self.max}]")

        self.max = other
        self.min = other

        return self

    def __ne__(self, other):
        return self
        # if is_iterable(other):
        #     other = [item for item in other if self.min <=
        #              item and item <= self.max]
        #     other = list(set(other))

        #     if not self.min in other:
        #         other.append(self.min)

        #     if not self.max in other:
        #         other.append(self.max)

        #     other.sort()

        #     if len(other) == 2:
        #         return self

        #     return BachedDomain(
        #         * [ContinuosDomain(other[i-1], other[i]) for i in range(1, len(other))]
        #     )

        # "If other is out of current domain, it will never enter and current domain is right"
        # if other > self.max or other < self.min:
        #     return self

        # """If other is equal that one of limit, we can't limit
        #    to domain only can check this condition after we sampler"""
        # if other == self.max or self.min == other:
        #     return self

        # return BachedDomain(ContinuosDomain(self.min, other), ContinuosDomain(other, self.max))

    def __lt__(self, other):
        if is_iterable(other):
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other, self.max)
        return self

    def __gt__(self, other):
        if is_iterable(other):
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

    def __mod_eq__(self, factor, value):
        return self

    def __mod_neq__(self, factor, value):
        return self

    def __mod_lt__(self, factor, value):
        return self

    def __mod_gt__(self, factor, value):
        return self

    def __mod_ge__(self, factor, value):
        return self

    def __mod_le__(self, factor, value):
        return self
