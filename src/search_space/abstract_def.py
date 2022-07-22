class SearchSpace:
    def __init__(self, domain, distribute_like) -> None:
        self.__distribution = distribute_like
        self.domain = domain
        self.constraint_list = []

    def get_sampler(self, verbose=False): 
        transformers = [c for c in self.constraint_list if c.is_transformer]
        conditions = [c for c in self.constraint_list if c.is_condition]

        domain = self.domain
        if verbose: print(f'Init with domain {domain}')
        for c in transformers:
            domain = c.transform(domain)
        
        if verbose: print(f'Transformed domain {domain}')
        while True:
            sample = self.__distribution.get_random_value(domain)
            if verbose: print(f'Check conditions by sampler {sample}')
            for c in conditions:
                if c.conditions(sample):
                    break
            else: 
                return sample
    
    def __or__(self, func):
        self.constraint_list = func(self)
        return self


class SearchSpaceConstraint:
    def __init__(self, value) -> None:
        self.value = value
    
    def transform(self, domain):
        pass

    def check_condition(self, sampler):
        pass

    @property
    def is_condition(self):
        return False

    @property
    def is_transformer(self):
        return False

    @property
    def is_context_sensitive(self):
        return issubclass(self.value, SearchSpace)
    
    @property
    def _real_value(self):
        return self.value
        if self.is_context_sensitive:
            return self.value.new_sampler
        else: self.value

