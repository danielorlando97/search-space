from .algebra_space import ast
from search_space.sampler import SamplerFactory, Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import InvalidSampler, NotEvaluateError, CircularDependencyDetected
from .algebra_constraint.ast import AstRoot, SelfNode
from .algebra_constraint import visitors


class SearchSpace(ast.SelfNode):

    def __init__(self, initial_domain, distribute_like=UNIFORM) -> None:
        super().__init__()
        self._distribution: Sampler = SamplerFactory().create_sampler(
            distribute_like, search_space=self)
        self.initial_domain = initial_domain
        self.__distribute_like = distribute_like
        self.ast_constraint = AstRoot()

    def get_sample(self, context=None, local_domain=None):

        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        precess_is_initialize = context.check_sampling_status(self)
        if not precess_is_initialize is None:
            raise CircularDependencyDetected(f'in {self.__class__.__name__}')
        context.registry_init_sampler_process(self)

        return self.__get_sample__(context, local_domain)

    def __get_sample__(self, context=None, local_domain=None):

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
            self.ast_constraint.add_constraint(self.__build_constraint__(func))

        return self

    def __build_constraint__(self, func):
        return func(SelfNode())

    def __or__(self, other):
        """
        """
        if type(other) == type(tuple()):
            return self.__ast_optimization__(other)
        if callable(other):
            return self.__ast_optimization__([other])
        if type(other) == type(AstRoot()):
            self.ast_constraint = other
            return self

        return super().__or__(self, other)

    def __hash__(self) -> int:
        return id(self)
