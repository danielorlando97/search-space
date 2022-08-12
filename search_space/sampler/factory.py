from search_space.utils.singleton import Singleton


class Sampler:
    def __init__(self) -> None:
        self.history = {}

    def generate_random_value(self, domain):
        pass

    def __random_value__(self, domain, repeat_last_value):
        if repeat_last_value:
            return self.history[domain][-1]

        return self.__add_to_history__(domain, self.generate_random_value(domain))

    def get_int(self, min, max, repeat_last_value=False):
        value = self.__random_value__(
            (min, max), repeat_last_value=repeat_last_value)
        decimal = value - int(value)
        return int(value) if decimal <= 0.5 else int(value) + 1

    def get_float(self, min, max, repeat_last_value=False):
        return self.__random_value__((min, max), repeat_last_value=repeat_last_value)

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
        return self.history[domain][-1]


class SamplerFactory(metaclass=Singleton):
    def __init__(self) -> None:
        self.db = {}
        self.__instances = {}

    def registry_sampler(self, name, cclass):
        self.db[name] = cclass

    def create_sampler(self, distribute_name, search_space=None):
        if search_space is None:
            return self.db[distribute_name]()

        try:
            return self.__instances[search_space]
        except KeyError:
            self.__instances[search_space] = self.db[distribute_name]()
            return self.__instances[search_space]

    def refresh_all_samplers(self):
        for sample in self.__instances.values():
            sample._refresh()

    def get_eval_feel_back(self, value):
        pass


def distribution(name=''):
    def f(classs):
        s = SamplerFactory()
        s.registry_sampler(name, classs)
        return classs

    return f
