from copy import copy
import inspect
from typing_extensions import Self
from search_space.sampler import BERNOULLI
from search_space.spaces.visitors import visitors
from search_space.spaces import BasicSearchSpace
import imp
from typing import Any, List, Type, Callable, Dict
from search_space.utils.singleton import Singleton
from search_space.spaces.search_space import SearchSpace, GetSampleParameters, GetSampleResult
from search_space.spaces.asts import constraints as ast_constraint
from typing import _UnionGenericAlias
from search_space.spaces.domains.categorical_domain import CategoricalDomain


class SpacesManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__spaces = {}
        self.__metadata = {}

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

    def find_metadata(self, _type):
        return self.__metadata[_type]

    def save_metadata(self, _type, sub_space):
        self.__metadata[_type] = {}
        for name, method in inspect.getmembers(_type, inspect.isfunction):
            self.__metadata[_type][name] = ClassFunction(
                method, sub_space, _type
            )

        return self.__metadata[_type]


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

    def get_sample(self, params: GetSampleParameters = None, sub_space=[], path=None):
        if self.default is None:
            return None

        try:
            _ = self.default.get_sample
        except AttributeError:
            return self.default

        try:
            value = next(filter(
                lambda s: hash(s) == hash(self.default),
                sub_space
            ))

            name = value.space_name
            path_space = value.path_space
            value.space_name = self.default.space_name
        except StopIteration:
            value = self.default

            name = value.space_name
            path_space = value.path_space
            value.path_space = path_space if path is None else path

        result = value.get_sample(params)

        value.path_space = path_space
        value.space_name = name

        return result.sample


class ClassFunction:
    def __init__(
        self,
        func: Callable,
        sub_space: List[BasicSearchSpace],
        _self: Type,
        sampler_params: GetSampleParameters = None,
        params=None,
        instance=None,
        class_path=None
    ) -> None:

        self.func = func
        self.params = params
        self.sampler_params = sampler_params
        self.sub_space = []
        self.instance = instance
        self.class_path = class_path

        if params is None:
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

                    _value = copy(value)

                    try:
                        member = next(filter(
                            lambda s: hash(s) == hash(value),
                            sub_space
                        ))
                        _value.set_hash(hash(member))
                    except StopIteration:
                        pass
                    finally:
                        value = _value
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

    def get_new_func(
        self,
        params: GetSampleParameters,
        sub_space: List[BasicSearchSpace],
        instance=None,
        class_path=None
    ):
        result = ClassFunction(
            self.func, [], None, params, self.params, instance, class_path=class_path
        )
        result.sub_space = sub_space

        return result

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
                    new_args.append(
                        arg.get_sample(
                            params=self.sampler_params,
                            sub_space=self.sub_space,
                            path=self.class_path
                        )
                    )
        return new_args

    def __call__(self, *args, **kwds):
        previous_params = self.sampler_params
        self.sampler_params = self.sampler_params.create_child_context(
            f'called_{self.func.__name__}'
        )

        try:
            new_args = self.sample_params(*args, **kwds)
        except Exception as e:
            error = e

        self.sampler_params = previous_params

        try:
            raise error
        except NameError:

            return self.func(*([self.instance] + new_args))


class SpaceFactory(SearchSpace):
    def __init__(
        self, _type,
        distribute_like=None,
        sampler=None,
        ast=None,
        clean_asts=None,
        layers=[],
        path=None
    ) -> None:
        path = _type.__name__ if path is None else path

        super().__init__(
            _type,
            distribute_like,
            sampler,
            ast_constraint.AstRoot() if ast is None else ast,
            ast_constraint.AstRoot() if ast is None else clean_asts,
            layers,
            path=path
        )

        self.type = _type
        self._sub_space: Dict[str, BasicSearchSpace] = {}
        self.space_name = _type.__name__

        for name, member in inspect.getmembers(self.type):
            try:
                if isinstance(member.space, BasicSearchSpace):
                    self._sub_space[name] = copy(member.space)
                    self._sub_space[name].set_hash(hash(member.space))
                    self._sub_space[name].path_space = f'path.{name}'
                    self._sub_space[name].layers_append(
                        visitors.EvalAstChecked(),
                        visitors.MemberAstModifierVisitor(self, name)
                    )

            except AttributeError:
                pass

        manager = SpacesManager()
        try:
            self._metadata = manager.find_metadata(self.type)
        except KeyError:
            self._metadata = manager.save_metadata(
                self.type, list(self._sub_space.values()))

        self.visitor_layers = []

    def __ast_init_filter__(self):
        return self.ast_constraint + self._clean_asts

    def __ast_result_filter__(self, result):
        return result

    def __sampler__(self, domain, params: GetSampleParameters):
        instance_params = params.create_child_context(
            f'{self.space_name}_members'
        )
        key_list = list(self._sub_space.values())
        class_func = self._metadata['__init__'].get_new_func(
            instance_params, key_list, class_path=self.path_space
        )

        class_instance = self.type(*class_func.sample_params())
        class_instance.__instance_context__ = instance_params

        for name, class_func in self._metadata.items():
            if name == '__init__':
                continue

            setattr(
                class_instance, name,
                class_func.get_new_func(
                    instance_params, key_list, class_instance, class_path=self.path_space
                )
            )

        return class_instance, instance_params.context

    def __ast_optimization__(self, ast_list):

        super().__ast_optimization__(ast_list)

        for key, space in self._sub_space.items():
            self._sub_space[key] = space.__ast_optimization__(ast_list)

        return self

    def __save_ast_from_self__(self, ast_list):
        super().__ast_optimization__(ast_list)
        return self

    def __getitem__(self, index):
        return self._sub_space[index]

    def layers_append(self, *args):
        super().layers_append(*args)

        for space in self._sub_space.values():
            space.layers_append(*args)

    def __repr__(self) -> str:
        return f'Space({self.space_name})'


