from search_space.errors import DetectedRuntimeDependency, InvalidSampler, NotEvaluateError
from search_space.spaces.search_space import BasicSearchSpace, GetSampleParameters, GetSampleResult
from copy import copy
from search_space.spaces.visitors import visitors
from search_space.spaces.asts import constraints as ast_constraint
from typing import Dict, Tuple
# TODO: check space types
import numpy as np


class ListSlicePointer:
    """
        This class is a pointer to some ListSpace slice
        The ListSpace is different that TensorSpace, because
        to build ListSpace samples is lineal. This space create
        a first list with NA and it was building index by index

        For Example:
            Let's x the sample list in the context, list dims is 4
            and we want the random slice [1:]. So:
            ```python
            >>> x = context.get_sampler_value(self.tensor)
            >>> # x == [NA, 1, NA, 3]
            ```
            In this case, we only need to generate a random value
            to the third index
    """

    def __init__(self, _slice, tensor, dims) -> None:
        self.slice: slice = _slice[0]
        self.tensor: ListSearchSpace = tensor
        self.dims = dims

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:
        # The first step of the ListSpace's generative mechanic
        # is to registry a list like ([NA] * len) as sample in the context.
        # After that, this sample can build index by index
        dynamic_result = params.context.get_sampler_value(self.tensor)

        for index in range(*self.slice.indices(self.dims)):
            if np.isnan(dynamic_result[index]):
                # If one of slice's indexes hasn't sampled yet
                # We have to get a nue sample for it
                result = self.tensor.__sample_index__(
                    (index,), params
                )

                dynamic_result[index] = result.sample
                params.context = result.context

        # return sampled slice
        return params.build_result(dynamic_result[self.slice])


class TensorSlicePointer:
    """
        This class is a pointer to some TensorSpace slice.
        In this case, we alway have to iterate for all index into
        the slice and to generate a sample or to get a sample from the context

        This process only can be by recursivity because as parameter we only have
        matrix dimensions.
    """

    def __init__(self, index, tensor, dims) -> None:
        self.index = index
        self.tensor: TensorSearchSpace = tensor
        self.dims = dims

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:
        params.initialize("TensorSlicePointer")

        # TODO: check if this cache is successful
        cache_value = params.context.get_sampler_value(self)
        if not cache_value is None:
            return params.build_result(cache_value)

        # The only way we can build a matrix slice is by recursivity
        sample = self._sample(self.index, params)
        params.context.registry_sampler(self, sample)

        return params.build_result(sample)

    def _sample(self, index, params: GetSampleParameters):
        if type(index) == type(tuple()):
            return self.tensor.samplers[index].get_sample(params).sample

        result = []
        for item in index:
            result.append(self._sample(item, params))

        return result

    def __hash__(self) -> int:
        return id(self)


class TensorIndexPointer:

    """
        This a pointer to one index into a ListSpace or a TensorSpace
    """

    def __init__(self, index, tensor) -> None:
        self.index = index
        self.tensor: TensorSearchSpace = tensor

    def get_sample(self, params: GetSampleParameters) -> GetSampleResult:
        return self.tensor.__sample_index__(self.index, params)


