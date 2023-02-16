from .factory import distribution, SamplerDataBase
from .model_sampler import Distribution
from statistics import mean, stdev
from typing import List, Dict, Hashable, Iterable


class SelectDistributionError(Exception):
    pass


NORMAL = 'Normal'


@distribution(NORMAL)
class NormalDistribution(Distribution):
    def __init__(self, mean: float, dev: float, *args, **kwds) -> None:
        super().__init__(*args, **kwds)

        self.mean = mean
        self.dev = dev
        self.initial_values = (args, kwds)

    @staticmethod
    def create_new_instance(domain: List, *args, **kwds):
        if len(domain) == 2:
            min, max = domain
        else:
            min, max = 0, len(domain)

        return NormalDistribution(
            mean=(min + max) / 2,
            dev=(max - min),
            *args, **kwds
        )

    def choice_random_option(self, options):
        idx = self.get_random_value(0, len(options) - 1)

        return idx, options[int(idx)]

    def get_random_value(self, a, b):
        x = self.rand.gauss(self.mean, self.dev)

        # BUG: to show
        if x < a or x > b:
            return self.rand.uniform(a, b)

        # if x < a:
        #     return a
        # if x > b:
        #     return b
        return x

    def update(self, updates: List, learning_rate=1) -> 'Distribution':
        new_mean = mean(updates)
        new_dev = stdev(updates, new_mean) if len(updates) > 1 else 0
        alpha = self.alpha_param(learning_rate)
        args, kwds = self.initial_values

        return NormalDistribution(
            mean=self.mean * (1 - alpha) + new_mean * alpha,
            dev=self.dev * (1 - alpha) + new_dev * alpha,
            *args, **kwds
        )

    def segmentation(self, domain, *args, **kwds) -> 'Distribution':
        if len(domain) == 2:
            _min, _max = domain
        else:
            _min, _max = 0, len(domain)

        mean = self.mean if _min <= self.mean and self.mean <= _max else (
            _max + _min)/2
        dev = min(self.dev, (_max - _min))

        return NormalDistribution(
            mean=mean, dev=dev, *args, **kwds
        )


BERNOULLI = 'Bernoulli'


@distribution(BERNOULLI)
class BernoulliDistribution(Distribution):
    def __init__(self, df: Dict[Hashable, float], *args, **kwds) -> None:
        super().__init__(*args, **kwds)

        self.df = df
        self.initial_values = (args, kwds)

    @staticmethod
    def create_new_instance(domain: List, *args, **kwds):
        df = {}
        for op in domain:
            try:
                df[op.tag] = 1
            except AttributeError:
                df[op] = 1

        return BernoulliDistribution(
            df=df,
            *args, **kwds
        )

    def get_random_value(self, a, b):
        raise SelectDistributionError(
            "The bernoulli distribution can't generate a random number into a subset"
        )

    def find_option(self, option):
        try:
            option = option.tag
        except AttributeError:
            pass

        try:
            return self.df[option]
        except KeyError:
            # The only case when into the options there are
            # an options that it wasn't at first time
            # is when a domain has been segmented.
            # In that case there is only one option,
            # a delimited domain has been divide in two half.
            # So, Let's x =(y, z) the new option, into old options
            # there is either (y, _) or (_, z)

            y, z = option
            old_option = next(filter(
                lambda x: len(x) == 2 and (x[0] == y or x[1] == z),
                self.df.keys()
            ))

            self.df[option] = self.df[old_option]
            return self.df[option]

    def choice_random_option(self, options):
        weighs = [self.find_option(op) for op in options]
        weighs = [x/sum(weighs) for x in weighs]

        value = self.rand.choices(options, weights=weighs, k=1)

        return value[0], value[0]

    def update(self, updates: List, learning_rate=1) -> 'Distribution':
        weighs = dict(self.df)
        args, kwd = self.initial_values

        for key in updates:
            # Here, use the learning_rate because
            # sometimes I don't use all of value in the domain
            # and it's good that the learning isn't very big
            # because when I use all of domain the different
            # between values that I already have used it and I haven't yet
            # don't is very big
            weighs[key] += learning_rate

        return BernoulliDistribution(
            df=weighs, *args, **kwd
        )


BOOLEAN_BERNOULLI = 'Boolean_Bernoulli'


@distribution(BOOLEAN_BERNOULLI)
class BooleanBernoulliDistribution(Distribution):
    def __init__(self, p, *args, **kwds) -> None:
        super().__init__(*args, **kwds)

        self.p = p
        self.initial_values = (args, kwds)

    @staticmethod
    def create_new_instance(domain, *args, **kwds):
        return BooleanBernoulliDistribution(
            p=0.5, *args, **kwds
        )

    def get_random_value(self, a=0, b=1):
        if self.rand.uniform(0, 1) < self.p:
            return a
        return b

    def choice_random_option(self, options):
        assert len(options) == 2

        idx = self.get_random_value()
        return idx, options[idx]

    def update(self, updates: List, learning_rate=1) -> 'Distribution':
        alpha = self.alpha_param(learning_rate)
        args, kwd = self.initial_values
        p = p * (1 - alpha) + mean(updates) * alpha

        return BooleanBernoulliDistribution(p, *args, **kwd)
