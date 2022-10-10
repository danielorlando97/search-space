from typing import Generic, Protocol, TypeVar
from search_space.sampler import Sampler

T = TypeVar('T')


class DomainProtocol(Generic[T]):
    def get_sample(self, sampler: Sampler) -> T:
        pass

    def __rlt__(self, other):
        return self.__gt__(other)

    def __rgt__(self, other):
        return self.__lt__(other)

    def __rle__(self, other):
        return self.__ge__(other)

    def __rge__(self, other):
        return self.__le__(other)


class NumeralDomainProtocol(DomainProtocol):

    @property
    def min(self):
        pass

    @property
    def max(self):
        pass