class ListSearchSpace(BasicSearchSpace):

    #################################################################
    #                                                               #
    #                     Space Initialize                          #
    #                                                               #
    #################################################################

    def __init__(self, shape_space: list, distribute_like=None, path=None) -> None:
        path = 'list_space' if path is None else path
        super().__init__((), None, path=path)

        # space configs
        self.samplers: Dict[Tuple, BasicSearchSpace] = {}
        self.len_spaces = shape_space if type(
            shape_space) in [list, tuple] else [shape_space]

        # generation configs
        self.ast_constraint = ast_constraint.AstRoot([])
        self.visitor_layers = []

    def set_type(self, space: BasicSearchSpace):
        """
            The DSL add tensor dims one by one.
            So, when the user finished to add them
            the DSL interface calls this function
            to end to build the tensor space
        """

        if len(self.len_spaces) > 1:
            # The class ListSearchSpace is a particular case of tensors space
            # I was created this class to generate simply sample faster
            # But, In more difficult cases we have use TensorSearchSpace class
            return TensorSearchSpace(self.len_spaces).set_type(space)

        self.type_space = space

        # If the list space's length is a SearchSpace, then
        # this ListSpace is a Space with dynamic dimension
        # So, we cannot prepare more thinks in compile time
        if isinstance(self.len_spaces[0], BasicSearchSpace):
            return self

        # If this space is a static list space, we can create
        # one space for each index and to reduce the operations number
        # at sampling time
        self._current_shape = self.len_spaces[0]
        for index in range(self.len_spaces[0]):
            self._create_sampler_by_index((index,))

        return self

    # def _get_range_iter(self, limit, length):
    #     if isinstance(limit, int):
    #         return range(limit)

    #     return range(*limit.indices(length))

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
        """
            This function initialize and get the space of index
        """

        try:
            self.samplers[index]
        except KeyError:
            self.samplers[index] = copy(self.type_space)
            self.samplers[index].space_name = f'{self.samplers[index].space_name}_{index}'
            self.samplers[index].path_space = f'{self.samplers[index].path_space}_{index}'
            # To transform the constraint about one tensor index
            # we need to apply all of transformations that
            # the tensor space needs
            self.samplers[index].layers_append(*self.visitor_layers)
            # After we have moved all constraint to the tensor spaces node
            # we need transform those constraint for they refer the index space
            self.samplers[index].layers_append(
                visitors.EvalAstChecked(),  # check integration and coherence
                # transform tensor[index] in self
                visitors.IndexAstModifierVisitor(self, index)
            )

            # Process all of tensor constraint to select which do refer to
            # this tensor's index
            self.samplers[index] = self.samplers[index].__ast_optimization__(
                self.ast_constraint
            )

    def __getitem__(self, index):
        self._check_limits(index)
        # if type(index) == type(list()):
        #     index = tuple(index)

        # for i in index:
        #     if isinstance(i, slice):
        #         break
        # else:
        if isinstance(index, slice):
            return ListSlicePointer(index, self, self._current_shape)

        self._create_sampler_by_index(index)
        return TensorIndexPointer(index, self)

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

    def __sampler__(self, domain, params: GetSampleParameters):

        try:
            # If this space is a dynamic list space
            # Before sampling this space we need to generate
            # a random length
            self._current_shape = self.len_spaces[0].get_sample(params).sample
        except AttributeError:
            self._current_shape = self.len_spaces[0]

        # How the list is a simply structure
        # We can create a void first sample
        result = [np.nan] * self._current_shape

        # We create a new context to discard samples easily
        # if there are some errors
        params = params.create_child_context(f'{self.space_name}_index')
        params.context.registry_sampler(self, result)

        for index in map(lambda x: (x,), range(self._current_shape)):
            self._create_sampler_by_index(index)
            result[index[0]] = self.samplers[index].get_sample(params).sample

        return params.build_result(result)

    def __sample_index__(self, index, params: GetSampleParameters):
        dynamic_result = params.context.get_sampler_value(self)
        result = self.samplers[index].get_sample(params)
        dynamic_result[index[0]] = result.sample
        return result

    def __domain_filter__(self, domain, params: GetSampleParameters):
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

    def __init__(self, shape_space: list, distribute_like=None, path=None) -> None:
        path = 'list_space' if path is None else path
        super().__init__((), None, path=path)

        # space configs
        self.samplers = {}
        self._current_shape = []
        self.len_spaces = shape_space if type(
            shape_space) in [list, tuple] else [shape_space]

        # generation configs
        self.ast_constraint = ast_constraint.AstRoot([])
        self.visitor_layers = []

    def set_type(self, space: BasicSearchSpace):
        """
            The DSL add tensor dims one by one. 
            So, when the user finished to add them 
            the DSL interface calls this function 
            to end to build the tensor space
        """

        self.type_space = space

        for size in self.len_spaces:
            if isinstance(size, BasicSearchSpace):
                break
        else:
            # If this space is a static tensor space, we can create
            # one space for each index and
            # to reduce the operations number at sampling time
            self._current_shape = self.len_spaces
            self.iter_virtual_list(
                self.len_spaces, [], lambda index: self[index])

        return self

    # TODO: copies by tag_names
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
            self.samplers[index].path_space = f'{self.samplers[index].path_space}_{index}'
            # To transform the constraint about one tensor index
            # we need to apply all of transformations that
            # the tensor space needs
            self.samplers[index].layers_append(*self.visitor_layers)
            # After we have moved all constraint to the tensor spaces node
            # we need transform those constraint for they refer the index space
            self.samplers[index].layers_append(
                visitors.EvalAstChecked(),  # check integration and coherence
                # transform tensor[index] in self
                visitors.IndexAstModifierVisitor(self, index)
            )

            # Process all of tensor constraint to select which do refer to
            # this tensor's index
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

    def __sampler__(self, domain, params: GetSampleParameters):

        shape = []
        for ls in self.len_spaces:
            try:
                # If this space is a dynamic tensor space
                # Before sampling this space we need to generate
                # a random length
                shape.append(ls.get_sample(params).sample)
            except AttributeError:
                shape.append(ls)

        self._current_shape = tuple(shape)

        # We create a new context to discard samples easily
        # if there are some errors
        params = params.create_child_context(f'{self.space_name}_index')

        return params.build_result(
            self.iter_virtual_list(
                shape, [],
                lambda index: self[index].get_sample(params).sample
            )
        )

    def __sample_index__(self, index, params: GetSampleParameters):
        return self.samplers[index].get_sample(params)

    def __domain_filter__(self, domain, params: GetSampleParameters):
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
