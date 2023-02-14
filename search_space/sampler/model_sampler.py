from random import random, Random
from .factory import SamplerDataBase
from search_space.utils.infinity import check_slice_limits
from typing import Dict, List, Tuple, Any, Union
from search_space.context_manager.runtime_manager import SearchSpaceConfig
from abc import abstractmethod, ABC
from collections import defaultdict


class Distribution(ABC):
    def __init__(self, random_instance: Random, space_learning_rate=1) -> None:
        self.rand = random_instance
        self.space_learning_rate = space_learning_rate

    def alpha_param(self, learning_rate):
        return learning_rate * self.space_learning_rate

    @abstractmethod
    def get_random_value(self, a, b):
        """This function should return an random value by the limits"""

    @abstractmethod
    def choice_random_option(self, options) -> Tuple[int, Any]:
        """This function should return a random chosen index and its value"""

    @abstractmethod
    def update(self, updates: List, learning_rate=1) -> 'Distribution':
        """
        This function should update the distribution's hyperparameters
        and return a new instance of the same class. This also should 
        to transform its parameter learning_rate by the function alpha_param
        """

    # The dynamic segmentation is only in the numerical domains.
    # In categorical domains we only drop unfeasible options
    def segmentation(self, domain, *args, **kwds) -> 'Distribution':
        """
        This function should check the conditions of the segmentation and
        create the best distribution for the new segment. 
        """

        return self.__class__.create_new_instance(domain, *args, **kwds)

    @staticmethod
    @abstractmethod
    def create_new_instance(domain, *args, **kwds):
        """By this function the user could create a default instance"""


class Sampler:

    def __init__(self):
        self.rand: Random = SearchSpaceConfig().random_instance

    def get_int(self, min, max):
        return self.rand.randint(min, max)

    def get_float(self, min, max):
        return self.rand.uniform(min, max)

    def choice(self, options):
        return self.rand.choice(options)

    def get_boolean(self):
        return self.rand.uniform(0, 1) < 0.5


class ModelSampler(Sampler):

    def __init__(self, model=None) -> None:
        super().__init__()

        self._model: Dict[str, Dict[Union[str, tuple], Distribution]] = defaultdict(
            dict) if model is None else model
        self._updates: Dict[str, Dict[Union[str, tuple], List]
                            ] = defaultdict(lambda: defaultdict(list))
        self._db = SamplerDataBase()

    def __get_sampler(
        self,
        domain,  # This param should send when a domain class ask a random value
        # This param should send when a domain is segmented
        tag: Union[str, tuple] = '',

        # Other next params are space informations and
        # They are from the class SearchSpace, from its SpaceInfo params
        path_space=None,
        distribution=None,
        learning_rate=1,
        check_segmentation=False
    ):

        if path_space is None:
            return None, None

        section = self._model[path_space]

        if not tag in section:
            if check_segmentation:
                # If these conditions are true, it means that
                # Some subdomain has been segmented dynamically.
                # It also means that tag is like (a, b) and into
                # section there should be a tag like (a, x) or (y, b)

                previous_domains = [
                    (abs(x[1] - x[0]), x) for x in section.keys()
                    if type(x) == tuple and (x[0] == tag[0] or x[1] == tag[1])
                ]

                if any(previous_domains):
                    _, base = min(previous_domains)

                    section[tag] = section[base].segmentation(
                        domain=tag,
                        random_instance=self.rand,
                        space_learning_rate=learning_rate,
                    )

                    return section[tag], (path_space, tag)

            section[tag] = self._db.get_sampler(
                distribute_name=distribution,
                random_instance=self.rand,
                space_learning_rate=learning_rate,
                domain=domain,
            )

        return section[tag], (path_space, tag)

    def __register_sample__(self, path, value):
        (space_name, tag) = path
        self._updates[space_name][tag].append(value)
        return value

    #################################################################
    #                                                               #
    #                   Randoms Functions                           #
    #                                                               #
    #################################################################

    @check_slice_limits
    def get_int(self, min, max, **kwd):
        model, model_key = self.__get_sampler(
            domain=(min, max), check_segmentation=True, **kwd
        )

        if model is None:
            return super().get_int(min, max)

        value = model.get_random_value(min, max)
        decimal = value - int(value)
        value = int(value) if decimal <= 0.5 else int(value) + 1

        return self.__register_sample__(model_key, value)

    @check_slice_limits
    def get_float(self, min, max, **kwd):
        model, model_key = self.__get_sampler(
            domain=(min, max), check_segmentation=True, **kwd
        )

        if model is None:
            return super().get_float(min, max)

        value = model.get_random_value(min, max)

        return self.__register_sample__(model_key, value)

    def choice(self, options, **kwd):
        model, model_key = self.__get_sampler(domain=options, **kwd)

        if model is None:
            return super().choice(options)

        idx, value = model.choice_random_option(options)
        self.__register_sample__(model_key, idx)

        return value

    def get_boolean(self, **kwd):
        model, model_key = self.__get_sampler(domain=None, **kwd)
        if model is None:
            return super().get_boolean()

        value = model.get_random_value(0, 1)
        value = 0 if value <= 0.5 else int(value) + 1

        return self.__register_sample__(model_key, value)

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
