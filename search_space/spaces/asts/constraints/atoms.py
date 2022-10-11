from .expr_ops import ExprOpsNode
from .__base__ import check_natural_value, UniversalVariableNode
from search_space.utils.ast_tools import decorated_all_methods
from search_space.errors import UnSupportOpError
from . import __namespace__ as nsp


def natural_node_check(fn):
    def f(*args):
        if not isinstance(args[1], NaturalValue):
            raise UnSupportOpError(args[0], args[1], 'members')

        return fn(*args)
    f.__name__ = fn.__name__
    return f


@decorated_all_methods(check_natural_value)
@decorated_all_methods(natural_node_check)
class AtomsOp(ExprOpsNode):

    def __getattr__(self, name):
        return GetAttr(self, name)

    def __getitem__(self, index):
        return GetItem(self, index)


class GetAttr(AtomsOp):
    pass


class GetItem(AtomsOp):
    pass


class Atoms(AtomsOp):
    def __init__(self, target) -> None:
        super().__init__(target, None)


class NaturalValue(Atoms, metaclass=nsp.NaturalValueNode):
    pass


class SelfNode(Atoms):
    def __init__(self) -> None:
        super().__init__(None)

    @ property
    def is_self(self):
        return True


class NotEvaluate(Atoms):
    def __init__(self) -> None:
        super().__init__(None)


class FunctionNode(NaturalValue):
    def __init__(self, func, args, kwargs) -> None:
        super().__init__(None)
        self.func = func
        self.args = args
        self.kwargs = kwargs


class AdvancedFunctionNode(FunctionNode):
    def __init__(self, target, func, args, kwargs, cls=None) -> None:
        super().__init__(func, args, kwargs)
        self.cls = cls
        self.args_target, self.kw_target = target


def params_analyze(func, args, kwargs, cls=None):
    new_args = []
    new_kwargs = {}
    var_intro_arg = []
    var_intro_kw = []

    for i, arg in enumerate(args):
        if isinstance(arg, UniversalVariableNode):
            var_intro_arg.append(i)
            new_args.append(arg)
        else:
            new_args.append(NaturalValue(arg))

    for name, arg in kwargs.items():
        if isinstance(arg, UniversalVariableNode):
            var_intro_kw.append(name)
            new_kwargs[name] = args
        else:
            new_kwargs[name] = NaturalValue(arg)

    if len(var_intro_arg) + len(var_intro_kw) > 0:
        return AdvancedFunctionNode((var_intro_arg, var_intro_kw), func, new_args, kwargs, cls)

    return FunctionNode(func, new_args, new_kwargs)


class AdvancedSelectorMetaClass(type):
    def __call__(self, *args, **kwds):
        instance = super().__call__(*args, **kwds)
        return params_analyze(instance.__call__, args, kwds, cls=instance)


class FunctionalConstraintClass(metaclass=AdvancedSelectorMetaClass):
    def __init__(self, *args, **kwgs) -> None:
        pass


class FunctionalConstraintFactory:
    def __mro_entries__(self, x):
        return FunctionalConstraintClass, object,

    def __call__(self, func):
        def f(*args, **kwargs):
            return params_analyze(func, args, kwargs)
        return f


FunctionalConstraint = FunctionalConstraintFactory()
