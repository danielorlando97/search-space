from search_space.spaces.algebra_constraint.ast import UniversalVariableNode
from .search_space import SearchSpace
from itertools import chain


class HandlerClass(type):

    def __call__(cls, *args, **kwargs):

        for arg in chain(args, kwargs.values()):
            if isinstance(arg, UniversalVariableNode):
                is_natural_value = False
                break
        else:
            is_natural_value = True

        # new_args = []
        # for arg in args:
        #     if isinstance(arg, UniversalVariableNode):
        #         new_args.append(arg)

        #     else:
        #         new_args.append(arg)

        # instances.kwargs = {}
        # for key, arg in kwargs.items():
        #     if isinstance(arg, UniversalVariableNode):
        #         instances.kwargs[key] = arg

        #     else:
        #         instances.kwargs[key] = NaturalValue(arg)

        instances = super(HandlerClass, cls).__call__(*args, **kwargs)
        if not is_natural_value:
            return DelegateUniversalVarDepended(instances)
        return instances


class DelegateUniversalVarDepended(UniversalVariableNode):
    def __init__(self, instance) -> None:
        super().__init__()
        self.instance = instance


class DelegateSearchSpace(SearchSpace, metaclass=HandlerClass):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__((), None, [])
        self.args = args
        self.kwargs = kwargs

    def __domain_filter__(self, domain, context):
        args = []
        for arg in self.args:
            try:
                args.append(arg.get_sample(context=context)[0])
            except AttributeError:
                args.append(arg)

        kwargs = {}
        for key, arg in self.kwargs.items():
            try:
                kwargs[key] = arg.get_sample(context=context)[0]
            except AttributeError:
                kwargs[key] = arg

        return (arg, kwargs)

    def __check_sample__(self, sample, ast_result, context):
        return sample

    def __sampler__(self, domain, context):
        args, kwargs = domain
        return self(*args, **kwargs)

    def __call__(self, *args, **kwds):
        raise NotImplementedError()


class Function(DelegateSearchSpace):

    def __invert__(self, *args, **kwargs):
        raise NotImplementedError()


class Predicate(DelegateSearchSpace):
    def __modifier_finite_domain__(self, domain, *args, **kwargs):
        raise NotImplementedError()

    def __modifier_infinite_domain__(self, _min, _max, *args, **kwargs):
        raise NotImplementedError()
