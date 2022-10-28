from search_space.utils import visitor
from search_space.spaces.asts import constraints
from search_space.errors import InvalidSampler, NotEvaluateError
from search_space.utils.ast_tools import index_list
from . import VisitorLayer
from search_space.utils.singleton import Singleton
from .visitor_natural_ast import NaturalAstVisitor, NaturalValuesNode


class ValidateSampler(VisitorLayer, metaclass=Singleton):

    def __init__(self) -> None:
        self.natural_visitor = NaturalAstVisitor()

    def check_is_not_eval_node(self, *nodes):
        for node in nodes:
            try:
                if not node.can_evaluate:
                    return node
            except AttributeError:
                pass
        return None

    @property
    def do_transform_to_modifier(self):
        return False

    def transform_to_check_sample(self, node, sample, context):
        self.sample, self.context = sample, context
        return self.visit(node)

    def check_sample_by_index(self, node, sample, context, index):
        self.current_index = index
        return self.transform_to_check_sample(node, sample, context)

    @visitor.on("node")
    def visit(self, node, current_index=[]):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node, current_index=[]):
        for n in node.asts:
            try:
                _ = self.visit(n, current_index)
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

        if type(b) in [list, tuple] and not type(a) in [list, tuple]:
            if not a in b:
                return self

        elif type(a) in [list, tuple] and not type(b) in [list, tuple]:
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

        if type(b) in [list, tuple] and not type(a) in [list, tuple]:
            if a in b:
                return self

        elif type(a) in [list, tuple] and not type(b) in [list, tuple]:
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

        if type(b) in [list, tuple]:
            b = min(b)

        if type(a) in [list, tuple]:
            a = max(a)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(constraints.LessOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if type(b) in [list, tuple]:
            b = min(b)

        if type(a) in [list, tuple]:
            a = max(a)

        if a <= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(constraints.GreatOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if type(b) in [list, tuple]:
            b = max(b)

        if type(a) in [list, tuple]:
            a = min(a)

        if a > b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} > {b} ]")

    @visitor.when(constraints.GreatOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if type(b) in [list, tuple]:
            b = max(b)

        if type(a) in [list, tuple]:
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
        if type(value) in [list, tuple] and mod in value:
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
            type(value) in [list, tuple]
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

        if type(value) in [list, tuple]:
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

        if type(value) in [list, tuple]:
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

        if type(value) in [list, tuple]:
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

        if type(value) in [list, tuple]:
            value = max(value)

        if abs(target % factor) >= abs(value):
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {target} % {factor} >= {value} ]")

    @visitor.when(constraints.SegmentationAddOp)
    def visit(self, node: constraints.SegmentationAddOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.value, current_index)

        if not target is None:
            return target + factor

        self.domain = self.domain.__mod_add__(factor, 0)

    @visitor.when(constraints.SegmentationSubOp)
    def visit(self, node: constraints.SegmentationSubOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)

        if not target is None:
            return target - factor

        self.domain = self.domain.__mod_sub__(factor, 0)

    @visitor.when(constraints.SegmentationMultiOp)
    def visit(self, node: constraints.SegmentationMultiOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)

        if not target is None:
            return target * factor

        self.domain = self.domain.__mod_mult__(factor, 0)

    @visitor.when(constraints.SegmentationDivOp)
    def visit(self, node: constraints.SegmentationDivOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)

        if not target is None:
            return target / factor

        self.domain = self.domain.__mod_div__(factor, 0)

    @visitor.when(constraints.SegmentationModOp)
    def visit(self, node: constraints.SegmentationModOp, current_index=[]):
        target = self.visit(node.target, current_index)
        factor = self.visit(node.other, current_index)

        if not target is None:
            return target % factor

        self.domain = self.domain.__mod_eq__(factor, 0)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node: constraints.GetItem, current_index=[]):

        b = self.visit(node.other, current_index)
        if type(b) == bool:
            b = self.current_index[-len(current_index) - 1]

        a = self.visit(node.target, current_index + [b])

        try:
            return a[b]
        except IndexError:
            raise NotEvaluateError()
        except TypeError:
            raise InvalidSampler(
                f"inconsistent sampler => sample isn't indexed")

    @visitor.when(constraints.GetAttr)
    def visit(self, node: constraints.GetAttr, current_index=[]):

        b = self.visit(node.other, current_index)
        a = self.visit(node.target, current_index)

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

    @ visitor.when(constraints.SelfNode)
    def visit(self, node, current_index=[]):
        return self.sample

    @ visitor.when(constraints.NaturalValue)
    def visit(self, node, current_index=[]):
        if isinstance(node.target, NaturalValuesNode):
            try:
                index = self.current_index
            except AttributeError:
                index = []
            return self.natural_visitor.get_value(
                node.target,
                context=self.context,
                current_index=index
            )
        return node.target

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        result = node.func(*new_args, **new_kw)

        if not result:
            raise InvalidSampler("False Restriction")

        return result

    @visitor.when(constraints.AdvancedFunctionNode)
    def visit(self, node: constraints.FunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        result = node.func(*new_args, **new_kw)
        if not result:
            raise InvalidSampler("False Restriction")
        return result
