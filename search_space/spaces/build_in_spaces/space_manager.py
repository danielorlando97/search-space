from copy import copy
import inspect
from token import EXACT_TOKEN_TYPES
from typing_extensions import Self
from search_space.context_manager.sampler_context import SamplerContext
from search_space.sampler.distribution_names import UNIFORM, UNIFORM_BERNOULLI
from search_space.spaces.visitors import visitors
from search_space.spaces import BasicSearchSpace
import imp
from typing import List, Type
from search_space.spaces.search_space_protocol import SearchSpaceProtocol
from search_space.utils.singleton import Singleton
from search_space.spaces import SearchSpace
from search_space.spaces.asts import constraints as ast_constraint
from typing import _UnionGenericAlias
from search_space.spaces.domains.categorical_domain import CategoricalDomain

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
            if type(_type) == _UnionGenericAlias:
                args = [self.get_space_by_type(t) for t in _type.__args__]
                return UnionSpace(*args)

            def f(*args, **kwargs):

                if _type == type(None):
                    return NoneSpace()

                if _type == Self:
                    return SelfSpace()

                return SpaceFactory(_type)
            return f


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
    def __init__(self, func, context, sub_space: list, _self) -> None:
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
                    value = copy(value)
                # except TypeError:
                #     pass

                try:
                    value.__self_assign__(_self)
                except AttributeError:
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


class SpaceFactory(SearchSpace):
    def __init__(
        self, _type,
        distribute_like=None,
        sampler=None,
        ast=None,
        clean_asts=None,
        layers=[]
    ) -> None:

        super().__init__(
            _type,
            distribute_like,
            sampler,
            ast_constraint.AstRoot() if ast is None else ast,
            ast_constraint.AstRoot() if ast is None else clean_asts,
            layers
        )

        self.type = _type
        self._sub_space = {}
        self.space_name = _type.__name__

        for name, member in self.type.__dict__.items():
            try:
                if isinstance(member.space, BasicSearchSpace):
                    self._sub_space[name] = copy(member.space)
                    self._sub_space[name].set_hash(hash(member.space))
                    self._sub_space[name].layers_append(
                        visitors.EvalAstChecked(),
                        visitors.MemberAstModifierVisitor(self, name)
                    )

            except AttributeError:
                pass

        self.visitor_layers = []

    def __ast_init_filter__(self):
        return self.ast_constraint + self._clean_asts

    def __ast_result_filter__(self, result):
        return result

    def __sampler__(self, domain, context: SamplerContext):
        instance_context = context.create_child(f'{self.space_name}_members')
        sub_space_list = list(self._sub_space.values())

        class_func = ClassFunction(
            self.type.__init__, instance_context, sub_space_list, self.type)
        class_instance = self.type(*class_func.sample_params())

        # there's propably a better way to do this
        for name, method in inspect.getmembers(class_instance, inspect.ismethod):
            setattr(class_instance, name,
                    ClassFunction(method, instance_context, sub_space_list,  self.type))

        return class_instance, instance_context

    def __ast_optimization__(self, ast_list):

        super().__ast_optimization__(ast_list)

        for key, space in self._sub_space.items():
            self._sub_space[key] = space.__ast_optimization__(ast_list)

        return self

    def __getitem__(self, index):
        return self._sub_space[index]

    def layers_append(self, *args):
        super().layers_append(*args)

        for space in self._sub_space.values():
            space.layers_append(*args)


class SelfSpace:
    def __init__(self, distribute_like=None) -> None:
        self.self_space = None

    def get_sample(self, context=None, local_domain=None):
        return self.self_space.get_sample()[0], context

    def __getattr__(self, __name: str):
        return getattr(self.self_space, __name)

    def __self_assign__(self, space):
        if self.self_space is None:
            self.self_space = SpacesManager().get_space_by_type(space)()


class NoneSpace(BasicSearchSpace):
    def __init__(self) -> None:
        super().__init__(None, None)

    def get_sample(self, context=None, local_domain=None):
        return None, context

    def __ast_optimization__(self, ast_list):
        return self


class UnionSpace(BasicSearchSpace):
    def __init__(self, *domain, distribute_like=UNIFORM) -> None:
        super().__init__(CategoricalDomain(domain), distribute_like=distribute_like)

    def get_sample(self, context=None, local_domain=None):
        space, context = super().get_sample(context, local_domain)
        return space.get_sample(context, local_domain)

    def __call__(self, *args, **kwds):
        self.initial_domain = CategoricalDomain(
            [space(*args, **kwds) for space in self.initial_domain.list]
        )

        return self

    def __self_assign__(self, space):

        for s in self.initial_domain.list:
            try:
                s.__self_assign__(space)
            except AttributeError:
                pass
