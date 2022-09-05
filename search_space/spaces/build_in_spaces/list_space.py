from search_space.context_manager.sampler_context import SamplerContext
from search_space.errors import InvalidSampler
from search_space.spaces import SearchSpace
from copy import copy
from search_space.spaces.algebra_constraint import visitors
from .numeral_space import NaturalSearchSpace
from search_space.utils.singleton import Singleton


class TensorSearchSpace(SearchSpace):
    def __init__(self, space_type: SearchSpace, shape_space: list) -> None:
        super().__init__(None, None)
        self.len_spaces = shape_space
        self.type_space = space_type
        self.samplers = {}

    def get_sample(self, context=None, local_domain=None):

        context = context if not context is None else SamplerContext()
        cache_value = context.get_sampler_value(self)
        if not cache_value is None:
            return cache_value, context

        shape = []
        for ls in self.len_spaces:
            shape.append(ls.get_sample(context))

        self.__create_samplers__(
            shape, visitors.IndexAstModifierVisitor(context, self))

        while True:
            sample = self.__sampler__(shape, context.create_child())
            try:
                self.__check_sample__(sample, context)

                context.registry_sampler(self, sample)
                return sample, context

            except InvalidSampler:
                pass

    def __create_samplers__(self, shape, index_modifier: visitors.IndexAstModifierVisitor, index=[]):
        if not any(shape):
            try:
                self.samplers[tuple(index)]
            except KeyError:
                self.samplers[tuple(index)] = copy(self.type_space)
                self.samplers[tuple(index)] |= index_modifier.visit(
                    self.ast_constraint, tuple(index))

        else:
            for i in range(shape[0]):
                self.__create_samplers__(
                    shape[1:], index_modifier, index + [i])

    def __sampler__(self, shape, context, index=[]):
        if not any(shape):
            return self.samplers[tuple(index)].get_sample(context)

        result = []
        for i in range(shape[0]):
            result.append(self.__sampler__(shape[1:], context, index + [i]))

        return result


# TODO: revolver circular problem

    def __get_index__(self, index, context):
        try:
            sampler = self.samplers[tuple(index)]
        except KeyError:
            self.samplers[tuple(index)] = copy(self.type_space)
            self.samplers[tuple(index)] |= visitors.IndexAstModifierVisitor(context, self).visit(
                self.ast_constraint, tuple(index))

        return self.samplers[tuple(index)]
