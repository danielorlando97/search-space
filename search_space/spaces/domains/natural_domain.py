from search_space.errors import InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.spaces.domains.categorical_domain import CategoricalDomain
from search_space.spaces.domains.__base__ import NumeralDomain
from search_space.spaces.domains.linear_transform_domain import LinearTransformedDomain
from .bached_domain import BachedDomain, LogBachedDomain
from search_space.sampler import Sampler
from . import __namespace__ as nsp
from typing import Iterable
from search_space.utils.itertools import is_iterable


class NaturalDomain(NumeralDomain, metaclass=nsp.NaturalDomain):
    def __init__(self, _min, _max) -> None:
        self.min, self.max = _min, _max

    def __copy__(self):
        return NaturalDomain(self.min, self.max)

    def get_sample(self, sampler: Sampler):
        return sampler.get_int(self.min, self.max)

    @property
    def limits(self):
        return (self.min, self.max)

    #################################################################
    #                                                               #
    #                     List Operations                           #
    #                                                               #
    #################################################################

    def __getitem__(self, index):
        raise InvalidSpaceConstraint("Numeral value isn't indexed")

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    def __eq__(self, other):
        if is_iterable(other):
            return CategoricalDomain([item for item in other if self.min <= item and item <= self.max])

        if other > self.max or other < self.min:
            raise InvalidSpaceDefinition(
                f"{other} isn't intro the [{self.min}, {self.max}]")

        self.max = other
        self.min = other

        return self

    # def __ne__(self, other):
    #     if is_iterable(other):
    #         if len(other) == 0:
    #             return self
    #         other = [item for item in other if self.min <=
    #                  item and item <= self.max]

    #         other.sort()
    #         try:
    #             other = [other[0]] + [other[i] for i in range(1, len(other))
    #                                   if other[i] - other[i-1] > 0.51]

    #             while len(other) > 0 and self.min == other[0]:
    #                 other.pop(0)
    #                 self.min += 0.51

    #             while len(other) > 0 and self.max == other[-1]:
    #                 other.pop(-1)
    #                 self.max -= 0.51
    #         except IndexError:
    #             raise InvalidSpaceDefinition('NaturalDomain is empty')

    #         other = [self.min - 0.51] + other + [self.max + 0.51]
    #         return BachedDomain(
    #             * [NaturalDomain(other[i-1] + 0.51, other[i] - 0.51) for i in range(1, len(other))]
    #         )

    #     "If other is out of current domain, it will never enter and current domain is right"
    #     if other > self.max or other < self.min:
    #         return self

    #     return BachedDomain(NaturalDomain(self.min, other - 0.51), NaturalDomain(other + 0.51, self.max))

    def __ne__(self, other):
        """
        This operation don't have to computing in less than nlogn.
        Is the only way that we can create the correctly baches 
        """

        if not is_iterable(other):
            other = [other]

        other = [item for item in other
                 if self.min <= item and item <= self.max]
        other.sort()

        if len(other) == 0:
            return self

        if other[0] != self.min:
            other = [self.min - 0.51] + other
        if other[-1] != self.max:
            other = other + [self.max + 0.51]

        other = [other[0]] + [other[i] for i in range(1, len(other))
                              if abs(other[i] - other[i-1]) > 0.51]

        return LogBachedDomain(
            * [NaturalDomain(other[i-1] + 0.51, other[i] - 0.51) for i in range(1, len(other))]
        )

    def __lt__(self, other):
        if is_iterable(other):
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other - 0.51, self.max)
        return self

    def __gt__(self, other):
        if is_iterable(other):
            other = max(other)

        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other + 0.51, self.min)
        return self

    def __rlt__(self, other):
        return self.__gt__(other)

    def __rgt__(self, other):
        return self.__lt__(other)

    def __ge__(self, other):
        if is_iterable(other):
            other = max(other)

        if self.max < other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are less that {other}")

        self.min = max(other, self.min)
        return self

    def __le__(self, other):
        if is_iterable(other):
            other = min(other)

        if self.min > other:
            raise InvalidSpaceDefinition(
                f"All values intro [{self.min}, {self.max}] are graters that {other}")

        self.max = min(other, self.max)
        return self

    def __or__(self, __o):
        return BachedDomain(self, __o)

    def _get_range(self, factor):
        if factor < 0:
            return (factor, -factor)

        return (-factor, factor)

    def __mod_eq__(self, factor, value):
        sing = factor/abs(factor)
        if is_iterable(value):

            _range = self._get_range(factor)
            value = [i for i in value if _range[0] < i and i < _range[1]]

            return nsp.New[nsp.BachedDomain](
                * [nsp.New[nsp.LinealTransformed](
                    original_domain=self,
                    transformer=lambda x: x/abs(factor),
                    inverse=lambda x: x * factor,
                    independent_value=ind * sing
                ) for ind in value]
            )

        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x/abs(factor),
            inverse=lambda x: x * factor,
            independent_value=value
        )

    def __mod_neq__(self, factor, value):
        if not is_iterable(value):
            value = [value]

        value = [abs(v) for v in value]

        return nsp.New[nsp.BachedDomain](
            * [nsp.New[nsp.LinealTransformed](
                original_domain=self,
                transformer=lambda x: x/abs(factor),
                inverse=lambda x: x * factor,
                independent_value=ind
            ) for ind in range(*self._get_range(factor))
                if not abs(ind) in value
            ]
        )

    def __mod_lt__(self, factor, value):
        if is_iterable(value):
            value = min([abs(v) for v in value])

        return nsp.New[nsp.BachedDomain](
            * [nsp.New[nsp.LinealTransformed](
                original_domain=self,
                transformer=lambda x: x/factor,
                inverse=lambda x: x * factor,
                independent_value=ind
            ) for ind in range(*self._get_range(factor)) if abs(ind) < value]
        )

    def __mod_gt__(self, factor, value):
        if is_iterable(value):
            value = max([abs(v) for v in value])

        return nsp.New[nsp.BachedDomain](
            * [nsp.New[nsp.LinealTransformed](
                original_domain=self,
                transformer=lambda x: x/factor,
                inverse=lambda x: x * factor,
                independent_value=ind
            ) for ind in range(*self._get_range(factor)) if abs(ind) > value]
        )

    def __mod_ge__(self, factor, value):
        if is_iterable(value):
            value = max([abs(v) for v in value])

        return nsp.New[nsp.BachedDomain](
            * [nsp.New[nsp.LinealTransformed](
                original_domain=self,
                transformer=lambda x: x/factor,
                inverse=lambda x: x * factor,
                independent_value=ind
            ) for ind in range(*self._get_range(factor)) if abs(ind) >= value]
        )

    def __mod_le__(self, factor, value):
        if is_iterable(value):
            value = min([abs(v) for v in value])

        return nsp.New[nsp.BachedDomain](
            * [nsp.New[nsp.LinealTransformed](
                original_domain=self,
                transformer=lambda x: x/factor,
                inverse=lambda x: x * factor,
                independent_value=ind
            ) for ind in range(*self._get_range(factor)) if abs(ind) <= value]
        )
