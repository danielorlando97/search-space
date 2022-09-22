import inspect
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces import BasicSearchSpace
import imp
from typing import List, Type
from search_space.utils.singleton import Singleton
from search_space.spaces import SearchSpace
from search_space.errors import TypeWithoutDefinedSpace
# TODO: Change to Multiply definitions


class SpacesManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__spaces = {}

    @staticmethod
    def registry(_type: Type = None):
        def f(cls):
            manager = SpacesManager()
            if _type is None:
                manager.__spaces[cls] = cls
            else:
                manager.__spaces[_type] = cls

            return cls
        return f

    def get_space_by_type(self, _type: Type) -> Type[SearchSpace]:
        try:
            return self.__spaces[_type]
        except KeyError:
            return SpaceFactory(_type)


class FunctionParamInfo:
    def __init__(self, name) -> None:
        self.name = name
        self.type = None
        self.default = None

    def type_init(self):
        if self.default is None and not self.type is None:
            self.default = SpacesManager().get_space_by_type(self.type)()

    def __eq__(self, __o: object) -> bool:
        return __o == self.name

    def get_sample(self, context=None):
        if self.default is None:
            return None

        try:
            return self.default.get_sample(context=context)[0]
        except AttributeError:
            return self.default


class ClassFunction:
    def __init__(self, func) -> None:
        self.func = func

        func_data = inspect.getfullargspec(func)
        self.params: List[FunctionParamInfo] = []

        for arg in func_data.args:
            if arg == 'self':
                continue
            self.params.append(FunctionParamInfo(arg))

        for param in self.params:
            try:
                param.type = func_data.annotations[param.name]
            except KeyError:
                pass

        if not func_data.defaults is None:
            for i, value in enumerate(func_data.defaults):
                self.params[-1 - i].default = value

        for arg in self.params:
            arg.type_init()

    def sample_params(self, *args, **kwds):
        new_args = []
        args_index = 0

        for arg in self.params:
            try:
                new_args.append(kwds[arg.name])
            except KeyError:
                if args_index < len(args):
                    new_args.append(args[args_index])
                    args_index += 1
                else:
                    new_args.append(arg.get_sample())
        return new_args

    def __call__(self, *args, **kwds):
        new_args = self.sample_params(*args, **kwds)
        return self.func(*new_args)


class SpaceFactory(BasicSearchSpace):
    def __init__(self, _type) -> None:
        super().__init__(_type, None)

        # self.visitor_layers.append(visitors.Member)

    def __sampler__(self, domain, context):
        class_func = ClassFunction(domain.__init__)
        class_instance = domain(*class_func.sample_params())

        # there's propably a better way to do this
        for name, method in inspect.getmembers(class_instance, inspect.ismethod):
            setattr(class_instance, name, ClassFunction(method))

        return class_instance

    def __call__(self, *args, **kwds):
        return self


# class TestA:
#     def __init__(self, a: int, b: float = Domain[float]()) -> None:
#         self.a = a
#         self.b = b

#     def __str__(self) -> str:
#         try:
#             return f'a:{self.a}\nb:{self.b}\nc:{self.c}'
#         except AttributeError:
#             return f'a:{self.a}\nb:{self.b}\n'

#     def build(self, c: int):
#         self.c = c + self.b


# m = Domain[TestA]()
