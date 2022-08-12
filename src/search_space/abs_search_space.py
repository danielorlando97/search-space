# try:
#     from ..tools.singleton import Singleton
# except (ModuleNotFoundError, ImportError):
#     from tools.singleton import Singleton

from ..tools.singleton import Singleton
from ..samplers import SamplerFactory, Sampler
from ..samplers.basic_names import UNIFORM
DEBUG_SAMPLER = False


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
    def __init__(self, domain, distribute_like=UNIFORM, log_name=None) -> None:
        self._distribution: Sampler = SamplerFactory(
        ).create_new_sampler(self, distribute_like)
        self.domain = domain
        self.constraint_list = []
        self.scope = log_name if not log_name is None else self.__class__.__name__

    def get_sampler(self, local_domain=None):
        """
            This method generate a new sampler by SearchSpace's domain and config
            This sample is unique for each instance of ContextManager
            It divide the constraint list in transforms list and conditional list
            The transforms are constraints that modification the SearchSpace's domain like <= (this reduce the domain)
            The conditionals are constraints that only can check before to generate the sampler like %2 == 0
        """

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

        self.__last_domain = domain
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
        """
            For default, this method generate a new random value intro the domain
            In the inherence, each class can do override it to change the types and form
            to generate new values
            for example: the categorical Search Space override it to get the random index
            and sample the category with that index
        """

        return self._distribution.get_random_value(domain)

    def _check_transform(self, constraint, domain):
        """
        """
        return constraint.transform(domain)

    def _check_condition(self, constraint, sample):
        """
        """
        return constraint.check_condition(sample)

    def __or__(self, other):
        try:
            for f in other:
                f(self)
        except TypeError:
            other(self)
        return self

    def _equal(self, other):
        raise TypeError(
            f"'==' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

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

    def _length(self):
        raise TypeError(
            f"'len' not supported between instances of '{self.__class__.__name__}'")

    def _getitem(self, index):
        raise TypeError(
            f"Indexation not supported between instances of '{self.__class__.__name__}'")

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

    def __len__(self):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: len(ssv))

    def __getitem__(self):
        return SearchSpace.SearchSpaceConditions(self, lambda ssv: len(ssv))

    def __hash__(self) -> int:
        return id(self)

    def __str__(self) -> str:
        DEBUG_SAMPLER = False
        v = self.get_sampler()
        DEBUG_SAMPLER = True
        return f'{self.__class__.__name__}: From {self.domain} to {self.__last_domain}, generate example sample {v}'
