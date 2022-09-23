from search_space.spaces.algebra_constraint.ast import UniversalVariableNode, NaturalValue


class FunctionNode(UniversalVariableNode):
    def __init__(self, func, args, kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs


class AdvancedFunctionNode(FunctionNode):
    def __init__(self, target, func, args, kwargs, cls=None) -> None:
        super().__init__(cls, func, args, kwargs)
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
