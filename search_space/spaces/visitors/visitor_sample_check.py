from doctest import Example
from random import sample
from token import EXACT_TOKEN_TYPES
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
                self.visit(n, current_index)
            except NotEvaluateError:
                pass

    #################################################################
    #                                                               #
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    # @visitor.when(constraints.ModOp)
    # def visit(self, node, current_index=[]):
    #     a = self.visit(node.target, current_index)
    #     b = self.visit(node.other, current_index)

    #     return a % b

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
        a = self.visit(node.target, current_index)

        if type(a) == bool and a:
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
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node: constraints.GetItem, current_index=[]):

        b = self.visit(node.other, current_index)
        if type(b) == bool:
            b = self.current_index[-len(current_index) - 1]

        return self.visit(node.target, current_index + [b])

    @visitor.when(constraints.GetAttr)
    def visit(self, node: constraints.GetAttr, current_index=[]):

        b = self.visit(node.other, current_index)
        a = self.visit(node.target, current_index)

        try:
            space = a.__class__.__dict__[b]
        except KeyError:
            raise InvalidSampler(
                f"inconsistent sampler => {a} don't has {b} member")

        try:
            sampler = space.get_sample
        except AttributeError:
            raise InvalidSampler(
                f"inconsistent sampler => {a}.{b} isn't search space")

        return sampler(context=self.context)[0]

    @ visitor.when(constraints.SelfNode)
    def visit(self, node, current_index=[]):
        if len(current_index) == 0:
            return self.sample
        try:
            result = self.sample
            for i in current_index:
                result = result[i]

            return result
        except IndexError:
            raise NotEvaluateError()
        except TypeError:
            raise InvalidSampler(
                f"inconsistent sampler => sample isn't indexed")

    @ visitor.when(constraints.NaturalValue)
    def visit(self, node, current_index=[]):
        if isinstance(node.target, NaturalValuesNode):
            return self.natural_visitor.get_value(
                node.target, context=self._context
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

        return node.func(*new_args, **new_kw)
