from typing import List
from search_space.abstract_def import SearchSpaceConstraint, SearchSpace
from .numeral_search_space import NaturalNormalDistributeSampler


class CategoricalSearchSpace(SearchSpace):
    def __init__(self, domain, distribute_like=NaturalNormalDistributeSampler(u=50000, o2=10), log_name=None) -> None:
        super().__init__(domain, distribute_like, log_name)

    def _get_random_value(self, domain):
        return domain[self._distribution.get_random_value((0, len(domain) - 1))]

    def _not_equal(self, other):
        self.constraint_list.append(NotEqual(other, self))
        return self.constraint_list[-1]


class BooleanSearchSpace(CategoricalSearchSpace):
    def __init__(self, distribute_like=NaturalNormalDistributeSampler(u=50000, o2=10), log_name=None) -> None:
        super().__init__([False, True], distribute_like, log_name)


class NotEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def _func_transform(self, domain: List):
        result = domain.copy()
        result.remove(self._real_value)
        return result
