from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from .bached_domain import BachedDomain
from search_space.sampler import Sampler


class CategoricalDomain:
    def __init__(self, _list) -> None:
        self.list = _list
        self.maps = []

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
        self.filter(lambda x: x == other)
        return self

    def __ne__(self, other):
        self.filter(lambda x: x != other)
        return self