class SelfSpace:
    def __init__(self, distribute_like=None, path=None) -> None:
        self.self_space = None
        self.ast_cache = []
        self.path_space = path

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:
        self_params = GetSampleParameters(sampler=params.sampler)
        result = self.self_space.get_sample(self_params)
        return params.build_result(result.sample)

    def __getattr__(self, __name: str):
        return getattr(self.self_space, __name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        try:
            setattr(self.self_space, __name, __value)
        except AttributeError:
            super().__setattr__(__name, __value)

    def __self_assign__(self, space):
        if self.self_space is None:
            self.self_space = SpacesManager().get_space_by_type(space)(path=self.path_space)
            for ast in self.ast_cache:
                self.self_space = self.self_space.__ast_optimization__(ast)

    def __ast_optimization__(self, ast_list):
        if self.self_space is None:
            self.ast_cache.append(ast_list)
        else:
            self.self_space = self.self_space.__save_ast_from_self__(ast_list)

        return self


class NoneSpace(BasicSearchSpace):
    def __init__(self) -> None:
        super().__init__(None, None)

    def get_sample(self, params: GetSampleParameters, local_domain=None):
        return params.build_result(None)

    def __ast_optimization__(self, ast_list):
        return self

    def __eq__(self, __o: object) -> bool:
        return __o == None or super().__eq__(__o)


class UnionSpace(SearchSpace):
    def __init__(
        self,
        *domain,
        distribute_like=BERNOULLI,
        sampler=None,
        ast=None,
        clean_asts=None,
        layers=[],
        path=None
    ) -> None:

        super().__init__(
            CategoricalDomain(domain),
            distribute_like,
            sampler,
            ast_constraint.AstRoot() if ast is None else ast,
            ast_constraint.AstRoot() if ast is None else clean_asts,
            layers=[visitors.TypeDomainModifierVisitor()] if len(
                layers) == 0 else layers,
            path=path
        )

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:
        result = super().get_sample(params)
        return result.sample.get_sample(params)

        # try:
        # except RecursionError:
        #     if None in self.initial_domain.limits:
        #         warn('ForceResult: For RecursionError Select None Value')
        #         context.registry_sampler(space, None)
        #         return None, context
        #     else:
        #         raise RecursionErrorSpaceDefinition

    def __call__(self, *args, path=None, **kwds):
        path = 'union_space' if path is None else path + '.union'
        self.space_name = path
        self.initial_domain = CategoricalDomain(
            [space(*args, path=f'{path}._type_{i}', **kwds)
             for i, space in enumerate(self.initial_domain.list)]
        )

        return self

    def __ast_optimization__(self, ast_list):

        super().__ast_optimization__(ast_list)

        result = []
        for space in self.initial_domain.list:
            result.append(space.__ast_optimization__(ast_list))

        self.initial_domain.list = result

        return self

    def __self_assign__(self, space):

        for s in self.initial_domain.list:
            try:
                s.__self_assign__(space)
            except AttributeError:
                pass

    def __check_sample__(self, sample, ast_result, params):
        return

    def __copy__(self):

        result = type(self)(
            distribute_like=self.__distribute_like__,
            sampler=None,
            ast=ast_constraint.AstRoot(copy(self.ast_constraint.asts)),
            clean_asts=ast_constraint.AstRoot(copy(self._clean_asts.asts)),
            layers=copy(self.visitor_layers),
            path=self.space_name
        )

        result.initial_domain = copy(self.initial_domain)
        return result
