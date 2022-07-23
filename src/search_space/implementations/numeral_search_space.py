from search_space.abstract_def import SearchSpace, SearchSpaceConstraint
from samplers.implementations.normal_distribution_sampler import NaturalNormalDistributeSampler, ContinueNormalDistributeSampler


class NumeralSearchSpace(SearchSpace):
    def __init__(self, min, max, distribute_like) -> None:
        super().__init__((min, max), distribute_like)

    def __ge__(self, other):
        return self.constraint_list.append(GreatEqual(other, self))

    def __le__(self, other):
        return self.constraint_list.append(LessEqual(other, self))


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=ContinueNormalDistributeSampler()) -> None:
        super().__init__(min, max, distribute_like)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, distribute_like=NaturalNormalDistributeSampler()) -> None:
        super().__init__(min, max, distribute_like)


class GreatEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def transform(self, domain):
        a, b = domain
        return (max(a, self._real_value), b)


class LessEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def transform(self, domain):
        a, b = domain
        return (a, min(b, self._real_value))
