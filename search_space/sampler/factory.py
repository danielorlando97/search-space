from search_space.utils.singleton import Singleton
from search_space.utils.infinity import Infinity


class Sampler:
    def __init__(self) -> None:
        self.history = {}

    def _get_true_range(self, a, b):
        if not Infinity in [type(a), type(b)]:
            return a, b

        if type(a) == Infinity and type(b) == Infinity:
            return float(a), float(b)

        if type(a) != Infinity:
            m = float(b)
            return (a, m) if a < m else (a, a*2)

        if type(b) != Infinity:
            m = float(a)
            return (m, b) if (m < b and abs(m) - abs(b) > 1) else (- abs(2*b), b)

    def generate_random_value(self, domain):
        pass

    def __random_value__(self, domain, repeat_last_value):
        if repeat_last_value:
            return self.history[domain][-1]

        return self.__add_to_history__(domain, self.generate_random_value(domain))

    def get_int(self, min, max, repeat_last_value=False):
        value = self.__random_value__(
            self._get_true_range(min, max), repeat_last_value=repeat_last_value)
        decimal = value - int(value)
        return int(value) if decimal <= 0.5 else int(value) + 1

    def get_float(self, min, max, repeat_last_value=False):
        return self.__random_value__(self._get_true_range(min, max), repeat_last_value=repeat_last_value)

    def choice(self, domain, repeat_last_value=False):
        index = self.get_int(
            0, len(domain) - 1, repeat_last_value=repeat_last_value)

        return domain[index]

    def get_boolean(self, domain=(0, 1), repeat_last_value=False):
        value = self.__random_value__(
            domain, repeat_last_value=repeat_last_value)
        return True if value > 0.5 else False

    def __add_to_history__(self, domain, value):
        try:
            self.history[domain].append(value)
        except KeyError:
            self.history[domain] = [value]
        return value

    def last_value(self, domain):
        if type(domain) == type(list()):
            domain = (0, len(domain) - 1)

        return self.history[domain][-1]


class SamplerDataBase(metaclass=Singleton):
    def __init__(self) -> None:
        self.db = {}

    def registry_sampler(self, name, cclass):
        self.db[name] = cclass

    def get_sampler(self, distribute_name):
        try:
            return self.db[distribute_name]()
        except:
            return None


class SamplerFactory:
    def __init__(self) -> None:
        self.db = SamplerDataBase()

    def create_sampler(self, distribute_name, search_space=None):
        return self.db.get_sampler(distribute_name)


class SamplerFactoryWithMemory(SamplerFactory):
    def __init__(self) -> None:
        super().__init__()
        self.__instances = {}

    def create_sampler(self, distribute_name, search_space=None):
        if distribute_name is None:
            return None

        if search_space is None:
            return self.db.get_sampler(distribute_name)

        try:
            return self.__instances[(search_space, distribute_name)]
        except KeyError:
            self.__instances[(search_space, distribute_name)
                             ] = self.db.get_sampler(distribute_name)

            return self.__instances[(search_space, distribute_name)]

    def refresh_all_samplers(self):
        for sample in self.__instances.values():
            sample._refresh()


def distribution(name=''):
    def f(classs):
        s = SamplerDataBase()
        s.registry_sampler(name, classs)
        classs.__distribute_name__ = name
        return classs

    return f
