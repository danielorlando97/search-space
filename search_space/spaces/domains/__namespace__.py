from typing import Protocol, Callable, Union
from search_space.utils.namespace_injection import InjectorMetaclass, New
from search_space.sampler import Sampler


class DomainProtocol:

    def get_sample(self, sampler: Sampler):
        pass

    def __copy__(self):
        pass


class NumeralDomainProtocol(DomainProtocol):
    min: int
    max: int


class NaturalDomain(NumeralDomainProtocol, InjectorMetaclass):
    def __init__(self, _min, _max) -> None:
        self.min = _min
        self.max = _max


class ContinuosDomain(NumeralDomainProtocol, InjectorMetaclass):
    def __init__(self, _min, _max) -> None:
        self.min = _min
        self.max = _max


class BachedDomain(DomainProtocol, InjectorMetaclass):
    def __init__(self, *domain: list[DomainProtocol]) -> None:
        pass


class LogBachedDomain(BachedDomain, InjectorMetaclass):
    def __init__(self, *domain: list[DomainProtocol]) -> None:
        pass


class LinealTransformed(DomainProtocol, InjectorMetaclass):
    def __init__(
        self,
        original_domain: NumeralDomainProtocol,
        transformer: Callable,
        inverse: Callable,
        independent_value: Union[int, float] = None
    ) -> None:
        pass
