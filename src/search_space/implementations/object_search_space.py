from search_space.abstract_def import SearchSpace
from search_space.implementations.numeral_search_space import NaturalSearchSpace


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

    def __or__(self, func):
        return None


class ListSearchSpace(ObjectSearchSpace):
    size = NaturalSearchSpace()

    def __init__(self) -> None:
        super().__init__({}, None)

    def _get_random_value(self, domain):
        sss = [(name, oss_property) for name, oss_property in self.__dict__.items() if isinstance(
            oss_property, SearchSpace)]

        value = object()
        for name, ss in sss:
            value.__dict__[name] = ss.get_sampler()

        return value
