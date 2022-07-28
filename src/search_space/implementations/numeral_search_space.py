from search_space.abstract_def import SearchSpace, SearchSpaceConstraint
from samplers.implementations.normal_distribution_sampler import NaturalNormalDistributeSampler, ContinueNormalDistributeSampler


class NumeralSearchSpace(SearchSpace):
    def __init__(self, min, max, distribute_like, log_name) -> None:
        super().__init__((min, max), distribute_like, log_name)

    def _great_equal(self, other):
        self.constraint_list.append(GreatEqual(other, self))
        return self.constraint_list[-1]

    def _less_equal(self, other):
        self.constraint_list.append(LessEqual(other, self))
        return self.constraint_list[-1]

    def _great(self, other):
        self.constraint_list.append(Great(other, self))
        return self.constraint_list[-1]

    def _less(self, other):
        self.constraint_list.append(Less(other, self))
        return self.constraint_list[-1]


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None,
                 distribute_like=ContinueNormalDistributeSampler(u=50000, o2=10)) -> None:
        super().__init__(min, max, distribute_like, log_name)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None,
                 distribute_like=NaturalNormalDistributeSampler(u=50000, o2=10)) -> None:
        super().__init__(min, max, distribute_like, log_name)


class GreatEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def _func_transform(self, domain):
        a, b = domain
        return (max(a, self._real_value), b)


class LessEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def _func_transform(self, domain):
        a, b = domain
        return (a, min(b, self._real_value))


class Great(GreatEqual):
    @property
    def is_condition(self):
        return True

    def _func_condition(self, sampler):
        return self._real_value < sampler


class Less(LessEqual):
    @property
    def is_condition(self):
        return True

    def _func_condition(self, sampler):
        return self._real_value > sampler
