from ..context_manager.sampler_context import ConstraintInfo, SamplerInfo
from search_space.sampler import SamplerFactory, Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext


class SearchSpace:
    def __init__(self, domain, distribute_like=UNIFORM, log_name=None) -> None:
        self._distribution: Sampler = SamplerFactory().create_sampler(
            distribute_like, search_space=self)
        self.domain = domain
        self.constraint_list = []
        self.scope = log_name if not log_name is None else self.__class__.__name__

    def get_sampler(self, local_domain=None, context: SamplerContext = None):
        """
            This method generate a new sampler by SearchSpace's domain and config
            This sample is unique for each instance of ContextManager
            It divide the constraint list in transforms list and conditional list
            The transforms are constraints that modification the SearchSpace's domain like <= (this reduce the domain)
            The conditionals are constraints that only can check before to generate the sampler like %2 == 0
        """
        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        transformers = [c for c in self.constraint_list if c.is_transformer]
        conditions = [c for c in self.constraint_list if c.is_condition]

        domain = self.domain if local_domain is None else local_domain

        for c in transformers:
            domain = self._check_transform(c, domain, context)

        self.__last_domain = domain
        while True:
            sample = self._get_random_value(domain)
            for c in conditions:
                if not self._check_condition(c, sample, context):
                    break
            else:
                context.registry_sampler(self, sample)
                context.push_log(SamplerInfo(
                    self.scope, domain, self._distribution.last_value(domain), sample))
                return sample, context

    def _get_random_value(self, domain):
        """
            For default, this method generate a new random value intro the domain
            In the inherence, each class can do override it to change the types and form
            to generate new values
            for example: the categorical Search Space override it to get the random index
            and sample the category with that index
        """
        pass

    def _check_transform(self, constraint, domain, context: SamplerContext):
        """
        """
        result = constraint.transform(domain, context)
        context.push_log(ConstraintInfo(
            self.scope, constraint.__class__.__name__, domain, result))
        return result

    def _check_condition(self, constraint, sample, context: SamplerContext):
        """
        """

        result = constraint.check_condition(sample, context)
        context.push_log(ConstraintInfo(
            self.scope, constraint.__class__.__name__, sample, result))
        return result

    def __or__(self, other):
        try:
            for f in other:
                f(self)
        except TypeError:
            other(self)
        return self

    def _equal(self, other):
        raise TypeError(
            f"'==' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _great_equal(self, other):
        raise TypeError(
            f"'>=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _great(self, other):
        raise TypeError(
            f"'>' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _less_equal(self, other):
        raise TypeError(
            f"'<=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _less(self, other):
        raise TypeError(
            f"'<' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _not_equal(self, other):
        raise TypeError(
            f"'!=' not supported between instances of '{self.__class__.__name__}' and '{type(other).__name__}' ")

    def _length(self):
        raise TypeError(
            f"'len' not supported between instances of '{self.__class__.__name__}'")

    def _getitem(self, index):
        raise TypeError(
            f"Indexation not supported between instances of '{self.__class__.__name__}'")
