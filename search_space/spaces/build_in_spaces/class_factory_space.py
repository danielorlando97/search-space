from search_space.sampler.distribution_names import UNIFORM
from .categorical_search_space import CategoricalSearchSpace
from search_space.spaces.algebra_constraint import visitors


def decorator(_self):
    def ff(func):
        def f(*args, **kwargs):
            context = _self.__context__.create_child()
            try:
                default_args, default_kws = _self.__abi__.abi[func.__name__]

                new_args = []
                for i, param in enumerate(default_args):
                    try:
                        new_args.append(args[i])
                    except IndexError:
                        new_args.append(param.get_sample(context=context)[0])

                new_kwargs = {}
                for key, item in default_kws.items():
                    try:
                        new_kwargs[key] = kwargs[key]
                    except KeyError:
                        kwargs[key] = item.get_sample(context=context)[0]

                return func(*new_args, **new_kwargs)
            except KeyError:
                return func(*args, **kwargs)

        return f
    return ff


class ABI_Class:
    def __init__(self) -> None:
        self.abi = {}

    def registry(self, name, *params, **kws):
        self.abi[name] = (params, kws)

    def __iter__(self):
        return self.abi.keys().__iter__()


class ClassFabricSearchSpace(CategoricalSearchSpace):
    def __init__(self, *domain, distribute_like=UNIFORM, visitor_layers=[]) -> None:
        super().__init__(*domain, distribute_like=distribute_like, visitor_layers=visitor_layers)

        self.abi = None

    def __space__(self, abi_class):
        pass

    def __sampler__(self, domain, context):
        instance_class = super().__sampler__(domain, context)

        if self.abi is None:
            self.abi = ABI_Class()
            self.__space__(self.abi)
        try:
            args, kws = self.abi.abi['__init__']

            new_args = []
            for param in args:
                new_args.append(param.get_sample(context=context)[0])

            new_kw = {}
            for key, item in kws.items():
                new_kw[key] = item.get_sample(context=context)[0]

            instance = instance_class(*new_args, **new_kw)

        except KeyError:
            instance = instance_class()

        instance.__context__ = context
        instance.__abi__ = self.abi
        for attr in self.abi:
            if callable(getattr(instance, attr)):
                setattr(instance, attr, decorator(
                    instance)(getattr(instance, attr)))

        return instance

    def __ast_optimization__(self, ast_list):

        self.abi = ABI_Class()
        self.__space__(self.abi)

        for key, item in self.__dic__.items():
            item.visitor_layers.append(visitors.MemberAstModifier(key))

        return super().__ast_optimization__(ast_list)


# TODO copy
