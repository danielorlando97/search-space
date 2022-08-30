from search_space.spaces import SearchSpace, SearchSpaceDomain
from search_space.context_manager import SamplerContext
from search_space.errors import InvalidSpaceDefinition
from .numeral_search_space import NaturalSearchSpace
from search_space.spaces import visitors
from .object_search_space import ObjectDomain
from copy import copy


class ListDomain(ObjectDomain):
    def __init__(self, space) -> None:
        super().__init__(space)
        self.lazy_ast = []
        self.self_detection = visitors.SelfDetector()

    def transform(self, node, context):
        ast = self.attribute_attention.visit('len_space', node)
        self.domain["len_space"] = self.domain['len_space'].transform(
            ast, context)

        self.lazy_ast.append(node)
        return self

    def check_sampler(self, node, sampler, context):
        for i, sample in enumerate(sampler):
            ast = self.space.index_attention.visit(i, node, context, self)
            if not self.self_detection.visit(ast):
                continue
            super().check_sampler(ast, sample, context)

        return self


class ListSearchSpace(SearchSpace):
    def __init__(self, type_space: SearchSpace, len_space: NaturalSearchSpace = NaturalSearchSpace(), log_name=None, distribute_like=None) -> None:
        super().__init__(None, distribute_like, log_name)
        self.len_space = len_space
        self.type_space = type_space
        self.samplers = []
        self.index_attention = visitors.IndexTransform(self)

    # TODO: add not save to _get_random_value
    def _get_random_value(self, domain: ListDomain, context):
        _len, _ = self.len_space.get_sampler(
            context=context, local_domain=domain.domain['len_space'])

        result = []
        self._circular_mask_checker = [False] * _len
        for sample_index in range(_len):
            value = self._getitem_(
                sample_index, context, domain)
            result.append(value)

        return result

    def _getitem_(self, sample_index, context: SamplerContext, domain: ListDomain):
        try:
            sampler: SearchSpace = self.samplers[sample_index]
        except IndexError:
            sampler: SearchSpace = copy(self.type_space)
            self.samplers.append(sampler)

        if self._circular_mask_checker[sample_index] and context.get_sampler_value(sampler) is None:
            raise InvalidSpaceDefinition(
                f"Circular Space Definition in {self.scope}")

        self._circular_mask_checker[sample_index] = True

        local_constraints = []
        for ast in domain.lazy_ast:
            ast = self.index_attention.visit(
                sample_index, ast, context, domain)
            if domain.self_detection.visit(ast):
                local_constraints.append(ast)

        return sampler.get_sampler(context=context, local_constraints=local_constraints)[0]

    # TODO: Include domain

    def _create_domain(self, domain) -> SearchSpaceDomain:
        return ListDomain(self)

    def __copy__(self):
        instance = super().__copy__()
        instance.len_space = copy(self.len_space)
        instance.type_space = copy(self.type_space)

        return instance
