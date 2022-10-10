from search_space.utils.singleton import Singleton
from typing import Type, TypeVar, Generic, Callable, Union
from search_space.sampler import Sampler

T = TypeVar('T')


class DomainProtocol(Generic[T]):

    def get_sample(self, sampler: Sampler) -> T:
        raise NotImplementedError()

    def __copy__(self):
        raise NotImplementedError()


class NumeralDomainProtocol(DomainProtocol):
    def __init__(self, _min, _max) -> None:
        super().__init__()
        self.min = _min
        self.max = _max


class BachedDomainProtocol(DomainProtocol):
    def __init__(self, *domain: list[DomainProtocol]) -> None:
        super().__init__()


class LinealTransformedProtocol(DomainProtocol):
    def __init__(
        self,
        original_domain: NumeralDomainProtocol,
        transformer: Callable,
        inverse: Callable,
        independent_value: Union[int, float] = None
    ) -> None:
        super().__init__()
        self.original_domain = original_domain
        self.transformer = transformer
        self.inverse = inverse
        self.independent_value = independent_value


class DomainNamespace(metaclass=Singleton):
    def __init__(self):
        self.__namespace__ = {}

    def registry(self, protocol):
        def f(cls):
            if not issubclass(cls, protocol):
                raise TypeError("The class don't implement the protocol")

            namespace = DomainNamespace()

            if protocol in namespace.__namespace__:
                raise ReferenceError('This protocol has implement yet')

            namespace.__namespace__[protocol] = cls
            return cls
        return f

    def __getitem__(self, protocol: Type[T]) -> Type[T]:
        namespace = DomainNamespace()

        try:
            return namespace.__namespace__[protocol]
        except KeyError:
            raise TypeError("This protocol hasn't implement yet")


domain_namespace = DomainNamespace()
