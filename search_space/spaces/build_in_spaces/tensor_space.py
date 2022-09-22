from search_space.context_manager.sampler_context import SamplerContext
from search_space.errors import InvalidSpaceConstraint, NotEvaluateError
from search_space.spaces import BasicSearchSpace
from copy import copy
from search_space.spaces.algebra_constraint import visitors
from .numeral_space import NaturalSearchSpace
from search_space.spaces.algebra_constraint import ast_index
from search_space.spaces.algebra_constraint import ast as ast_constraint
# TODO: check space types


class TensorSearchSpace(BasicSearchSpace):

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, shape_space: list) -> None:
        super().__init__((), None)
        self.len_spaces = shape_space if type(
            shape_space) in [type(list()), type(tuple())] else [shape_space]

        self.samplers = {}
        self.ast_constraint = ast_constraint.AstRoot([])

    def set_type(self, space: BasicSearchSpace):
        self.type_space = space

        for size in self.len_spaces:
            if isinstance(size, BasicSearchSpace):
                break
        else:
            self.iter_virtual_list(
                self.len_spaces, [], lambda index: self[index])

    def iter_virtual_list(self, shape, index, func):
        if len(shape) == 0:
            return func(index)

        result = []
        for i in range(shape[0]):
            result.append(self.iter_virtual_list(shape[1:], index + [i], func))

        return result

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
            self.samplers[index].__ast_optimization__(self.ast_constraint.asts)

        return self.samplers[index]

    #################################################################
    #                                                               #
    #                     Ast Optimization                          #
    #                                                               #
    #################################################################

    def __ast_optimization__(self, ast_list):

        self.ast_constraint += ast_list

        for key, space in self.samplers.items():
            self.samplers[key] = space | ast_list

        return self

    #################################################################
    #                                                               #
    #                     Sample Generate                           #
    #                                                               #
    #################################################################

    def __sampler__(self, domain, context: SamplerContext):

        shape = []
        for ls in self.len_spaces:
            try:
                shape.append(ls.get_sample(context)[0])
            except AttributeError:
                shape.append(ls)

        context = context.create_child()
        return self.iter_virtual_list(
            shape, [], lambda index: self[index].get_sample(context)[0])

    def __check_sample__(self, sample, ast_result, context):
        return sample

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
