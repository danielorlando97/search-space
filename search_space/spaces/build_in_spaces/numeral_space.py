from search_space.spaces import BasicSearchSpace
from search_space.sampler import NORMAL
from search_space.spaces.domains.continuos_domain import ContinuosDomain
from search_space.spaces.domains.natural_domain import NaturalDomain
from .space_manager import SpacesManager
from search_space.utils.infinity import oo

__all__ = [
    "BasicContinueSearchSpace",
    "BasicNaturalSearchSpace",
]


@SpacesManager.registry(float)
class BasicContinueSearchSpace(BasicSearchSpace):
    def __init__(self, min=-oo, max=oo, distribute_like=NORMAL, path=None) -> None:
        path = 'float_space' if path is None else path
        super().__init__(ContinuosDomain(min, max), distribute_like, path=path)


@SpacesManager.registry(int)
class BasicNaturalSearchSpace(BasicSearchSpace):
    def __init__(self, min=-oo, max=oo, distribute_like=NORMAL, path=None) -> None:
        path = 'int_space' if path is None else path
        super().__init__(NaturalDomain(min, max), distribute_like, path=path)
