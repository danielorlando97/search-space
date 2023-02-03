from random import random, Random
from .factory import SamplerDataBase
from search_space.utils.infinity import check_slice_limits
from typing import Dict, List, Tuple, Any


class Distribution:
    def __init__(self, random_instance: Random, space_learning_rate=1) -> None:
        self.rand = random_instance
        self.space_learning_rate = space_learning_rate

    def alpha_param(self, learning_rate):
        return learning_rate * self.space_learning_rate

    def get_random_value(self, a, b):
        """This function should return an random value by the limits"""

    def choice_random_option(self, options) -> Tuple[int, Any]:
        """This function should return a random chosen index and its value"""

    def update(self, updates: List, learning_rate=1) -> 'Distribution':
        """
        This function should update the distribution's hyperparameters
        and return a new instance of the same class. This also should 
        to transform its parameter learning_rate by the function alpha_param
        """

    @staticmethod
    def create_new_instance(*args, **kwds):
        """By this function the user could create a default instance"""


class Sampler:

    def __init__(self, random_state: int = None):
        self.rand: Random = random.Random(random_state)

    def get_int(self, min, max):
        return self.rand.randint(min, max)

    def get_float(self, min, max):
        return self.rand.uniform(min, max)

    def choice(self, options):
        return self.rand.choice(options)

    def get_boolean(self):
        return self.rand.uniform(0, 1) < 0.5


class ModelSampler(Sampler):

    def __init__(self, model=None, random_state=0) -> None:
        super().__init__(random_state)

        self._model: Dict[str, Distribution] = {} if model is None else model
        self._updates: Dict[str, List] = {}
        self._db = SamplerDataBase()

    def register_space(self, space_name, distribution, *args, **kwd):
        self._model[space_name] = self._db.get_sampler(
            distribute_name=distribution,
            random_instance=self.rand,
            *args, **kwd
        )

    def __register_sample__(self, space_name, value):
        try:
            self._updates[space_name].append(value)
        except KeyError:
            self._updates[space_name] = [value]

        return value

    #################################################################
    #                                                               #
    #                   Randoms Functions                           #
    #                                                               #
    #################################################################

    @check_slice_limits
    def get_int(self, min, max, space_name=None):
        if space_name is None:
            return super().get_int(min, max)

        value = self._model[space_name].get_random_value(min, max)
        decimal = value - int(value)
        value = int(value) if decimal <= 0.5 else int(value) + 1

        return self.__register_sample__(space_name, value)

    @check_slice_limits
    def get_float(self, min, max, space_name=None):
        if space_name is None:
            return super().get_float(min, max)

        value = self._model[space_name].get_random_value(min, max)

        return self.__register_sample__(space_name, value)

    def choice(self, options, space_name=None):
        if space_name is None:
            return super().choice(options)

        idx, value = self._model[space_name].choice_random_option(options)
        self.__register_sample__(space_name, idx)

        return value

    def get_boolean(self, space_name=None):
        if space_name is None:
            return super().get_boolean()

        value = self._model[space_name].get_random_value(0, 1)
        value = 0 if value <= 0.5 else int(value) + 1

        return self.__register_sample__(space_name, value)

    #################################################################
    #                                                               #
    #                   Optimization                                #
    #                                                               #
    #################################################################

    @staticmethod
    def update_model(model: Dict, samples: List['ModelSampler'], learning_rate=1):

        # collect all of sample
        result = {}
        iterator = map(lambda x: x._updates, samples)
        for updates in iterator:
            for key, values in updates.items():
                try:
                    result[key].extend(values)
                except KeyError:
                    result[key] = values

        # update model
        new_model = {}

        for key, sampler in model.items():
            try:
                upd = result[key]
                new_model[key] = sampler.update(
                    upd, learning_rate=learning_rate)
            except KeyError:
                new_model[key] = sampler

        return new_model
