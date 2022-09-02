from search_space.spaces import SearchSpace
from search_space.sampler.distribution_names import UNIFORM


class NumeralSearchSpace(SearchSpace):

    def __init__(self, min, max, distribute_like) -> None:
        super().__init__((min, max), distribute_like)


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

    def __sampler__(self, domain, context):
        return self._distribution.get_float(*domain)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like)

    def __sampler__(self, domain, context):
        return self._distribution.get_int(*domain)
