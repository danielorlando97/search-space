from typing import Generic, Tuple, Type, TypeVar, List
from search_space.spaces.build_in_spaces import ListSearchSpace, SpacesManager, BasicCategoricalSearchSpace, TensorSearchSpace
from search_space.spaces import SearchSpace
from search_space.context_manager import SamplerContext
T = TypeVar("T")


class TypeBuilder(Generic[T]):

    def __init__(self, space: SearchSpace) -> None:
        super().__init__()
        self._space = space
        self.is_tensor_type = False

    @property
    def space(self):
        return self._space if not self.is_tensor_type else self.__space

    def __call__(self, constraints=None, min=None, max=None, options=None, distribute_like=None):

        kwarg = {}

        if not distribute_like is None:
            kwarg['distribute_like'] = distribute_like

        if not options is None:
            def f(x): return True
            if not min is None:
                def f(x): return f(x) and x > min
            if not max is None:
                def f(x): return f(x) and x < max

            options = [option for option in options if f(options)]
            result = BasicCategoricalSearchSpace(
                *options, **kwarg)
        else:

            if not min is None:
                kwarg['min'] = min
            if not max is None:
                kwarg['max'] = max

            result = self.space(**kwarg)

        if self.is_tensor_type:
            result = self._space.set_type(result)

        if constraints is None:
            return result

        return result.__ast_optimization__(constraints)

    def __getitem__(self, item):
        try:
            item = item.space
            item.space_name = item.space_name + '_tensor_size'
        except AttributeError:
            pass

        try:
            self._space.len_spaces.append(item)
        except AttributeError:
            self.__space = self._space
            self._space = ListSearchSpace([item])

        self.is_tensor_type = True
        return self


class RandomValueFunc(TypeBuilder, Generic[T]):

    def __init__(self, space: SearchSpace) -> None:
        super().__init__(space)

    def __call__(self, constraint_fun=None, min=None, max=None, options=None, distribute_like=None, context: SamplerContext = None) -> T:
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
        self.space = self.space.__ast_optimization__(func_constraint)
        return self

    def get_sample(self, context: SamplerContext = None) -> Tuple[T, SamplerContext]:
        return self.space.get_sample(context=context)

    @property
    def random_sample(self) -> T:
        return self


class DomainFactory(TypeBuilder, Generic[T]):
    def __call__(self, constraint_fun=None, min=None, max=None, options=None, distribute_like=None) -> SpaceDomain[T]:
        space = super().__call__(constraint_fun, min, max, options, distribute_like)
        return SpaceDomain[T](space)

    def __getitem__(self, item) -> 'DomainFactory[List[T]]':
        return super().__getitem__(item)

    def __or__(self, func_constraint):
        return self.__call__(constraint_fun=func_constraint)


class DomainClass:
    def __getitem__(self, _type: Type[T]) -> DomainFactory[T]:
        types_space_class = SpacesManager().get_space_by_type(_type)
        return DomainFactory[T](types_space_class)


Domain = DomainClass()
