from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.spaces.domains.__base__ import Domain
from .bached_domain import BachedDomain
from search_space.sampler import Sampler
from typing import Iterable
from search_space.utils.itertools import is_iterable


class CategoricalDomain(Domain):
    def __init__(self, _list) -> None:
        self.list = _list
        self.maps = []

    def is_invalid(self):
        return len(self.list) == 0

    def __copy__(self):
        return CategoricalDomain(self.list)

    def get_sample(self, sampler: Sampler):
        return sampler.choice(self.list)

    @property
    def limits(self):
        return self.list

    def filter(self, predicate):
        result = []
        for i, item in enumerate(self.list):
            for _map in self.maps:
                item = _map(item)

            if predicate(item):
                result.append(self.list[i])

        self.list = result

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
        if is_iterable(other) and not isinstance(other, str):
            self.filter(lambda x: x in other)
            return self

        self.filter(lambda x: x == other)
        return self

    def __ne__(self, other):
        if is_iterable(other) and not isinstance(other, str):
            self.filter(lambda x: not x in other)
            return self

        self.filter(lambda x: x != other)
        return self

    def __lt__(self, other):
        if is_iterable(other):
            other = min(other)

        self.filter(lambda x: x < other)
        return self

    def __gt__(self, other):
        if is_iterable(other) and not isinstance(other, str):
            other = max(other)
        self.filter(lambda x: x > other)
        return self

    def __ge__(self, other):
        if is_iterable(other) and not isinstance(other, str):
            other = max(other)

        self.filter(lambda x: x >= other)
        return self

    def __le__(self, other):
        if is_iterable(other):
            other = min(other)

        self.filter(lambda x: x <= other)
        return self

    def __or__(self, __o):
        return BachedDomain(self, __o)
