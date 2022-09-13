from typing import Generic, Tuple, Type, TypeVar, List
from search_space.spaces.build_in_spaces import TensorSearchSpace, SpacesManager, CategoricalSearchSpace
from search_space.spaces import SearchSpace
from search_space.context_manager import SamplerContext
from search_space.sampler import SamplerFactory
from search_space.sampler.distribution_names import UNIFORM
T = TypeVar("T")


class TypeBuilder(Generic[T]):

    def __init__(self, space: SearchSpace) -> None:
        super().__init__()
        self._space = space
        self.is_tensor_type = False

    @property
    def space(self):
        return self._space if not self.is_tensor_type else self._space.type_space

    def __call__(self, constraints=[], min=None, max=None, options=None, distribute_like=None):

        if not options is None:
            def f(x): return True
            if not min is None:
                def f(x): return f(x) and x > min
            if not max is None:
                def f(x): return f(x) and x < max

            options = [option for option in options if f(options)]
            result = CategoricalSearchSpace(*options)

        else:
            result = self.space(min=min, max=max)

        sampler = SamplerFactory().create_sampler(
            distribute_like if not distribute_like is None else UNIFORM, search_space=result)
        result = result.set_sampler(sampler)

        if self.is_tensor_type:
            self._space.type_space = result
            return self._space.__ast_optimization__(constraints)

        return result.__ast_optimization__(constraints)

    def __getitem__(self, item):
        try:
            self._space.len_spaces.append(item)
        except AttributeError:
            self._space = TensorSearchSpace(self._space, [item])

        self.is_tensor_type = True
        return self


class RandomValueFunc(TypeBuilder, Generic[T]):
    def __call__(self, constraint_fun=[], min=None, max=None, options=None, distribute_like=None, context: SamplerContext = None) -> T:
        space = super().__call__(constraint_fun, min, max, options, distribute_like)
        return space.get_sample(context=context)[0]

    def __getitem__(self, item) -> 'RandomValueFunc[List[T]]':
        return super().__getitem__(item)


class RandomValueClass():
    def __getitem__(self, _type: Type[T]) -> RandomValueFunc[T]:
        types_space_class = SpacesManager().get_space_by_type(_type)
        return RandomValueFunc[T](types_space_class)


RandomValue = RandomValueClass()


class SpaceDomain(Generic[T]):

    def __init__(self, space) -> None:
        self.space: SearchSpace = space

    def __or__(self, func_constraint):
        self.space.__ast_optimization__(func_constraint)
        return self

    def get_sample(self, context: SamplerContext = None) -> Tuple[T, SamplerContext]:
        return self.space.get_sample(context=context)


class DomainFactory(TypeBuilder, Generic[T]):
    def __call__(self, constraint_fun=[], min=None, max=None, options=None, distribute_like=None) -> SpaceDomain[T]:
        space = super().__call__(constraint_fun, min, max, options, distribute_like)
        return SpaceDomain[T](space)

    def __getitem__(self, item) -> 'DomainFactory[List[T]]':
        return super().__getitem__(item)


class DomainClass:
    def __getitem__(self, _type: Type[T]) -> DomainFactory[T]:
        types_space_class = SpacesManager().get_space_by_type(_type)
        return DomainFactory[T](types_space_class)


Domain = DomainClass()