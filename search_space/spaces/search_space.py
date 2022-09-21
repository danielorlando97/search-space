from email.policy import default
from typing import List
from . import ast
from search_space.sampler import SamplerFactory, Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import DetectedRuntimeDependency, InvalidSampler, NotEvaluateError, CircularDependencyDetected, UndefinedSampler
from .algebra_constraint import ast as ast_constraint
from .algebra_constraint import ast_index as ast_index
from .algebra_constraint import visitors
from .algebra_constraint import VisitorLayer
import inspect


class BasicSearchSpace(ast.SelfNode):
    def __init__(self, initial_domain, distribute_like=UNIFORM, sampler=None) -> None:
        super().__init__()
        self.initial_domain = initial_domain
        self.__distribute_like__: str = distribute_like
        self._distribution: Sampler = SamplerFactory().create_sampler(
            self.__distribute_like__, self) if sampler is None else sampler

        self.visitor_layers: List[VisitorLayer] = [
            visitors.DomainModifierVisitor()]

    def change_distribution(self, distribution):
        self.__distribute_like__ = distribution
        self._distribution = SamplerFactory().create_sampler(
            self.__distribute_like__, self)

    def get_sample(self, context=None, local_domain=None):

        if not context is None:
            cache_value = context.get_sampler_value(self)
            if not cache_value is None:
                return cache_value, context
        else:
            context = SamplerContext()

        domain = self.initial_domain if local_domain is None else local_domain
        sample = self.__sampler__(domain, context)
        context.registry_sampler(self, sample)
        return sample, context

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)

    def __advance_space__(self, ast):
        return SearchSpace(
            domain=self.initial_domain,
            distribute_like=self.__distribute_like__,
            sampler=self._distribution,
            ast=ast
        )

    def __domain_optimization__(self, domain, ast_result):
        for visitor in reversed(self.visitor_layers):
            if not visitor.do_domain_optimization:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain
            ast_result, domain = visitor.domain_optimization(
                ast_result, domain)

        return domain, ast_result

    def __ast_optimization__(self, ast_list):
        """
        """

        if type(ast_list) == type(ast_constraint.AstRoot([])):
            ast = ast_list
        else:
            ast = ast_constraint.AstRoot([])

            if callable(ast_list):
                ast_list = [ast_list]

            temp_ast = ast_constraint.AstRoot([])
            for func in ast_list:
                new_ast = self.__build_constraint__(func)
                temp_ast.add_constraint(new_ast)

            for new_ast in temp_ast.asts:
                new_ast = ast_constraint.AstRoot([new_ast])
                try:
                    self.initial_domain, _ = self.__domain_optimization__(
                        self.initial_domain, new_ast)

                except DetectedRuntimeDependency:
                    ast.add_constraint(new_ast.asts)

        if len(ast.asts) > 0:
            return self.__advance_space__(ast)
        return self

    def __build_constraint__(self, func):

        func_data = inspect.getfullargspec(func)
        args = [ast_constraint.SelfNode()]

        defaults = [] if func_data.defaults is None else func_data.defaults

        args += [ast_index.SelfNode(i)
                 for i in range(len(func_data.args) - 1 - len(defaults))]

        args += [item.space for item in defaults]

        return func(*args)

    def __hash__(self) -> int:
        return id(self)


class SearchSpace(BasicSearchSpace):

    def __init__(self, domain, distribute_like, sampler, ast) -> None:
        super().__init__(domain, distribute_like, sampler)
        self.ast_constraint: ast_constraint.AstRoot = ast

    def get_sample(self, context=None, local_domain=None):

        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        precess_is_initialize = context.check_sampling_status(self)
        if not precess_is_initialize is None:
            raise CircularDependencyDetected(f'in {self.__class__.__name__}')
        context.registry_init_sampler_process(self)

        domain = self.initial_domain if local_domain is None else local_domain
        domain, ast_result = self.__domain_filter__(domain, context)

        while True:
            sample = self.__sampler__(domain, context.create_child())
            try:
                self.__check_sample__(sample, ast_result, context)

                context.registry_sampler(self, sample)
                return sample, context

            except InvalidSampler:
                pass

    def __domain_filter__(self, domain, context):
        ast_result = self.ast_constraint
        for visitor in reversed(self.visitor_layers):
            if not visitor.do_transform_to_modifier:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain

            ast_result, domain = visitor.transform_to_modifier(
                ast_result, domain, context)

        return domain, ast_result

    def __check_sample__(self, sample, ast_result, context):

        visitors.ValidateSampler().transform_to_check_sample(ast_result, sample, context)

        # ast_result = self.ast_constraint
        # for visitor in reversed(self.visitor_layers):
        #     if not visitor.do_transform_to_check_sample:
        #         continue
        #     # All visitors modifier the ast except the last one
        #     # The last one check if the sample is valid

        #     ast_result = visitor.transform_to_check_sample(
        #         ast_result, sample, context)

        # return sample

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self.ast_constraint.asts += ast.asts
        return self
