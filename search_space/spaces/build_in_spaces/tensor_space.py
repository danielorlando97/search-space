from search_space.context_manager.sampler_context import SamplerContext
from search_space.errors import DetectedRuntimeDependency, InvalidSampler, InvalidSpaceConstraint, NotEvaluateError
from search_space.spaces import BasicSearchSpace
from copy import copy
from search_space.spaces.algebra_constraint import visitors
from search_space.spaces.algebra_constraint import ast as ast_constraint
# TODO: check space types


class TensorSlicePointer:

    def __init__(self, index, tensor) -> None:
        self.index = index
        self.tensor: TensorSearchSpace = tensor

    def get_sample(self, context=None, local_domain=None):
        if context is None:
            context = SamplerContext()

        sample = self._sample(context, local_domain, self.index)
        context.registry_sampler(self, sample)

        return sample, context

    def _sample(self, context, local_domain, index):
        if type(index) == type(tuple()):
            return self.tensor.samplers[index].get_sample(context, local_domain)[0]

        result = []
        for item in index:
            result.append(self._sample(context, local_domain, item))

        return result

    def __hash__(self) -> int:
        return id(self)


class TensorIndexPointer:

    def __init__(self, index, tensor) -> None:
        self.index = index
        self.tensor: TensorSearchSpace = tensor

    def get_sample(self, context=None, local_domain=None):
        return self.tensor.samplers[self.index].get_sample(context, local_domain)


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
        self._current_shape = []

    def set_type(self, space: BasicSearchSpace):
        self.type_space = space

        for size in self.len_spaces:
            if isinstance(size, BasicSearchSpace):
                break
        else:

            self._current_shape = self.len_spaces
            self.iter_virtual_list(
                self.len_spaces, [], lambda index: self[index])

    def iter_virtual_list(self, shape, index, func):
        if len(shape) == 0:
            return func(index)

        result = []
        for i in range(shape[0]):
            result.append(self.iter_virtual_list(shape[1:], index + [i], func))

        return result

    def _check_limits(self, index):
        if len(index) != len(self._current_shape):
            raise InvalidSampler(
                f"shape error, the index {index} in dimension {self._current_shape}")

        for i, shape in zip(index, self._current_shape):
            try:
                if i < 0 or i >= shape:
                    raise NotEvaluateError()
            except TypeError:
                if i.start < 0 or i.stop >= shape:
                    raise NotEvaluateError()

    def _create_sampler_by_index(self, index):
        try:
            self.samplers[index]
        except KeyError:
            self.samplers[index] = copy(self.type_space)
            self.samplers[index].visitor_layers += [
                visitors.EvalAstChecked(),
                visitors.IndexAstModifierVisitor(self, index)
            ]
            self.samplers[index].__ast_optimization__(self.ast_constraint)

    def _flatter_index(self, index, i=0, result=[]):
        if i >= len(index):
            result = tuple(result)
            self._create_sampler_by_index(result)
            return result

        if isinstance(index[i], int):
            return self._flatter_index(index, i + 1, result + tuple(index[i]))

        response = []
        for j in range(*index[i].indices(self._current_shape[i])):
            response.append(self._flatter_index(index, i + 1, result + [j]))

        return response

    def __getitem__(self, index):
        self._check_limits(index)
        if type(index) == type(list()):
            index = tuple(index)

        for i in index:
            if isinstance(i, slice):
                break
        else:
            self._create_sampler_by_index(index)
            return TensorIndexPointer(index, self)

        flatter_index = self._flatter_index(index)
        return TensorSlicePointer(flatter_index, self)

    #################################################################
    #                                                               #
    #                     Ast Optimization                          #
    #                                                               #
    #################################################################

    def __domain_optimization__(self, domain, ast_result):
        raise DetectedRuntimeDependency()

    def __advance_space__(self, ast: ast_constraint.AstRoot):
        self.ast_constraint.asts += ast.asts
        return self

    def __ast_optimization__(self, ast_list):

        super().__ast_optimization__(ast_list)

        for key, space in self.samplers.items():
            self.samplers[key] = space.__ast_optimization__(ast_list)

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

        self._current_shape = tuple(shape)
        context = context.create_child()
        return self.iter_virtual_list(
            shape, [], lambda index: self[index].get_sample(context)[0])

    def __domain_filter__(self, domain, context):
        return domain, self.ast_constraint

    # TODO: Check list

    def __check_sample__(self, sample, ast_result, context):
        return sample
        # self.iter_virtual_list(
        #     self._current_shape, [],
        #     lambda index: visitors.ValidateSampler().check_sample_by_index(
        #         ast_result, sample, context, index
        #     )
        # )

    def __check_index__(self, index):
        for i, size in enumerate(self._current_shape):
            try:
                value = index[i]
            except IndexError:
                raise InvalidSpaceConstraint(
                    f'bad index reference index={index} shape={self._current_shape}')

            if value < 0 or value >= size:
                raise NotEvaluateError("Index out of range")


# TODO copy
