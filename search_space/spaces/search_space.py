from copy import copy
from distutils.command.config import config
from typing import List

from search_space.context_manager.runtime_manager import SearchSpaceConfig
from search_space.sampler import Sampler
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import ArgumentFunctionError, DetectedRuntimeDependency, InvalidSampler, InvalidSpaceConstraint, InvalidSpaceDefinition, NotEvaluateError, CircularDependencyDetected, UndefinedSampler
from .asts import constraints as ast_constraint
from .asts import naturals_values as ast_natural
from .visitors import visitors
from .visitors import VisitorLayer
from .printer_tools.default_printer_class import DefaultPrinter

import inspect


class BasicSearchSpace:

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, initial_domain, distribute_like=UNIFORM, sampler=None, name=None) -> None:
        # super().__init__()
        self.initial_domain = initial_domain
        self.__distribute_like__: str = distribute_like

        self.visitor_layers: List[VisitorLayer] = [
            visitors.DomainModifierVisitor()]
        self._inner_hash = None
        self._clean_asts = ast_constraint.AstRoot([])
        self.space_name = self.__class__.__name__ if name is None else name

        self._distribution: Sampler = SearchSpaceConfig().sampler_manager.create_sampler(
            self.__distribute_like__, self) if sampler is None else sampler

    def change_distribution(self, distribution):
        self.__distribute_like__ = distribution
        self._distribution = SearchSpaceConfig().sampler_manager.create_sampler(
            self.__distribute_like__, self)

    def layers_append(self, *args):
        self.visitor_layers += list(args)

    def set_hash(self, v):
        self._inner_hash = v

    def __hash__(self) -> int:
        if self._inner_hash is None:
            return id(self)

        return self._inner_hash

    def __copy__(self):
        try:
            domain = self.initial_domain.limits

        except AttributeError:
            domain = self.initial_domain,

        result = type(self)(
            *domain, distribute_like=self.__distribute_like__)
        result.initial_domain = copy(self.initial_domain)
        result.space_name = f"{result.space_name}'"
        result.visitor_layers = [item for item in self.visitor_layers]
        result._clean_asts.add_constraint(self._clean_asts.asts)
        return result

    #################################################################
    #                                                               #
    #                     Ast Optimization                          #
    #                                                               #
    #################################################################

    def __ast_optimization__(self, ast_list):
        """
        """

        ast = ast_constraint.AstRoot([])

        if type(ast_list) == type(ast):
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
            except ArgumentFunctionError:
                self._clean_asts.add_constraint(opt_ast.asts)

        if len(ast.asts) > 0:
            return self.__advance_space__(ast)
        return self

    def __build_constraint__(self, func):

        func_data = inspect.getfullargspec(func)
        args = [ast_constraint.SelfNode()]

        defaults = [] if func_data.defaults is None else func_data.defaults

        args += [ast_natural.IndexSelf(i)
                 for i in range(len(func_data.args) - 1 - len(defaults))]

        args += [ast_natural.SpaceSelfNode(item.space) for item in defaults]

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
        ss = SearchSpace(
            domain=self.initial_domain,
            distribute_like=self.__distribute_like__,
            sampler=self._distribution,
            ast=ast,
            clean_asts=self._clean_asts,
            layers=self.visitor_layers,
        )
        ss.space_name = self.space_name
        ss.set_hash(hash(self))
        return ss

    #################################################################
    #                                                               #
    #                     Sample Generate                           #
    #                                                               #
    #################################################################

    def get_sample(self, context=None, local_domain=None):
        config = SearchSpaceConfig(printer=DefaultPrinter())
        printer = config.printer_class

        printer.init_search(hash(self), self.space_name)

        if not context is None:
            cache_value = context.get_sampler_value(self)
            if not cache_value is None:
                printer.sample_value(cache_value, True)
                return cache_value, context

            precess_is_initialize = context.check_sampling_status(self)
            if not precess_is_initialize is None:
                raise CircularDependencyDetected(
                    f'in {self.__class__.__name__}')
        else:
            context = SamplerContext(self.space_name)

        context.registry_init_sampler_process(self)
        printer.context_name(context)

        domain = self.initial_domain if local_domain is None else local_domain
        printer.domain_init(domain)

        printer.tabs += 1
        domain, ast_result = self.__domain_filter__(domain, context)
        printer.tabs -= 1

        sample_index = 0
        while True:

            printer.tabs += 1
            sample, sample_context = self.__sampler__(domain, context)
            printer.tabs -= 1

            try:
                self.__check_sample__(sample, ast_result, sample_context)

                context.registry_sampler(self, sample)
                printer.sample_value(sample)
                return sample, context

            except InvalidSampler as e:
                if not config.replay_nums is None and config.replay_nums <= sample_index:
                    raise e

                config.attempts.append(sample)
                try:
                    domain = domain != sample
                except:
                    pass

                printer.sample_error(sample, e.text, sample_index, domain)

            sample_index += 1

    def __domain_filter__(self, domain, context):
        return domain, self._clean_asts

    def __sampler__(self, domain, context):
        if domain.is_invalid():
            raise InvalidSpaceConstraint(
                "the constraints change to domain in invalid")
        return domain.get_sample(self._distribution), context

    def __check_sample__(self, sample, ast_result, context):
        visitors.ValidateSampler().transform_to_check_sample(ast_result, sample, context)


class SearchSpace(BasicSearchSpace):

    def __init__(self, domain, distribute_like, sampler, ast, clean_asts, layers, _hash=None) -> None:
        super().__init__(domain, distribute_like, sampler)
        self.ast_constraint: ast_constraint.AstRoot = ast
        self._clean_asts: ast_constraint.AstRoot = clean_asts
        self.visitor_layers = layers

    def __ast_init_filter__(self):
        return self.ast_constraint

    def __ast_result_filter__(self, result):
        return result + self._clean_asts

    def __domain_filter__(self, domain, context):
        ast_result = self.__ast_init_filter__()
        if len(ast_result.asts) == 0:
            return domain, self.__ast_result_filter__(ast_result)

        config = SearchSpaceConfig(printer=DefaultPrinter())
        printer = config.printer_class

        domain = copy(domain)

        printer.ast_transformation(domain, ast_result)

        for visitor in reversed(self.visitor_layers):
            if not visitor.do_transform_to_modifier:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain

            ast_result, domain = visitor.transform_to_modifier(
                ast_result, domain, context)

            printer.ast_transformation(
                domain, ast_result, visitor.__class__.__name__)

        return domain, self.__ast_result_filter__(ast_result)

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self.ast_constraint.asts += ast.asts
        return self

    def __copy__(self):
        return type(self)(
            self.initial_domain,
            distribute_like=self.__distribute_like__,
            sampler=None,
            ast=ast_constraint.AstRoot(copy(self.ast_constraint.asts)),
            clean_asts=ast_constraint.AstRoot(copy(self._clean_asts.asts)),
            layers=copy(self.visitor_layers)
        )
