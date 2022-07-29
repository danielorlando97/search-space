DEBUG_SAMPLER = True


class Singleton(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances


class ContextManagerSearchSpace(metaclass=Singleton):
    def __init__(self) -> None:
        self.__dict = {}

    def _get_last_sampler(self, search_space):
        try:
            return self.__dict[search_space]
        except KeyError:
            return None

    def _save_new_sampler(self, search_space, value):
        self.__dict[search_space] = value

    def reset(self):
        self.__dict = {}


class SearchSpace:
    def __init__(self, domain, distribute_like, log_name=None) -> None:
        self._distribution = distribute_like
        self.domain = domain
        self.constraint_list = []
        self.__cache = None
        self.scope = log_name if not log_name is None else self.__class__.__name__

    def clean_cache(self):
        self.__cache = None

    def get_sampler(self, local_domain=None):
        cache_value = ContextManagerSearchSpace()._get_last_sampler(self)
        if not cache_value is None:
            return cache_value

        transformers = [c for c in self.constraint_list if c.is_transformer]
        conditions = [c for c in self.constraint_list if c.is_condition]

        domain = self.domain if local_domain is None else local_domain
        if DEBUG_SAMPLER:
            print(f'Init with domain {domain} in {self.scope}')
        for c in transformers:
            domain = self._check_transform(c, domain)

        if DEBUG_SAMPLER:
            print(f'Transformed domain {domain} in {self.scope}')
        while True:
            sample = self._get_random_value(domain)
            if DEBUG_SAMPLER:
                print(
                    f'Check conditions by sampler {sample} in {self.scope}')
            for c in conditions:
                if not self._check_condition(c, sample):
                    break
            else:
                ContextManagerSearchSpace()._save_new_sampler(self, sample)
                return sample

    def _get_random_value(self, domain):
        return self._distribution.get_random_value(domain)

    def _check_transform(self, constraint, domain):
        return constraint.transform(domain)

    def _check_condition(self, constraint, sample):
        return constraint.check_condition(sample)

    def __or__(self, other):
        try:
            for f in other:
                f(self)
        except TypeError:
            other(self)
        return self

    def such_that(self, func):
        func(self)
        return self

    def _great_equal(self, other):
        raise TypeError(
            f"'>=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _great(self, other):
        raise TypeError(
            f"'>' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _less_equal(self, other):
        raise TypeError(
            f"'<=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _less(self, other):
        raise TypeError(
            f"'<' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _not_equal(self, other):
        raise TypeError(
            f"'!=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    class SearchSpaceConditions:
        def __init__(self, ss, func) -> None:
            self.ss = ss
            self.func = func

        def __eq__(self, __o: bool) -> bool:
            return self.func(self.ss.get_sampler()) == __o

    def __ge__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv >= other)

    def __gt__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv > other)

    def __le__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv <= other)

    def __lt__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv < other)

    def __ne__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv != other)

    def __eq__(self, other):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: ssv == other)

    def __hash__(self) -> int:
        return id(self)


class SearchSpaceConstraint:
    def __init__(self, value, search_space) -> None:
        self.value = value
        self.__ss = search_space
        self.__conditional_value = None

    def transform(self, domain):
        if self.__conditional_value == False:
            return domain

        return self._func_transform(domain)

    def check_condition(self, sampler):
        if self.__conditional_value == False:
            return True

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
            return self.value.get_sampler()
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


class UniversalVariable:
    def __init__(self, father=None, func=None) -> None:
        self.father = father
        self.func = func

    # def __lshift__(self, other):
    #     self.ss = other
    #     return other

    def __ge__(self, other):
        return UniversalVariable(father=self, func=lambda ss: ss._great_equal(other))

    def __gt__(self, other):
        return UniversalVariable(father=self, func=lambda ss: ss._great(other))

    def __le__(self, other):
        return UniversalVariable(father=self, func=lambda ss: ss._less_equal(other))

    def __lt__(self, other):
        return UniversalVariable(father=self, func=lambda ss: ss._less(other))

    def __ne__(self, other):
        return UniversalVariable(father=self, func=lambda ss: ss._not_equal(other))

    def __getattr__(self, name):
        return UniversalVariable(father=self, func=lambda ss: ss.__class__.__dict__[name])

    def __rrshift__(self, other):
        return UniversalVariable(father=self, func=lambda ss: other >> ss)

    def __call__(self, ss: SearchSpace) -> None:
        if self.func is None:
            return ss

        return self.func(self.father(ss))


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
