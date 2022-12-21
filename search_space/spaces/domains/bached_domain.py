from copy import copy
from typing import List
from search_space.context_manager.runtime_manager import SearchSpaceConfig
from search_space.errors import InvalidSpaceDefinition
from search_space.spaces.domains.__base__ import Domain
from search_space.sampler import Sampler
from search_space.sampler.distribution_names import UNIFORM
from . import __namespace__ as nsp
from search_space.spaces import domains


class BachedDomain(Domain, metaclass=nsp.BachedDomain):
    def __init__(self, *domains: List[Domain]) -> None:
        self.domains: List[Domain] = list(domains)
        self.sampler_selector: Sampler = None

    def extend(self, top):
        self.domains[-1].extend(top)

    def is_invalid(self):
        index = 0
        while index < len(self.domains):

            if self.domains[index].is_invalid():
                self.domains.pop(index)
            else:
                index += 1

        return len(self.domains) == 0

    @property
    def limits(self):
        self.is_invalid()
        return tuple([d.limits for d in self.domains])

    def get_sample(self, sampler: Sampler):
        if self.sampler_selector is None:
            self.sampler_selector = SearchSpaceConfig(
            ).sampler_manager.create_sampler(UNIFORM, self)
        bache = self.sampler_selector.choice(self.domains)
        return bache.get_sample(sampler)

    def __copy__(self):
        return BachedDomain(*[copy(d) for d in self.domains])

    def _propagation(self, f):
        new_space = []
        for domain in self.domains:
            try:
                domain = f(domain)

            except InvalidSpaceDefinition:
                continue

            if isinstance(domain, BachedDomain):
                new_space += [d for d in domain.domains if not d.is_invalid()]
            else:
                new_space.append(domain)

        self.domains = new_space

    def _find_bache(self, n):
        r, l = 0, len(self.domains)
        m = l + r >> 1

        while not n in self.domains[m] and r < l:
            _min, _max = self.domains[m].limits

            if n > _max:
                r = m + 1
            elif n < _min:
                l = m - 1

            m = l + r >> 1

        return m

    def __eq__(self, other):
        self._propagation(lambda x: x == other)
        return self

    def __ne__(self, other):
        # index = self._find_bache(other)
        # domain = self.domains[index] != other

        # if isinstance(domain, BachedDomain):
        #     self.domains = (
        #         self.domains[:index] +
        #         [d for d in domain.domains if not d.is_invalid()] +
        #         self.domains[index + 1:]
        #     )
        self._propagation(lambda x: x != other)

        return self

    def __lt__(self, other):
        self._propagation(lambda x: x < other)
        return self

    def __gt__(self, other):
        self._propagation(lambda x: x > other)
        return self

    def __ge__(self, other):
        self._propagation(lambda x: x >= other)
        return self

    def __le__(self, other):
        self._propagation(lambda x: x <= other)
        return self

    def __or__(self, __o):
        return self.domains.append(__o)

    def __hash__(self) -> int:
        return id(self)


class LogBachedDomain(BachedDomain, metaclass=nsp.LogBachedDomain):
    def __init__(self, *domains: List[Domain]) -> None:
        super().__init__(*domains)

    def __copy__(self):
        return LogBachedDomain(*[copy(d) for d in self.domains])

    def _find_bache(self, n):
        r, l = 0, len(self.domains)
        m = l + r >> 1

        while r < l and not n in self.domains[m]:
            _min, _max = self.domains[m].limits

            if n > _max:
                r = m + 1
            elif n < _min:
                l = m - 1

            m = l + r >> 1

        return m if m < len(self.domains) else len(self.domains) - 1

    def __eq__(self, other):
        index = self._find_bache(other)
        return self.domains[index] == other

    def __ne__(self, other):
        index = self._find_bache(other)
        domain = self.domains[index] != other

        if isinstance(domain, BachedDomain):
            self.domains = (
                self.domains[:index] +
                [d for d in domain.domains if not d.is_invalid()] +
                self.domains[index + 1:]
            )

        return self

    def __lt__(self, other):
        index = self._find_bache(other)
        self.domains = self.domains[:index] + [self.domains[index] < other]

        return self

    def __gt__(self, other):
        index = self._find_bache(other)
        self.domains = [self.domains[index] > other] + self.domains[index + 1:]
        return self

    def __ge__(self, other):
        index = self._find_bache(other)
        self.domains = [self.domains[index] >=
                        other] + self.domains[index + 1:]
        return self

    def __le__(self, other):
        index = self._find_bache(other)
        self.domains = self.domains[:index] + [self.domains[index] <= other]

        return self

    def __or__(self, __o):
        bd = BachedDomain(*self.domains) | __o
        bd.sample_selector = self.sampler_selector
        return bd

    def __hash__(self) -> int:
        return id(self)
