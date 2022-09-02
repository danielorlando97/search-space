from .algebra_space import ast
from search_space.sampler import SamplerFactory, Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import InvalidSampler, NotEvaluateError
from .algebra_constraint.ast import AstRoot, SelfNode
from .algebra_constraint import visitors


class SearchSpace(ast.SelfNode):

    def __init__(self, initial_domain, distribute_like=UNIFORM) -> None:
        super().__init__()
        self._distribution: Sampler = SamplerFactory().create_sampler(
            distribute_like, search_space=self)
        self.initial_domain = initial_domain
        self.ast_constraint = AstRoot()

    def get_sample(self, context=None, local_domain=None):

        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        domain = self.initial_domain if local_domain is None else local_domain
        domain = self.__domain_filter__(domain, context)

        while True:
            sample = self.__sampler__(domain, context.create_child())
            try:
                self.__check_sample__(sample, context)

                context.registry_sampler(self, sample)
                return sample, context

            except InvalidSampler:
                pass

    def __domain_filter__(self, domain, context):
        """
        """
        return domain

    def __sampler__(self, domain, context):
        """
        """
        pass

    def __check_sample__(self, sample, context):
        visitors.ValidateSampler(context).visit(sample, self.ast_constraint)
        return sample

    def __ast_optimization__(self, ast_list):
        """
        """

        for func in ast_list:
            self.ast_constraint.add_constraint(func(SelfNode()))

    def __or__(self, other):
        """
        """
        if type(other) == type(tuple()):
            self.__ast_optimization__(other)
            return self
        if callable(other):
            self.__ast_optimization__([other])
            return self

        return super().__or__(self, other)

    def __hash__(self) -> int:
        return id(self)
