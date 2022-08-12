# try:
#     from .abs_search_space import SearchSpace
# except (ModuleNotFoundError, ImportError):
#     from abs_search_space import SearchSpace

from .search_space import SearchSpace
from .universal_variable import UniversalVariable


class SearchSpaceConstraint:
    def __init__(self, value, search_space) -> None:
        self.value = value
        self.__ss = search_space
        self.__conditional_value = None

    def transform(self, domain, context):
        if self.__conditional_value == False:
            return domain
        self.__context = context
        return self._func_transform(domain)

    def check_condition(self, sampler, context):
        if self.__conditional_value == False:
            return True

        self.__context = context
        return self._func_condition(sampler)

    def _func_transform(self, domain):
        raise TypeError(
            f"is constraint isn't transform constraint")

    def _func_condition(self, sampler):
        raise TypeError(
            f"is constraint isn't conditional constraint")

    @property
    def target(self):
        return self.__ss

    @property
    def is_condition(self):
        return False

    @property
    def is_transformer(self):
        return False

    @property
    def is_context_sensitive(self):
        return isinstance(self.value, SearchSpace)

    @property
    def _real_value(self):
        if self.is_context_sensitive:
            return self.value.get_sampler(context=self.__context)[0]
        else:
            return self.value

    def depend_of(self, other):
        return self.value == other

    def __rshift__(self, other):
        self.__conditional_value = other
        return self

    def __rrshift__(self, other):
        self.__conditional_value = other
        return self


class FunctionConstraint(SearchSpaceConstraint):
    @property
    def is_condition(self):
        return True

    def __init__(self, params, func) -> None:
        self.params = params
        self.func = func
        self.index = [i for i, p in enumerate(
            params) if isinstance(p, UniversalVariable)][0]
        super().__init__(None, None)

    def __call__(self, search_space):
        search_space.constraint_list.append(self)
        self.__ss = search_space
        return self

    @property
    def is_context_sensitive(self):
        result = False
        for i, param in enumerate(self.params):
            if i == self.index:
                continue

            self.value = param
            result |= super().is_context_sensitive

        return result

    def _func_condition(self, sampler):
        params = self._real_value
        params[self.index] = sampler

        result = self.func(*params)
        return result

    @property
    def _real_value(self):
        result = []
        for i, param in enumerate(self.params):
            if i == self.index:
                result.append(param)
                continue
            self.value = param
            result.append(super()._real_value)

        return result


class MetaPredication(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        instance = super(
            MetaPredication, cls).__call__(*args, **kwargs)
        try:
            instance.__call__
            return FunctionConstraint(list(args), instance.__call__)
        except AttributeError:
            l = list(args)
            return FunctionConstraint(l[0:-1], l[-1])


class Predication(metaclass=MetaPredication):
    def __init__(self, *args) -> None:
        pass
