from search_space.spaces.algebra_constraint.ast import UniversalVariableNode, NaturalValue
from itertools import chain


class HandlerClass(type):

    def __call__(cls, *args, **kwargs):
        instances = super(HandlerClass, cls).__call__()

        for arg in chain(args, kwargs.values()):
            if isinstance(arg, UniversalVariableNode):
                instances.is_natural_value = False
                break
        else:
            instances.is_natural_value = True

        instances.args = []
        for arg in args:
            if isinstance(arg, UniversalVariableNode):
                instances.args.append(arg)

            else:
                instances.args.append(NaturalValue(arg))

        instances.kwargs = {}
        for key, arg in kwargs.items():
            if isinstance(arg, UniversalVariableNode):
                instances.kwargs[key] = arg

            else:
                instances.kwargs[key] = NaturalValue(arg)

        return instances


class Function(UniversalVariableNode, metaclass=HandlerClass):
    def __init__(self) -> None:
        self.is_natural_value = None
        self.args = ()
        self.kwargs = {}

    def __invert__(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwds):
        pass


class Predicate(UniversalVariableNode, metaclass=HandlerClass):
    def __init__(self) -> None:
        self.is_natural_value = None
        self.args = ()
        self.kwargs = {}

    def __modifier_finite_domain__(self, domain, *args, **kwargs):
        raise NotImplementedError()

    def __modifier_infinite_domain__(self, _min, _max, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwds):
        pass
