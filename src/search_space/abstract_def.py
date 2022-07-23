
from xml import dom


DEBUG_SAMPLER = True


class SearchSpace:
    def __init__(self, domain, distribute_like) -> None:
        self.__distribution = distribute_like
        self.domain = domain
        self.constraint_list = []
        self.cache = None

    def clean_cache(self):
        self.cache = None

    def get_sampler(self, local_domain=None):
        if not self.cache is None:
            return self.cache

        transformers = [c for c in self.constraint_list if c.is_transformer]
        conditions = [c for c in self.constraint_list if c.is_condition]

        domain = self.domain if local_domain is None else local_domain
        if DEBUG_SAMPLER:
            print(f'Init with domain {domain}')
        for c in transformers:
            domain = self._check_transform(c, domain)

        if DEBUG_SAMPLER:
            print(f'Transformed domain {domain}')
        while True:
            sample = self._get_random_value(domain)
            if DEBUG_SAMPLER:
                print(f'Check conditions by sampler {sample}')
            for c in conditions:
                if self._check_condition(c, sample):
                    break
            else:
                self.cache = sample
                return sample

    def _get_random_value(self, domain):
        return self.__distribution.get_random_value(domain)

    def _check_transform(self, constraint, domain):
        return constraint.transform(domain)

    def _check_condition(self, constraint, sample):
        return constraint.condition(sample)

    def __or__(self, func):
        func(self)
        return self

    def such_that(self, func):
        func(self)
        return self


class SearchSpaceConstraint:
    def __init__(self, value, search_space) -> None:
        self.value = value
        self.__ss = search_space

    def transform(self, domain):
        pass

    def check_condition(self, sampler):
        pass

    @property
    def target(self):
        return self.__ss

    @property
    def is_condition(self):
        return False

    @property
    def is_transformer(self):
        return False

    @property
    def is_context_sensitive(self):
        return isinstance(self.value, SearchSpace)

    @property
    def _real_value(self):
        if self.is_context_sensitive:
            return self.value.get_sampler()
        else:
            return self.value

    def depend_of(self, other):
        return self.value == other
