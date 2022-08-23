from copy import copy
from typing import Type
from search_space.spaces import SearchSpace, SearchSpaceDomain
import inspect
from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.errors import UnSupportOpError, InvalidSampler


class ObjectDomain(SearchSpaceDomain):
    def __init__(self, cls) -> None:
        super().__init__()
        self.cls = cls

        for key, items in cls.__dict__.items():
            if isinstance(items, SearchSpace):
                self.__dict__[key] = items._create_domain(items.initial_domain)

    #################################################################
    #                                                               #
    #                  Transformations                              #
    #                                                               #
    #################################################################

    @visitor.on("node")
    def transform(self, node, context):
        pass

    @visitor.when(ast.UniversalVariable)
    def transform(self, node, context: SamplerContext):
        raise UnSupportOpError(self, node, "transform")

    #################################################################
    #                                                               #
    #             Class Transformations                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.Index)
    def transform(self, node, context: SamplerContext):
        name = node.index
        self.__dict__[name] = self.__dict__[name].transform(node.ast, context)
        return self

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def transform(self, node: ast.SelfValue, context: SamplerContext):
        return self

    @visitor.when(ast.NaturalValue)
    def transform(self, node: ast.NaturalValue, context: SamplerContext):
        try:
            return node.other.get_sampler(context=context)[0]
        except AttributeError:
            return node.other

    #################################################################
    #                                                               #
    #                  Check Sample                                 #
    #                                                               #
    #################################################################

    @visitor.on("node")
    def check_sampler(self, node, sampler, context):
        pass

    #################################################################
    #                                                               #
    #             Class Transformations                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.Index)
    def check_sampler(self, node, sampler, context):
        name = node.index
        local_domain = self.__dict__[name]
        property_sample = sampler.__dict__[name].get_sampler(context)
        result, _ = self.cls.__dict__[
            name].check_sampler(property_sample, context, local_domain=local_domain)

        if result:
            return self

        raise InvalidSampler(f"the property {name} has error")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def check_sampler(self, node: ast.SelfValue, sampler, context: SamplerContext):
        return self

    @visitor.when(ast.NaturalValue)
    def check_sampler(self, node: ast.NaturalValue, sampler, context: SamplerContext):
        try:
            return node.other.get_sampler(context=context)[0]
        except AttributeError:
            return node.other


def decorator(func):
    def f(*args, **kwargs):
        _self = args[0]
        try:
            context = kwargs["__context__"]
            fabric = kwargs["__fabric__"]
            domain = kwargs["__domain__"]
        except KeyError:
            context = _self.__context__
            fabric = _self.__fabric__
            domain = _self.__domain__

        new_kwargs = {}
        func_data = inspect.getfullargspec(func)
        args_len = len(func_data.args)
        defaults_len = len(func_data.defaults)
        for index in range(defaults_len):
            ss = func_data.defaults[defaults_len - 1 - index]
            if not isinstance(ss, SearchSpace):
                try:
                    value = args[args_len - 1 - index]
                    new_kwargs[func_data.args[args_len -
                                              1 - index]] = value
                except IndexError:
                    new_kwargs[func_data.args[args_len - 1 - index]] = ss
                continue

            for key, item in _self.__class__.__dict__.items():
                if ss.is_equal(item):  # check instance
                    ss = fabric.__dict__[key].get_sampler(context, local_domain=domain.__dict__[key])[
                        0]
                    break
            try:
                # check rules
                value = args[args_len - 1 - index]
                context.registry_sampler(ss, value)
            except IndexError:
                value = ss.get_sampler(context)

            new_kwargs[func_data.args[args_len - 1 - index]] = value

        args = args[0: args_len - defaults_len]
        return func(*args, **new_kwargs)
    return f


class MetaClassFabricSearchSpace(Type):
    class_decorated = False

    def __call__(cls, *args, **kwargs):
        # check if normal caller or ss solicit

        try:
            logs_name = kwargs["log_name"]
        except:
            logs_name = None

        if not cls.class_decorated:

            for attr in cls.__dict__:  # there's propably a better way to do this
                if callable(getattr(cls, attr)):
                    setattr(cls, attr, decorator(getattr(cls, attr)))

        oss = FabricSearchSpace(cls, (args, kwargs), log_name=logs_name)
        for key, item in cls.__dict__.items():
            if isinstance(item, SearchSpace):
                oss.__dict__[key] = copy(item)

        return oss


class FabricSearchSpace(SearchSpace):
    def __init__(self, cls, initial_data, log_name=None) -> None:
        super().__init__(None, None, log_name)
        self.cls = cls
        self.initial_domain = initial_data

    def _get_random_value(self, domain, context):
        args, kw = self.initial_domain
        result = type.__call__(self.cls, *args, **kw,
                               __context__=context, __fabric__=self, __domain__=domain)
        result.__context__ = context
        result.__fabric__ = self
        result.__domain__ = domain
        return result

    def _create_domain(self, domain) -> SearchSpaceDomain:
        return ObjectDomain(self)
