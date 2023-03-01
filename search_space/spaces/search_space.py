from copy import copy
from typing import List, Generic, TypeVar
from search_space.context_manager.runtime_manager import SearchSpaceConfig
from search_space.sampler.distribution_names import UNIFORM
from search_space.context_manager import SamplerContext
from search_space.errors import ArgumentFunctionError, DetectedRuntimeDependency, InvalidSampler, InvalidSpaceConstraint, InvalidSpaceDefinition
from search_space.errors import NotEvaluateError, CircularDependencyDetected
from search_space.utils.itertools import UncompressClass
from .asts import constraints as ast_constraint
from .asts import naturals_values as ast_natural
from .visitors import visitors
from .visitors import VisitorLayer
from .printer_tools.default_printer_class import DefaultPrinter
from search_space.sampler import ModelSampler
import inspect
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class GetSampleResult(Generic[T]):
    sample: T
    context: SamplerContext = None
    sampler: ModelSampler = None


@dataclass
class GetSampleParameters:
    """
    This struct contain all of dependencies that
    the function get_sample need to generate a new
    sample. It also have some function to transform and
    mute this dependencies.
    """

    context: SamplerContext = None
    sampler: ModelSampler = None
    # local_domain: Any = None

    def build_result(self, sample: T):
        return GetSampleResult(
            sample,
            context=self.context,
            sampler=self.sampler
        )

    def initialize(self, context_name=""):

        if self.context is None:
            # We need a SamplerContext to ensure the consistence and
            # coherence in the generative process

            self.context = SamplerContext(context_name)

        if self.sampler is None:
            # We need a sampling mechanism to generate random structures
            self.sampler = ModelSampler()

    def create_child_context(self, context_name) -> 'GetSampleParameters':
        return GetSampleParameters(
            context=self.context.create_child(context_name),
            sampler=self.sampler
        )


@dataclass
class SpaceInfo(UncompressClass):
    """
    This struct is to send some info about the space
    to its domain and sampler as easy and maintained way
    """
    distribution: str

    # Genetic samplers use path spaces as key of hyperparamters dict
    # When the search space is hieratichical there isn't problems
    # all of class have different types with different names
    # and there is usually an only root to generate sampler.
    # But we also can investigations with functional spaces
    # where there are more than one root and those roots
    # sometime have the same type. Usually when one space is root
    # its path_space is its type name. So, this cases where there're
    # more than one root the genetic samplers will have a contradictions.
    # In that case they have to use the hash to try to resolve them.
    path_space: str

    # How we have context dependency, it isn't enough
    # one hyperparameter as learning rate. We have to
    # control how much lean the sampler, but we also have
    # to control the different between simply spaces and
    # contextual spaces. We can't permit that the seconds lean
    # faster than firsts, because domains of seconds depend on
    # values of firsts
    learning_rate: float


