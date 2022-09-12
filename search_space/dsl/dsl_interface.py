from inspect import Parameter
from typing import Generic, Tuple, Type, TypeVar, List, Union
from search_space.spaces.build_in_spaces import NaturalSearchSpace, TensorSearchSpace
from search_space.spaces import SearchSpace
from search_space.context_manager import SamplerContext
T = TypeVar("T")

type_dict = {}
type_dict[int] = NaturalSearchSpace


class TypeBuilder(Generic[T]):

    def __init__(self, space: SearchSpace) -> None:
        super().__init__()
        self.space = space

    def __call__(self, constraint_fun=None, min=None, max=None, options=None, distribute_like=None):
        return self.space(constraint_fun, min, max, options, distribute_like)

    def __getitem__(self, item):
        try:
            self.space.len_space.append(item)
        except TypeError:
            self.space = TensorSearchSpace(self.space, [item])

        return self


class RandomValueFunc(TypeBuilder, Generic[T]):
    def __call__(self, constraint_fun=None, min=None, max=None, options=None, distribute_like=None) -> T:
        space = super().__call__(constraint_fun, min, max, options, distribute_like)
        return space.get_sample()[0]

    def __getitem__(self, item) -> 'RandomValueFunc[List[T]]':
        return super().__getitem__(item)


class RandomValueClass():
    def __getitem__(self, _type: Type[T]) -> RandomValueFunc[T]:
        return RandomValueFunc[T](type_dict[_type]())


RandomValue = RandomValueClass()


class SpaceDomain(Generic[T]):

    def __init__(self, space) -> None:
        self.space = space

    def __or__(self, func_constraint):
        return self

    def get_sample(self) -> Tuple[T, SamplerContext]:
        return self.space.get_sample()

    def __repr__(self) -> str:
        return T.__repr__()


class DomainFactory(TypeBuilder, Generic[T]):
    def __call__(self, constraint_fun=None, min=None, max=None, options=None, distribute_like=None) -> SpaceDomain[T]:
        space = super().__call__(constraint_fun, min, max, options, distribute_like)
        return SpaceDomain[T](space)

    def __getitem__(self, item) -> 'DomainFactory[List[T]]':
        return super().__getitem__(item)


class DomainClass:
    def __getitem__(self, _type: Type[T]) -> DomainFactory[T]:
        return DomainFactory[T](type_dict[_type]())


Domain = DomainClass()

InnerT = TypeVar("InnerT")


class _SampleOf(Generic[InnerT]):

    def __getitem__(self, space: T) -> InnerT:
        self.space = space
        return self

    def __repr__(self) -> str:
        return self.space.__repr__()


SampleOf = _SampleOf()


# TODO: debug typing Union
def test_final_syntax():

    class ProblemItem:
        BagsDimensionsDomain = Domain[int][10]()

        def __init__(self, weight: Union[int, str]) -> None:
            self.weight = weight

    a = SampleOf[BagsDimensionsDomain]
    BagsDimensionsDomain = Domain[int][10]()
    ItemsSpace = Domain[ProblemItem][10]() | (lambda x, y, i: (
        y in BagsDimensionsDomain, x[i].weight < y[i + 1]
    ))

    items, context = ItemsSpace.get_sample()
    bags, _ = BagsDimensionsDomain.get_sample(context=context)

    for i in range(1, 10):
        assert items[i - 1].weight < bags[i]
