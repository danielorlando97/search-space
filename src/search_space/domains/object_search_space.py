# try:
#     from ..abs_search_space import SearchSpace
#     from .numeral_search_space import NaturalNormalDistributeSampler, NaturalSearchSpace
#     from .categorical_search_space import CategoricalSearchSpace
# except (ModuleNotFoundError, ImportError):
from ..abs_search_space import SearchSpace
from .numeral_search_space import NaturalNormalDistributeSampler, NaturalSearchSpace
from .categorical_search_space import CategoricalSearchSpace


class ObjectSearchSpace(SearchSpace):
    def __init__(self) -> None:
        super().__init__({}, None)

    def _get_random_value(self, domain):
        sss = [(name, oss_property) for name, oss_property in self.__class__.__dict__.items() if isinstance(
            oss_property, SearchSpace)]

        value = {}
        for name, ss in sss:
            value[name] = ss.get_sampler()

        return value


class IndexOfList:
    def __init__(self, father=None, func=None) -> None:
        self.father = father
        self.func = func

    def __ge__(self, other):
        return IndexOfList(father=self, func=lambda i: i >= other)

    def __gt__(self, other):
        return IndexOfList(father=self, func=lambda i: i > other)

    def __le__(self, other):
        return IndexOfList(father=self, func=lambda i: i <= other)

    def __lt__(self, other):
        return IndexOfList(father=self, func=lambda i: i < other)

    def __ne__(self, other):
        return IndexOfList(father=self, func=lambda i: i != other)

    def __add__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i + other)

    def __sub__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i - other)

    def __mul__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i * other)

    def __div__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i / other)

    def __mod__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i % other)

    def __and__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i and other)

    def __or__(self, other):
        return IndexOfList(
            father=self, func=lambda i: i or other)

    def __hash__(self) -> int:
        return id(self)

    def __call__(self, index: int) -> None:
        if self.func is None:
            return index

        return self.func(self.father(index))


class ListSearchSpace(SearchSpace):
    def __init__(self, value_space_ctr, *args, len_distribute_like=NaturalNormalDistributeSampler(3, 100)) -> None:
        self.size = NaturalSearchSpace(
            distribute_like=len_distribute_like, log_name="List Size")
        self._value_space_ctr = value_space_ctr
        self._initials_args = args
        self._index_constraint = {}
        super().__init__(None, None)

    def _get_random_value(self, domain):
        len_ = self.size.get_sampler()

        index_conditions = dict(
            [(index, ss) for index, ss in self._index_constraint.items() if isinstance(index, IndexOfList)])
        result = [None] * len_

        for ss_index, ss in [(index, ss) for index, ss in self._index_constraint.items() if isinstance(index, SearchSpace)]:
            index = ss_index.get_sampler()
            result[index] = ss
            ss.scope = f'Value Index {index}'

        for i in range(len_):
            try:
                result[i] = self._index_constraint[i]
            except KeyError:
                result[i] = self._value_space_ctr(
                    *self._initials_args, log_name=f'Value Index {i}')

            for index, ss in index_conditions.items():
                if index(i):
                    result[i].constraint_list += ss.constraint_list

            result[i] = result[i].get_sampler()

        return result

    def __getitem__(self, index):
        if isinstance(index, SearchSpace):
            name = "Value Index Undefined"
        else:
            name = f"Value Index {index}"

        try:
            return self._index_constraint[index]
        except KeyError:
            self._index_constraint[index] = self._value_space_ctr(
                *self._initials_args, log_name=name)
        return self._index_constraint[index]

    def _length(self):
        return self._len

    def _getitem(self, index):
        try:
            index = index(IndexOfList())
            name = "FakeSearchSpace"
        except TypeError:
            index = index
            name = f"Value Index {index}"

        try:
            return self._index_constraint[index]
        except KeyError:
            self._index_constraint[index] = self._value_space_ctr(
                *self._initials_args, log_name=name)
        return self._index_constraint[index]


class MultiTypeSearchSpace(CategoricalSearchSpace):
    def __init__(self, domain) -> None:
        super().__init__(domain)

    def _get_random_value(self, domain):
        return super()._get_random_value(domain).get_sampler()
