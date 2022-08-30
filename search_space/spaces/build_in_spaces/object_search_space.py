from copy import copy
from typing import Type
from search_space.spaces import SearchSpace, SearchSpaceDomain
import inspect
from search_space.spaces import visitors


class ObjectDomain(SearchSpaceDomain):
    def __init__(self, space) -> None:
        super().__init__()
        self.space = space
        self.domain = {}
        self.attribute_attention = visitors.AttributeAttention()

        for key, items in space.__dict__.items():
            if isinstance(items, SearchSpace):
                self.domain[key] = items._create_domain(items.initial_domain)

    @property
    def initial_limits(self):
        result = {}

        for name, domain in self.domain.items():
            result[name] = domain.initial_limits

        return result

    @property
    def limits(self):
        result = {}

        for name, domain in self.domain.items():
            result[name] = domain.limits

        return result

    def transform(self, node, context):
        for name, domain in self.domain.items():
            ast = self.attribute_attention.visit(name, node)
            self.domain[name] = domain.transform(ast, context)

        return self

    def check_sampler(self, node, sampler, context):
        visitors.ValidateSampler(context, self.space).visit(sampler, node)
        return self

# TODO: Check If the params complies with constraint rules
# TODO: Add decorator for add contextual functions


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
                    try:
                        # check rules
                        value = args[args_len - 1 - index]
                        context.registry_sampler(fabric.__dict__[key], value)
                    except IndexError:
                        value = fabric.__dict__[key].get_sampler(
                            context, local_domain=domain.domain[key], not_save=func.__name__ != '__init__')[0]

                    new_kwargs[func_data.args[args_len - 1 - index]] = value
                    break

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
            cls.class_decorated = True
            for attr in cls.__dict__:  # there's propably a better way to do this
                if callable(getattr(cls, attr)):
                    setattr(cls, attr, decorator(getattr(cls, attr)))

        oss = FabricSearchSpace(cls, (args, kwargs), log_name=logs_name)
        for key, item in cls.__dict__.items():
            if isinstance(item, SearchSpace):
                oss.__dict__[key] = copy(item)

        return oss


class FabricSearchSpace(SearchSpace):
    def __init__(self, cls, initial_data=None, log_name=None, distribute_like=None) -> None:
        super().__init__(None, distribute_like, log_name)
        self.class_type = cls
        self.initial_domain = initial_data

    def _get_random_value(self, domain, context):
        args, kw = self.initial_domain
        result = type.__call__(self.class_type, *args, **kw,
                               __context__=context, __fabric__=self, __domain__=domain)
        result.__context__ = context
        result.__fabric__ = self
        result.__domain__ = domain
        return result

    # TODO: Add domain to create domain
    def _create_domain(self, domain) -> SearchSpaceDomain:
        return ObjectDomain(self)

    def __copy__(self):
        instance = super().__copy__()

        instance.class_type = self.class_type
        instance.initial_domain = self.initial_domain

        for key, item in self.__dict__.items():
            if isinstance(item, SearchSpace):
                instance.__dict__[key] = copy(item)

        return instance
