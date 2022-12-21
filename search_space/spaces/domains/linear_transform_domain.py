from copy import copy
from search_space.errors import InvalidSpaceDefinition
from search_space.spaces.domains.bached_domain import BachedDomain
from search_space.spaces.domains.__base__ import Domain, NumeralDomain
from search_space.sampler import Sampler
from search_space.sampler.distribution_names import UNIFORM
from . import __namespace__ as nsp
from typing import Iterable
from search_space.utils.itertools import is_iterable


class LinearTransformedDomain(Domain, metaclass=nsp.LinealTransformed):
    def __init__(
        self,
        original_domain: NumeralDomain,
        transformer, inverse, independent_value,
    ) -> None:
        self.original_domain = copy(original_domain)
        self.transformer = transformer
        self.inverse = inverse
        self.ind_v = independent_value

        self.original_domain.min = self._transform_origin_to_new(
            self.original_domain.min)
        self.original_domain.max = self._transform_origin_to_new(
            self.original_domain.max)

    def is_invalid(self):
        return self.original_domain.is_invalid()

    @property
    def limits(self):
        return self.original_domain.limits

    def _transform_origin_to_new(self, value):
        return self.transformer(value - self.ind_v)

    def _transform_new_to_origin(self, value):
        return self.inverse(value) + self.ind_v

    def _transform_values(self, values):
        if not is_iterable(values):
            return self._transform_origin_to_new(values)

        return [self._transform_origin_to_new(item) for item in values]

    def get_sample(self, sampler: Sampler):
        return self._transform_new_to_origin(self.original_domain.get_sample(sampler))

    def __eq__(self, __o: object) -> bool:
        self.original_domain = self.original_domain == self._transform_values(
            __o)
        return self

    def __ne__(self, __o: object) -> bool:
        self.original_domain = self.original_domain != self._transform_values(
            __o)
        return self

    def __lt__(self, __o: object) -> bool:
        self.original_domain = self.original_domain < self._transform_values(
            __o)
        return self

    def __le__(self, __o: object) -> bool:
        self.original_domain = self.original_domain <= self._transform_values(
            __o)
        return self

    def __ge__(self, __o: object) -> bool:
        self.original_domain = self.original_domain >= self._transform_values(
            __o)
        return self

    def __gt__(self, __o: object) -> bool:
        self.original_domain = self.original_domain > self._transform_values(
            __o)
        return self
