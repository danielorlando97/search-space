from unittest import result
from search_space.context_manager.sampler_context import SamplerContext
from search_space.errors import DetectedRuntimeDependency, InvalidSampler, InvalidSpaceConstraint, NotEvaluateError
from search_space.spaces import BasicSearchSpace
from copy import copy
from search_space.spaces.visitors import visitors
from search_space.spaces.asts import constraints as ast_constraint
# TODO: check space types
import numpy as np


class ListSlicePointer:
    def __init__(self, _slice, tensor, dims) -> None:
        self.slice: slice = _slice[0]
        self.tensor: ListSearchSpace = tensor
        self.dims = dims

    def get_sample(self, context: SamplerContext = None, local_domain=None):
        dynamic_result = context.get_sampler_value(self.tensor)

        for index in range(*self.slice.indices(self.dims)):
            if np.isnan(dynamic_result[index]):
                dynamic_result[index], context = self.tensor.__sample_index__(
                    (index,), context, local_domain)

        return dynamic_result[self.slice], context


class TensorSlicePointer:

    def __init__(self, index, tensor, dims) -> None:
        self.index = index
        self.tensor: TensorSearchSpace = tensor
        self.dims = dims

    def get_sample(self, context=None, local_domain=None):
        if context is None:
            context = SamplerContext(name="TensorSlicePointer")
        else:
            cache_value = context.get_sampler_value(self)
            if not cache_value is None:
                return cache_value, context

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
        return self.tensor.__sample_index__(self.index, context, local_domain)


class ListSearchSpace(BasicSearchSpace):

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, shape_space: list, distribute_like=None) -> None:
        super().__init__((), None)
        self.len_spaces = shape_space if type(
            shape_space) in [type(list()), type(tuple())] else [shape_space]

        self.samplers = {}
        self.ast_constraint = ast_constraint.AstRoot([])
        self.visitor_layers = []

    def set_type(self, space: BasicSearchSpace):
        if len(self.len_spaces) > 1:
            return TensorSearchSpace(self.len_spaces).set_type(space)

        self.type_space = space

        if isinstance(self.len_spaces[0], BasicSearchSpace):
            return self

        self._current_shape = self.len_spaces[0]
        for index in range(self.len_spaces[0]):
            self._create_sampler_by_index((index,))

        return self

    def _get_range_iter(self, limit, length):
        if isinstance(limit, int):
            return range(limit)

        return range(*limit.indices(length))

    def __copy__(self):
        result = super().__copy__()
        result.len_spaces = self.len_spaces
        result.type_space = self.type_space
        result.ast_constraint = self.ast_constraint

        for key, sampler in self.samplers.items():
            result.samplers[key] = copy(sampler)

        return result

    # def bfs_dimensions_computing(self, dims):
    #     Q = [(i,) for i in self._get_range_iter(dims[0], self.len_spaces[0])]

    #     for i in range(1, len(dims)):
    #         temp = []
    #         for j in self._get_range_iter(dims[i], self.len_spaces[i]):
    #             for n in Q:
    #                 temp.append(n + (j,))
    #         Q = temp

    #     return Q

    #################################################################
    #                                                               #
    #                     GetItem                                   #
    #                                                               #
    #################################################################

    def _check_limits(self, index):
        if len(index) != 1:
            raise InvalidSampler(
                f"shape error, the index {index} in dimension {self.len_spaces}")
        i = index[0]
        shape = self._current_shape
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
            self.samplers[index].space_name = f'{self.samplers[index].space_name}_{index}'
            self.samplers[index].layers_append(*self.visitor_layers)
            self.samplers[index].layers_append(
                visitors.EvalAstChecked(),
                visitors.IndexAstModifierVisitor(self, index)
            )

            self.samplers[index] = self.samplers[index].__ast_optimization__(
                self.ast_constraint)

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

        return ListSlicePointer(index, self, self._current_shape)

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

    def layers_append(self, *args):
        self.visitor_layers += list(args)
        for key in self.samplers.keys():
            self.samplers[key].layers_append(*args)

    #################################################################
    #                                                               #
    #                     Sample Generate                           #
    #                                                               #
    #################################################################

    def __sampler__(self, domain, context: SamplerContext):

        try:
            self._current_shape = self.len_spaces[0].get_sample(context)[0]
        except AttributeError:
            self._current_shape = self.len_spaces[0]

        result = [np.nan] * self._current_shape
        context = context.create_child(f'{self.space_name}_index')
        context.registry_sampler(self, result)
        for index in range(self._current_shape):
            index = index,
            self._create_sampler_by_index(index)
            result[index[0]] = self.samplers[index].get_sample(context)[0]

        return result, context

    def __sample_index__(self, index, context: SamplerContext, domain):
        dynamic_result = context.get_sampler_value(self)
        dynamic_result[index[0]], context = self.samplers[index].get_sample(
            context)
        return dynamic_result[index[0]], context

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


class TensorSearchSpace(BasicSearchSpace):

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, shape_space: list, distribute_like=None) -> None:
        super().__init__((), None)
        self.len_spaces = shape_space if type(
            shape_space) in [type(list()), type(tuple())] else [shape_space]

        self.samplers = {}
        self.ast_constraint = ast_constraint.AstRoot([])
        self._current_shape = []
        self.visitor_layers = []

    def set_type(self, space: BasicSearchSpace):
        self.type_space = space

        for size in self.len_spaces:
            if isinstance(size, BasicSearchSpace):
                break
        else:

            self._current_shape = self.len_spaces
            self.iter_virtual_list(
                self.len_spaces, [], lambda index: self[index])

        return self

    def __copy__(self):
        result = super().__copy__()
        result.len_spaces = []
        for item in self.len_spaces:
            _copy = copy(item)
            try:
                _copy.set_hash(hash(item))
            except AttributeError:
                pass
            result.len_spaces.append(_copy)

        result.type_space = self.type_space
        result.ast_constraint = self.ast_constraint

        for key, sampler in self.samplers.items():
            result.samplers[key] = copy(sampler)

        return result

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
            self.samplers[index].space_name = f'{self.samplers[index].space_name}_{index}'
            self.samplers[index].layers_append(*self.visitor_layers)
            self.samplers[index].layers_append(
                visitors.EvalAstChecked(),
                visitors.IndexAstModifierVisitor(self, index)
            )

            self.samplers[index] = self.samplers[index].__ast_optimization__(
                self.ast_constraint)

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
        return TensorSlicePointer(flatter_index, self, self._current_shape)

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

    def layers_append(self, *args):
        self.visitor_layers += list(args)
        for key in self.samplers.keys():
            self.samplers[key].layers_append(*args)

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
        context = context.create_child(f'{self.space_name}_index')
        return self.iter_virtual_list(
            shape, [], lambda index: self[index].get_sample(context)[0]), context

    def __sample_index__(self, index, context: SamplerContext, domain):
        return self.samplers[index].get_sample(context, domain)

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


# TODO copy
