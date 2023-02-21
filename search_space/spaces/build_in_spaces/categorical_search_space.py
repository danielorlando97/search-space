from search_space.spaces import BasicSearchSpace
from search_space.sampler import BERNOULLI, BOOLEAN_BERNOULLI
from search_space.spaces.build_in_spaces.space_manager import SpacesManager
from search_space.spaces.domains.categorical_domain import CategoricalDomain

__all__ = [
    "BasicCategoricalSearchSpace",
    "BasicBooleanSearchSpace",
]


@SpacesManager.registry(str)
class BasicCategoricalSearchSpace(BasicSearchSpace):
    def __init__(self, *domain, distribute_like=BERNOULLI, path=None) -> None:
        path = 'str_space' if path is None else path

        super().__init__(
            CategoricalDomain(domain),
            distribute_like=distribute_like,
            path=path, tag=str
        )


@SpacesManager.registry(bool)
class BasicBooleanSearchSpace(BasicSearchSpace):
    def __init__(self, *domain, distribute_like=BOOLEAN_BERNOULLI, path=None) -> None:

        domain = [True, False] if len(domain) == 0 else domain
        path = 'boolean_space' if path is None else path

        super().__init__(
            CategoricalDomain(domain),
            distribute_like=distribute_like,
            path=path, tag=bool
        )
