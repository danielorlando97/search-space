from ..tools.singleton import Singleton


class Sampler:
    def __init__(self) -> None:
        self.history = {}
        self.__generate_new_sampler__ = True

    def generate_random_value(self, domain):
        pass

    def __random_value__(self, domain):
        if self.__generate_new_sampler__:
            self.__generate_new_sampler__ = False
            return self.__add_to_history__(domain, self.generate_random_value(domain))

        return self.history[domain][-1]

    def get_int(self, min, max):
        value = self.__random_value__(self, (min, max))
        decimal = value - int(value)
        return int(value) if decimal <= 0.5 else int(value) + 1

    def get_float(self, min, max):
        return self.__random_value__(self, (min, max))

    def choise(self, domain):
        index = self.get_int((0, len(domain)))
        return domain[index]

    def get_boolean(self, domain):
        value = self.__random_value__((0, 1))
        return True if value > 0.5 else False

    def __add_to_history__(self, domain, value):
        try:
            self.history[domain].push(value)
        except KeyError:
            self.history[domain] = [value]
        return value

    def _refresh(self):
        self.__generate_new_sampler__ = True


class SamplerFactory(metaclass=Singleton):
    def __init__(self) -> None:
        self.db = {}
        self.__instances = {}

    def registry_sampler(self, name, cclass):
        self.db[name] = cclass

    def create_new_sampler(self, search_space, distribute_name):
        try:
            return self.__instances[search_space]
        except KeyError:
            self.__instances[search_space] = self.db[distribute_name]()
            return self.__instances[search_space]

    def new_sample_generate(self):
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
