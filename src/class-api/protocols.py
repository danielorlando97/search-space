from typing import Any, Protocol, TypeVar, Union, List

"""
SearchSpace = Object's set
Sampling = get an object of set
Optimal Sampling = get the best object of set by objective function  
Valid Sampling = get an object of set that it complies with all rules of the describe
"""
T = TypeVar('T')

class Constraint(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

class SearchSpace(Protocol[T]):
    """Is a defined and iterable domain"""

    def __or__(self, c: Constraint) -> 'SearchSpace[T]':
        pass

    def __iter__(self):
        pass

class FiniteSearchSpace(SearchSpace[T], Protocol[T]):
    def __len__(self) -> int:
        pass

class OrdinalSearchSpace(SearchSpace[T], Protocol[T]):
    def __getitem__(self, index: int) -> T:
        pass
