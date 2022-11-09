from typing import Iterator
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from search_space.spaces.asts import naturals_values
from search_space.errors import InvalidSampler, NotEvaluateError
from search_space.utils.ast_tools import index_list
from . import VisitorLayer
from search_space.utils.singleton import Singleton
from .visitor_natural_ast import NaturalAstVisitor, NaturalValuesNode
from search_space.utils import itertools
from typing import Iterable
from search_space.utils.itertools import is_iterable


class ValidateSampler(VisitorLayer, metaclass=Singleton):

    def __init__(self) -> None:
        self.natural_visitor = NaturalAstVisitor()

    def transform_to_check_sample(self, node, sample, context):
        self.sample, self.context = sample, context
        return self.visit(node)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node, current_index=[]):
        for n in node.asts:
            try:
                result = self.visit(n, current_index)
                if not result:
                    raise InvalidSampler("False Restriction")
            except NotEvaluateError:
                pass

    #################################################################
    #                                                               #
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    @visitor.when(constraints.AddOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return a + b

    @visitor.when(constraints.SubOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return a - b

    @visitor.when(constraints.MultiOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return a * b

    @visitor.when(constraints.DivOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return a / b

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(constraints.AndOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)

        if type(a) == bool and not a:
            return a

        return self.visit(node.other, current_index)

    @visitor.when(constraints.OrOp)
    def visit(self, node, current_index=[]):
        a = False
        try:
            a = self.visit(node.target, current_index)
        except InvalidSampler:
            pass

        if a:
            return a

        return self.visit(node.other, current_index)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.NotEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b) and not is_iterable(a):
            if not a in b:
                return self

        elif is_iterable(a) and not is_iterable(b):
            if not b in a:
                return self

        elif a != b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} != {b} ]")

    @visitor.when(constraints.EqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b) and not is_iterable(a):
            if a in b:
                return self

        elif is_iterable(a) and not is_iterable(b):
            if b in a:
                return self

        elif a == b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} == {b} ]")

    @visitor.when(constraints.LessOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b):
            b = min(b)

        if is_iterable(a):
            a = max(a)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(constraints.LessOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b):
            b = min(b)

        if is_iterable(a):
            a = max(a)

        if a <= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(constraints.GreatOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b):
            b = max(b)

        if is_iterable(a):
            a = min(a)

        if a > b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} > {b} ]")

    @visitor.when(constraints.GreatOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if is_iterable(b):
            b = max(b)

        if is_iterable(a):
            a = min(a)

        if a >= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} >= {b} ]")

    #################################################################
    #                                                               #
    #                 Segmentation Visit                            #
    #                                                               #
    #################################################################

    @visitor.when(constraints.SegmentationEqualOp)
    def visit(self, node: constraints.SegmentationEqualOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        mod = abs(target % factor)
        if is_iterable(value) and mod in value:
            return self

        if mod == abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} == {value} ]")

    @visitor.when(constraints.SegmentationNotEqualOp)
    def visit(self, node: constraints.SegmentationNotEqualOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        mod = target % factor
        if (
            is_iterable(value)
            and not mod in value
            and not -mod in value
        ):
            return self

        if mod != value and -mod != value:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} != {value} ]")

    @visitor.when(constraints.SegmentationLessOp)
    def visit(self, node: constraints.SegmentationLessOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        if is_iterable(value):
            value = min(value)

        if abs(target % factor) < abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} < {value} ]")

    @visitor.when(constraints.SegmentationLessOrEqualOp)
    def visit(self, node: constraints.SegmentationLessOrEqualOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        if is_iterable(value):
            value = min(value)

        if abs(target % factor) <= abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} <= {value} ]")

    @visitor.when(constraints.SegmentationGreatOp)
    def visit(self, node: constraints.SegmentationGreatOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        if is_iterable(value):
            value = max(value)

        if abs(target % factor) > abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} > {value} ]")

    @visitor.when(constraints.SegmentationGreatOrEqualOp)
    def visit(self, node: constraints.SegmentationGreatOrEqualOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)
        value = self.visit(node.value, current_index)

        if is_iterable(value):
            value = max(value)

        if abs(target % factor) >= abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} >= {value} ]")

    # @visitor.when(constraints.SegmentationAddOp)
    # def visit(self, node: constraints.SegmentationAddOp, current_index=[]):
    #     target = self.visit(node.target, current_index)
    #     factor = self.visit(node.value, current_index)

    #     if not target is None:
    #         return target + factor

    #     self.domain = self.domain.__mod_add__(factor, 0)

    # @visitor.when(constraints.SegmentationSubOp)
    # def visit(self, node: constraints.SegmentationSubOp, current_index=[]):
    #     target = self.visit(node.target, current_index)
    #     factor = self.visit(node.other, current_index)

    #     if not target is None:
    #         return target - factor

    #     self.domain = self.domain.__mod_sub__(factor, 0)

    # @visitor.when(constraints.SegmentationMultiOp)
    # def visit(self, node: constraints.SegmentationMultiOp, current_index=[]):
    #     target = self.visit(node.target, current_index)
    #     factor = self.visit(node.other, current_index)

    #     if not target is None:
    #         return target * factor

    #     self.domain = self.domain.__mod_mult__(factor, 0)

    # @visitor.when(constraints.SegmentationDivOp)
    # def visit(self, node: constraints.SegmentationDivOp, current_index=[]):
    #     target = self.visit(node.target, current_index)
    #     factor = self.visit(node.other, current_index)

    #     if not target is None:
    #         return target / factor

    #     self.domain = self.domain.__mod_div__(factor, 0)

    # @visitor.when(constraints.SegmentationModOp)
    # def visit(self, node: constraints.SegmentationModOp, current_index=[]):
    #     target = self.visit(node.target, current_index)
    #     factor = self.visit(node.other, current_index)

    #     if not target is None:
    #         return target % factor

    #     self.domain = self.domain.__mod_eq__(factor, 0)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node: constraints.GetItem):
        target = self.visit(node.target)

        try:
            _len = len(target)
        except TypeError:
            raise InvalidSampler(
                f"inconsistent sampler => {target} isn't indexed")

        indexes = self.visit_natural(node.other, _len)

        def f(a, b):
            try:
                return a[b]
            except TypeError:
                raise InvalidSampler(
                    f"inconsistent sampler => sample isn't indexed")

        return itertools.map_reduce(target, indexes, f)

    @visitor.when(constraints.GetAttr)
    def visit(self, node: constraints.GetAttr):
        b = self.visit(node.other)
        a = self.visit(node.target)

        def f(a, b):
            try:
                space = getattr(a, b)
            except AttributeError:
                raise InvalidSampler(
                    f"inconsistent sampler => {a} don't has {b} member")

            try:
                sampler = space.get_sample
            except AttributeError:
                raise InvalidSampler(
                    f"inconsistent sampler => {a}.{b} isn't search space")

            return sampler(context=a.__instance_context__)[0]

        return itertools.map_reduce(a, b, f)

    @ visitor.when(constraints.SelfNode)
    def visit(self, node):
        return self.sample

    @ visitor.when(constraints.NaturalValue)
    def visit(self, node):
        if isinstance(node.target, NaturalValuesNode):
            return self.natural_visitor.get_value(
                node.target,
                context=self.context,
            )
        return node.target

    # @visitor.when(constraints.FunctionNode)
    # def visit(self, node: constraints.FunctionNode, current_index):
    #     new_args = []
    #     for arg in node.args:
    #         new_args.append(self.visit(arg, current_index))

    #     new_kw = {}
    #     for name, arg in node.kwargs:
    #         new_kw[name] = self.visit(arg, current_index)

    #     result = node.func(*new_args, **new_kw)
    #     return result

    # @visitor.when(constraints.AdvancedFunctionNode)
    # def visit(self, node: constraints.FunctionNode, current_index):
    #     new_args = []
    #     for arg in node.args:
    #         new_args.append(self.visit(arg, current_index))

    #     new_kw = {}
    #     for name, arg in node.kwargs:
    #         new_kw[name] = self.visit(arg, current_index)

    #     result = node.func(*new_args, **new_kw)
    #     return result

    #################################################################
    #                                                               #
    #                 Natural Visit                                 #
    #                                                               #
    #################################################################

    @visitor.on("node")
    def visit_natural(self, node, _len=None):
        pass

    @visitor.when(constraints.NaturalValue)
    def visit_natural(self, node, _len):
        result = node.target
        if isinstance(node.target, NaturalValuesNode):
            self.len = _len
            result = self.visit_natural(node.target)
            self.len = None

        return result

    #################################################################
    #                                                               #
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.ModOp)
    def visit(self, node: naturals_values.ModOp):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce_longest(a, b, lambda a, b: a % b, 1)

    @visitor.when(naturals_values.AddOp)
    def visit(self, node: naturals_values.AddOp):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce_longest(a, b, lambda a, b: a + b, 0)

    @visitor.when(naturals_values.SubOp)
    def visit(self, node: naturals_values.SubOp):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce_longest(a, b, lambda a, b: a - b, 0)

    @visitor.when(naturals_values.MultiOp)
    def visit(self, node: naturals_values.MultiOp):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce_longest(a, b, lambda a, b: a * b, 1)

    @visitor.when(naturals_values.DivOp)
    def visit(self, node: naturals_values.DivOp):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce_longest(a, b, lambda a, b: a / b, 1)

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.AndOp)
    def visit(self, node: naturals_values.AndOp):
        a = self.visit_natural(node.a)

        if not isinstance(a, Iterator) and not a:
            return True

        b = self.visit_natural(node.b)

        return itertools.compare(a, b, lambda a, b: a and b)

    @visitor.when(naturals_values.OrOp)
    def visit(self, node: naturals_values.OrOp):
        a = self.visit_natural(node.a)

        if not isinstance(a, Iterator) and a:
            return True

        b = self.visit_natural(node.b)

        return itertools.compare(a, b, lambda a, b: a or b)

    #################################################################
    #                                                               #
    #             Binary Cmp Natural Visit                          #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.LessOp)
    def visit_natural(self, node: naturals_values, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a < b)

    @visitor.when(naturals_values.LessOrEqualOp)
    def visit_natural(self, node: naturals_values.LessOrEqualOp, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a <= b)

    @visitor.when(naturals_values.GreatOp)
    def visit_natural(self, node: naturals_values.GreatOp, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a > b)

    @visitor.when(naturals_values.GreatOrEqualOp)
    def visit_natural(self, node: naturals_values.GreatOrEqualOp, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a >= b)

    @visitor.when(naturals_values.NotEqualOp)
    def visit_natural(self, node: naturals_values.NotEqualOp, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a != b)

    @visitor.when(naturals_values.EqualOp)
    def visit_natural(self, node: naturals_values.EqualOp, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.filter(a, b, lambda a, b: a == b)

    #################################################################
    #                                                               #
    #                 Simple Natural Visit                          #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.GetAttr)
    def visit_natural(self, node: naturals_values.GetAttr, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        def f(a, b):
            value = getattr(a, b)
            try:
                _ = value.get_sample
            except AttributeError:
                return value

            return value.get_sample(a.__instance_context__)[0]

        yield itertools.map_reduce(a, b, f)

    @visitor.when(naturals_values.GetItem)
    def visit_natural(self, node: naturals_values.GetItem, _len=None):
        a = self.visit_natural(node.a)
        b = self.visit_natural(node.b)

        yield itertools.map_reduce(a, b, lambda a, b: a[b])

    @visitor.when(naturals_values.IndexSelf)
    def visit_natural(self, node, _len=None):
        for i in range(self.len - 1):
            yield i

        return self.len

    @visitor.when(naturals_values.SpaceSelfNode)
    def visit_natural(self, node: naturals_values.SpaceSelfNode, _len=None):
        return node.a.get_sample(self.context)[0]

    @visitor.when(naturals_values.NaturalValue)
    def visit_natural(self, node: naturals_values.NaturalValue, _len=None):
        return node.a
