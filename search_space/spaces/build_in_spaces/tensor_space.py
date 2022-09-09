from search_space.context_manager.sampler_context import SamplerContext
from search_space.errors import InvalidSpaceConstraint, NotEvaluateError
from search_space.spaces import SearchSpace
from copy import copy
from search_space.spaces.algebra_constraint import visitors
from .numeral_space import NaturalSearchSpace
from search_space.spaces.algebra_constraint import ast_index
from search_space.spaces.algebra_constraint import ast_constraint
# TODO: check space types


class TensorSearchSpace(SearchSpace):
    def __init__(self, space_type: SearchSpace, shape_space: list) -> None:
        super().__init__(None, None)
        self.len_spaces = shape_space if type(
            shape_space) in [type(list()), type(tuple())] else [shape_space]
        self.type_space = space_type
        self.samplers = {}

    def __domain_filter__(self, domain, context):
        shape = []
        for ls in self.len_spaces:
            try:
                shape.append(ls.get_sample(context)[0])
            except AttributeError:
                shape.append(ls)

        self.__current_shape = shape

        return super().__domain_filter__(domain, context)

    def __sampler__(self, domain, context):

        def f(shape, index):
            if len(shape) == 0:
                return self[index].get_sample(context, local_domain=domain)[0]

            result = []
            for i in range(shape[0]):
                result.append(f(shape[1:], index + [i]))

            return result

        return f(self.__current_shape, [])

    def __check_sample__(self, sample, ast_result, context):
        return sample

    def __build_constraint__(self, func):

        return func(*([ast_index.SelfNode(i) for i in range(0, len(self.len_spaces))] + [ast_constraint.SelfNode()]))

    def __getitem__(self, index):
        if type(index) == type(list()):
            index = tuple(index)

        try:
            self.samplers[index]
        except KeyError:
            self.samplers[index] = copy(self.type_space)
            self.samplers[index].visitor_layers += [
                visitors.EvalAstChecked(),
                visitors.IndexAstModifierVisitor(self, index)
            ]
            self.samplers[index].ast_constraint = self.ast_constraint

        return self.samplers[index]

    def __check_index__(self, index):
        for i, size in enumerate(self.__current_shape):
            try:
                value = index[i]
            except IndexError:
                raise InvalidSpaceConstraint(
                    f'bad index reference index={index} shape={self.__current_shape}')

            if value < 0 or value >= size:
                raise NotEvaluateError("Index out of range")


# TODO copy
