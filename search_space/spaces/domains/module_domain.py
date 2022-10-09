from copy import copy
from email.mime import base
from typing import Generic, List, TypeVar
from search_space.errors import InvalidSpaceDefinition
from search_space.spaces.domains.bached_domain import BachedDomain
from search_space.spaces.domains.domain_protocol import DomainProtocol, NumeralDomainProtocol
from search_space.sampler import Sampler, SamplerFactory
from search_space.sampler.distribution_names import UNIFORM

T = TypeVar('T')


class LinearTransformedDomain:
    def __init__(
        self,
        original_domain: NumeralDomainProtocol,
        transformer, inverse, independent_value=None,
        segmentation=False
    ) -> None:
        self.original_domain = copy(original_domain)
        self.transformer = transformer
        self.inverse = inverse
        self.ind_v = independent_value
        self._the_origin_domain_is_transformed = False
        self.segmentation = segmentation

    def _transform_origin_to_new(self, value):
        return self.transformer(value - self.ind_v)

    def _transform_new_to_origin(self, value):
        return self.inverse(value) + self.ind_v

    def _transform_values(self, values):
        if not type(values) in [list, tuple]:
            return self._transform_origin_to_new(values)

        return [self._transform_origin_to_new(item) for item in values]

    def _transformer(self):
        if self._the_origin_domain_is_transformed:
            return

        self._the_origin_domain_is_transformed = True
        if self.ind_v is None:
            self.ind_v = 0

        self.original_domain.min = self._transform_origin_to_new(
            self.original_domain.min)
        self.original_domain.max = self._transform_origin_to_new(
            self.original_domain.max)

    def get_sample(self, sampler: Sampler):
        self._transformer()
        return self._transform_new_to_origin(self.original_domain.get_sample(sampler))

    def __eq_seg__(self, other):
        other = [other] if not type(other) in [list, tuple] else copy(other)
        if self.ind_v is None:
            self.ind_v = other.pop(0)

        return BachedDomain(*([self] + [
            LinearTransformedDomain(
                self.original_domain,
                self.transformer,
                self.inverse,
                independent_value=plus,
                segmentation=True
            )
            for plus in other
        ]))

    def __eq__(self, other):

        if self.ind_v is None and not type(other) in [list, tuple]:
            self.ind_v = other
            return self

        if self.segmentation:
            return self.__eq_seg__(other)

        self.original_domain = self.original_domain == self._transform_values(
            other)

        return self

    def __neq_seg__(self, other):
        other = [other] if not type(other) in [list, tuple] else copy(other)
        if self.ind_v is None:
            self.ind_v = other.pop(0)

        return BachedDomain(*([self] + [
            LinearTransformedDomain(
                self.original_domain,
                self.transformer,
                self.inverse,
                independent_value=plus,
                segmentation=True
            )
            for plus in other
        ]))

    def __neq__(self, other):

        if self.segmentation:
            return self.__eq_seg__(other)

        self.original_domain = self.original_domain == self._transform_values(
            other)

        return self


class ModuleDomain(Generic[T]):
    def __init__(self, original_domain: NumeralDomainProtocol, factor, plus=None) -> None:
        self.original_domain = copy(original_domain)
        self.factor = factor
        self.plus = plus
        self._is_transformed_domain = False

    def _transform_back_to_origin(self, value):
        return value * self.factor + self.plus

    def _transform_func(self, value):
        return (value - self.plus) / self.factor

    def _transformer(self):
        if self._is_transformed_domain:
            return

        if self.plus is None:
            self.plus = 0

        self.original_domain.min = self._transform_func(
            self.original_domain.min)
        self.original_domain.max = self._transform_func(
            self.original_domain.max)

    def get_sample(self, sampler: Sampler) -> T:
        self._transformer()
        return self._transform_back_to_origin(self.original_domain.get_sample(sampler))

    def __copy__(self):
        return ModuleDomain(copy(self.original_domain), self.factor, self.plus)

    def __eq__(self, other):

        if self.plus is None and not type(other) in [list, tuple]:
            self.plus = other
            return self

        other = [other] if not type(other) in [list, tuple] else copy(other)
        if self.plus is None:
            self.plus = other.pop(0)

        return BachedDomain(*([self] + [
            ModuleDomain(self.original_domain, self.factor, plus)
            for plus in other
        ]))

    def __ne__(self, other):
        if not self.plus is None:
            try:
                if self.plus in other:
                    raise InvalidSpaceDefinition(
                        'contradictory description about rest of module')
            except TypeError:
                if self.plus == other:
                    raise InvalidSpaceDefinition(
                        'contradictory description about rest of module')

            return self

        other = [other] if not type(other) in [list, tuple] else other

        return BachedDomain(*[
            ModuleDomain(self.original_domain, self.factor, plus)
            for plus in range(self.factor) if not plus in other
        ])

    def _transform_values(self, values):
        if type(values) in [list, tuple]:
            return [self._transform_func(v) for v in values]

        return self._transform_func(values)

    def __lt__(self, other):
        self.original_domain = self.original_domain < self._transform_values(
            other)

        return self

    def __gt__(self, other):
        self.original_domain = self.original_domain > self._transform_values(
            other)

        return self

    def __ge__(self, other):
        self.original_domain = self.original_domain >= self._transform_values(
            other)

        return self

    def __le__(self, other):
        self.original_domain = self.original_domain <= self._transform_values(
            other)

        return self

    def __or__(self, __o):
        return BachedDomain(self, __o)