class BasicSearchSpace:

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, initial_domain, distribute_like=UNIFORM, name=None, path="", tag=None) -> None:
        # super().__init__()

        # space basic vars
        self.initial_domain = initial_domain
        self.__distribute_like__: str = distribute_like
        self.space_name = self.__class__.__name__ if name is None else name
        self._path_space = path
        self.tag = tag

        # generation vars
        self.visitor_layers: List[VisitorLayer] = [
            visitors.DomainModifierVisitor()]
        self._inner_hash = None
        self._clean_asts = ast_constraint.AstRoot([])

        # global config vars
        self.config = SearchSpaceConfig(printer=DefaultPrinter())
        self.printer = self.config.printer_class
        self.learning_rate = self.config.simply_learning_rate

        # space info structure
        self.__info__ = SpaceInfo(
            path_space=path,
            distribution=distribute_like,
            learning_rate=self.config.simply_learning_rate
        )

    @property
    def path_space(self):
        return self._path_space

    @path_space.setter
    def path_space(self, value):
        self._path_space = value
        self.__info__.path_space = value

    def change_distribution(self, distribution):
        self.__distribute_like__ = distribution

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
            *domain,
            distribute_like=self.__distribute_like__,
            path=self.path_space,
        )

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

        for item in defaults:
            try:
                s = item.space
                if not s:
                    raise AttributeError()
            except AttributeError:
                raise InvalidSpaceDefinition(
                    "Some of the dependencies aren't valid spaces"
                )

            args.append(ast_natural.SpaceSelfNode(item.space))

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
            ast=ast,
            clean_asts=self._clean_asts,
            layers=self.visitor_layers,
            path=self.path_space,
            tag=self.tag
        )
        ss.space_name = self.space_name
        ss.set_hash(hash(self))
        return ss

    #################################################################
    #                                                               #
    #                     Sample Generate                           #
    #                                                               #
    #################################################################

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:

        params.initialize(self.space_name)
        self.printer.init_search(hash(self), self.space_name)

        # Check in the generate context if this
        # instance of Search Space has been sampling already
        cache_value = params.context.get_sampler_value(self)
        if not cache_value is None:
            self.printer.sample_value(cache_value, True)
            return params.build_result(cache_value)

        # If this space instance hasn't been sampling yet
        # We need to check if this space already has begun its generation
        # Because in that case, this try is a circular dependency
        # And this is a problem, a definition error
        precess_is_initialize = params.context.check_sampling_status(self)
        if not precess_is_initialize is None:
            raise CircularDependencyDetected(
                f'in {self.__class__.__name__}')

        # We have to notify that this space has begun
        # its generative process to check circular dependencies late on
        params.context.registry_init_sampler_process(self)
        self.printer.context_name(params.context)
        # domain = self.initial_domain if params.local_domain is None else params.local_domain

        # Before to generate a new sample we need to register
        # our space into the sampler. At that time this class
        # can create all of structures that it need to create
        # new random values

        # params.sampler.register_space(
        #     self.path_space,
        #     self.__distribute_like__,
        #     domain=self.initial_domain,

        #     space_learning_rate=self.learning_rate

        # )

        # We describe search spaces with a context-sensitive grammar
        # So, We have to filter the initial domain by current context
        # To get the more faceable domain
        # This process we call inference time
        self.printer.domain_init(self.initial_domain)
        self.printer.tabs += 1
        domain, ast_result = self.__domain_filter__(
            self.initial_domain, params
        )
        self.printer.tabs -= 1

        # Some constraint couldn't check neither at compile time nor
        # inference time. So, we have to solve it by back tracking.
        # And sometimes we can't solve it. For that we count how many
        # samples we already have generated
        sample_index = 0

        while True:

            # Get a new sample
            self.printer.tabs += 1
            sample, sample_context = self.__sampler__(domain, params)
            self.printer.tabs -= 1

            try:
                # Check if the new sample is consistent with all of constraints
                pre_sample_context = params.context
                params.context = sample_context
                self.__check_sample__(sample, ast_result, params)
                params.context = pre_sample_context

                # How we can have contextual dependencies. We have to registry
                # all of generated samples to take easily if some space depends on them
                params.context.registry_sampler(self, sample)

                self.printer.sample_value(sample)
                return params.build_result(sample)

            except InvalidSampler as e:
                # Throw the error if we have done to much attempts.
                # In that case, it's a very complex space to obtain random values.
                if not self.config.replay_nums is None and self.config.replay_nums <= sample_index:
                    raise e

                self.config.attempts.append(sample)

                # If this space was a simply space, then it's very easy to drop
                # one value from its domain. So, if we already know that one
                # value is unfeasible we can drop it from the dynamic domain.
                # If the space is a combined space to drop one option isn't trivial
                try:
                    domain = domain != sample
                except:
                    pass

                self.printer.sample_error(sample, e.text, sample_index, domain)

            sample_index += 1

    def __domain_filter__(self, domain, params: GetSampleParameters):
        return domain, self._clean_asts

    def __sampler__(self, domain, params: GetSampleParameters):
        if domain.is_invalid():
            raise InvalidSpaceConstraint(
                "the constraints change to domain in invalid"
            )

        # For generating a simply sample we need three things
        # - Limits or domains. They're in the param domain, it has this info.
        # - A sampler, some mechanic to get random values and make decisions
        #   it's into the var params. it's one of the dependencies of get_sample function
        # - Some other information about the space like its distribution, its name, its position
        #   into the main space, .... All of those are into the struct SpaceInfo,
        #   it save in self.__info__

        return domain.get_sample(params.sampler, **self.__info__), params.context

    def __check_sample__(self, sample, ast_result, params: GetSampleParameters):
        visitors.ValidateSampler().transform_to_check_sample(ast_result, sample, params)


class SearchSpace(BasicSearchSpace):

    def __init__(self, domain, distribute_like, ast, clean_asts, layers, path, tag) -> None:
        super().__init__(domain, distribute_like, path=path, tag=tag)
        self.learning_rate = self.config.dynamic_learning_rate

        # generation config
        self.ast_constraint: ast_constraint.AstRoot = ast
        self._clean_asts: ast_constraint.AstRoot = clean_asts
        self.visitor_layers = layers

    def __ast_init_filter__(self):
        return self.ast_constraint

    def __ast_result_filter__(self, result):
        return result + self._clean_asts

    def __domain_filter__(self, domain, params: GetSampleParameters):
        ast_result = self.__ast_init_filter__()
        if len(ast_result.asts) == 0:
            return domain, self.__ast_result_filter__(ast_result)

        domain = copy(domain)

        self.printer.ast_transformation(domain, ast_result)

        for visitor in reversed(self.visitor_layers):
            if not visitor.do_transform_to_modifier:
                continue
            # All visitors modifier the ast except the last one
            # The last one return the restricted domain

            ast_result, domain = visitor.transform_to_modifier(
                ast_result, domain, params
            )

            self.printer.ast_transformation(
                domain, ast_result, visitor.__class__.__name__)

        return domain, self.__ast_result_filter__(ast_result)

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self.ast_constraint.asts += ast.asts
        return self

    def __copy__(self):
        return type(self)(
            self.initial_domain,
            distribute_like=self.__distribute_like__,
            ast=ast_constraint.AstRoot(copy(self.ast_constraint.asts)),
            clean_asts=ast_constraint.AstRoot(copy(self._clean_asts.asts)),
            layers=copy(self.visitor_layers),
            path=self.path_space,
            tag=self.tag
        )
