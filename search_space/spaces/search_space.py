from copy import copy
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

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, initial_domain, distribute_like=UNIFORM, sampler=None) -> None:
        super().__init__()
        self.initial_domain = initial_domain
        self.__distribute_like__: str = distribute_like
        self._distribution: Sampler = SamplerFactory().create_sampler(
            self.__distribute_like__, self) if sampler is None else sampler

        self.visitor_layers: List[VisitorLayer] = [
            visitors.DomainModifierVisitor()]

        self._clean_asts = ast_constraint.AstRoot([])

    def change_distribution(self, distribution):
        self.__distribute_like__ = distribution
        self._distribution = SamplerFactory().create_sampler(
            self.__distribute_like__, self)

    def __hash__(self) -> int:
        return id(self)

    def __copy__(self):
        return type(self)(*self.initial_domain.limits, distribute_like=self.__distribute_like__)

    #################################################################
    #                                                               #
    #                     Ast Optimization                          #
    #                                                               #
    #################################################################

    def __ast_optimization__(self, ast_list):
        """
        """

        ast = ast_constraint.AstRoot([])

        if type(ast_list) == type(ast_constraint.AstRoot([])):
            temp_ast = ast_list
        else:

            if callable(ast_list):
                ast_list = [ast_list]

            temp_ast = ast_constraint.AstRoot([])
            for func in ast_list:
                new_ast = self.__build_constraint__(func)
                temp_ast.add_constraint(new_ast)

        for new_ast in temp_ast.asts:
            opt_ast = ast_constraint.AstRoot([new_ast])
            new_ast = ast_constraint.AstRoot([new_ast])
            try:
                for _domain, _ast in self.__domain_optimization__(self.initial_domain, new_ast):
                    self.initial_domain, opt_ast = _domain, _ast
                self._clean_asts.add_constraint(opt_ast.asts)
            except DetectedRuntimeDependency:
                ast.add_constraint(opt_ast.asts)
            except NotEvaluateError:
                pass

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

    def __domain_optimization__(self, domain, ast_result):
        for visitor in reversed(self.visitor_layers):
            if not visitor.do_domain_optimization:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain
            ast_result, domain = visitor.domain_optimization(
                ast_result, domain)

            yield domain, ast_result

    def __advance_space__(self, ast):
        return SearchSpace(
            domain=self.initial_domain,
            distribute_like=self.__distribute_like__,
            sampler=self._distribution,
            ast=ast,
            clean_asts=self._clean_asts
        )

    #################################################################
    #                                                               #
    #                     Sample Generate                           #
    #                                                               #
    #################################################################

    def get_sample(self, context=None, local_domain=None):

        if not context is None:
            cache_value = context.get_sampler_value(self)
            if not cache_value is None:
                return cache_value, context

            precess_is_initialize = context.check_sampling_status(self)
            if not precess_is_initialize is None:
                raise CircularDependencyDetected(
                    f'in {self.__class__.__name__}')
        else:
            context = SamplerContext()

        context.registry_init_sampler_process(self)

        domain = self.initial_domain if local_domain is None else local_domain
        domain, ast_result = self.__domain_filter__(domain, context)

        while True:
            sample = self.__sampler__(domain, context)
            try:
                self.__check_sample__(sample, ast_result, context)

                context.registry_sampler(self, sample)
                return sample, context

            except InvalidSampler as e:
                pass

    def __domain_filter__(self, domain, context):
        return domain, self._clean_asts

    def __sampler__(self, domain, context):
        return domain.get_sample(self._distribution)

    def __check_sample__(self, sample, ast_result, context):
        visitors.ValidateSampler().transform_to_check_sample(ast_result, sample, context)


class SearchSpace(BasicSearchSpace):

    def __init__(self, domain, distribute_like, sampler, ast, clean_asts) -> None:
        super().__init__(domain, distribute_like, sampler)
        self.ast_constraint: ast_constraint.AstRoot = ast
        self._clean_asts: ast_constraint.AstRoot = clean_asts

    def __domain_filter__(self, domain, context):
        domain = copy(domain)
        ast_result = self.ast_constraint
        for visitor in reversed(self.visitor_layers):
            if not visitor.do_transform_to_modifier:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain

            ast_result, domain = visitor.transform_to_modifier(
                ast_result, domain, context)

        return domain, ast_result + self._clean_asts

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self.ast_constraint.asts += ast.asts
        return self

    def __copy__(self):
        return type(self)(
            self.initial_domain,
            self.__distribute_like__,
            sampler=None,
            ast=self.ast_constraint,
            clean_asts=self._clean_asts
        )
