from copy import copy
import inspect
from token import EXACT_TOKEN_TYPES
from search_space.context_manager.sampler_context import SamplerContext
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces import BasicSearchSpace
import imp
from typing import List, Type
from search_space.utils.singleton import Singleton
from search_space.spaces import SearchSpace
from search_space.spaces.algebra_constraint import ast as ast_constraint

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
            return _SpaceFactory(_type)


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
            _ = self.default.get_sample
        except AttributeError:
            return self.default

        return self.default.get_sample(context=context)[0]


class ClassFunction:
    def __init__(self, func, context, sub_space: list) -> None:
        self.func = func
        self.context = context

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
            for i, value in enumerate(reversed(func_data.defaults)):

                try:
                    value = value.space
                except AttributeError:
                    pass

                try:
                    value = [s for s in sub_space if hash(s) == hash(value)][0]
                except IndexError:
                    pass
                except TypeError:
                    pass

                try:
                    if not value.space_name.startswith(f'{self.params[-1 -i].name}:'):
                        value.space_name = f'{self.params[-1 -i].name}:{value.space_name}'
                except:
                    pass

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
                    new_args.append(arg.get_sample(context=self.context))
        return new_args

    def __call__(self, *args, **kwds):
        new_args = self.sample_params(*args, **kwds)
        return self.func(*new_args)


class _SpaceFactory:
    def __init__(self, _type) -> None:
        self.type = _type

    def __call__(self, *args, **kwds):
        return SpaceFactory(self.type)


class SpaceFactory(BasicSearchSpace):
    def __init__(self, _type, distribute_like=None) -> None:
        super().__init__(_type, None)

        self.ast_constraint = ast_constraint.AstRoot([])
        self.type = _type
        self._sub_space = {}
        self.space_name = _type.__name__

        for name, member in self.type.__dict__.items():
            try:
                if isinstance(member.space, BasicSearchSpace):
                    self._sub_space[name] = copy(member.space)
                    self._sub_space[name].set_hash(hash(member.space))
                    self._sub_space[name].visitor_layers += [
                        visitors.EvalAstChecked(),
                        visitors.MemberAstModifierVisitor(self, name)
                    ]

            except AttributeError:
                pass

    def __sampler__(self, domain, context: SamplerContext):
        instance_context = context.create_child(f'{self.space_name}_members')
        sub_space_list = list(self._sub_space.values())

        class_func = ClassFunction(
            self.type.__init__, instance_context, sub_space_list)
        class_instance = domain(*class_func.sample_params())

        # there's propably a better way to do this
        for name, method in inspect.getmembers(class_instance, inspect.ismethod):
            setattr(class_instance, name,
                    ClassFunction(method, instance_context, sub_space_list))

        return class_instance, instance_context

    def __ast_optimization__(self, ast_list):

        super().__ast_optimization__(ast_list)

        for key, space in self._sub_space.items():
            self._sub_space[key] = space.__ast_optimization__(ast_list)

        return self

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self._clean_asts.asts += ast.asts
        return self

    def __getitem__(self, index):
        return self._sub_space[index]

    def layers_append(self, *args):
        super().layers_append(*args)

        for space in self._sub_space.values():
            space.layers_append(*args)

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
