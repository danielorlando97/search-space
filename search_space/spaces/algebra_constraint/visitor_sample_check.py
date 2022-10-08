from doctest import Example
from random import sample
from token import EXACT_TOKEN_TYPES
from search_space.spaces.algebra_constraint.visitor_index_ast_modifier import IndexSolutionVisitor
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.errors import InvalidSampler, NotEvaluateError
from search_space.utils.ast_tools import index_list
from . import VisitorLayer
from search_space.utils.singleton import Singleton
from search_space.spaces.algebra_constraint.functions_and_predicates import FunctionNode, AdvancedFunctionNode
from . import ast_index


class ValidateSampler(VisitorLayer, metaclass=Singleton):

    def __init__(self) -> None:
        self.index_solution = IndexSolutionVisitor()

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

    @visitor.when(ast.AstRoot)
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

    @visitor.when(ast.ModOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return a % b

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(ast.AndOp)
    def visit(self, node, current_index=[]):
        a = self.visit(node.target, current_index)

        if type(a) == bool and not a:
            return a

        return self.visit(node.other, current_index)

    @visitor.when(ast.OrOp)
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

    @visitor.when(ast.NotEqualOp)
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

    @visitor.when(ast.EqualOp)
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

    @visitor.when(ast.LessOp)
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

    @visitor.when(ast.LessOrEqualOp)
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

    @visitor.when(ast.GreatOp)
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

    @visitor.when(ast.GreatOrEqualOp)
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

    @visitor.when(ast.GetItem)
    def visit(self, node: ast.GetItem, current_index=[]):

        b = self.visit(node.other, current_index)
        return self.visit(node.target, current_index + [b])

    @visitor.when(ast.GetAttr)
    def visit(self, node: ast.GetAttr, current_index=[]):

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

    @ visitor.when(ast.SelfNode)
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

    @ visitor.when(ast.NaturalValue)
    def visit(self, node, current_index=[]):
        if isinstance(node.target, ast_index.IndexNode):
            result = self.index_solution.visit(
                current_index, node.target, self.context)
            if type(result) == type(bool()):
                return current_index[-len(current_index) - 1]
            else:
                return result

        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target
        except TypeError:
            pass

    @ visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        return node.func(*new_args, **new_kw)


# class SimpleIndexChecker:
#     def __init__(self, sample, context) -> None:
#         self.sample = sample
#         self.index_node = []
#         self.index_solution = IndexSolutionVisitor()
#         self.dim = ()
#         self.index_list = []
#         self._maps = []
#         self.context = context

#     def add_dim(self, node):
#         self.index_node.append(node)

#         pivot, self.dim = self.sample, []
#         for i in range(len(self.index_node)):
#             pivot, value = pivot[0], len(pivot)
#             self.dim.append(value)

#     def __iter__(self):
#         if len(self.index_node) > self.dim:

#             self.index_list = index_list(self.dim)
#         return self.index_list.__iter__()

#     def __cmp_value__(self, index):
#         result = [self.sample]
#         for i in index:
#             ii = self.index_solution.visit(
#                 index, self.index_node[i], self.context)

#             for
#             result = result[i]

#         for f in self._maps:
#             result = f(result)

#         return [result]

#     def __op_exec__(self, other, predicate):
#         for index in self:
#             try:
#                 values = other.__cmp_value__(index)
#             except AttributeError:
#                 values = [other]

#             for current_value in self.__cmp_value__(index):
#                 for other_value in values:
#                     if not predicate(current_value, other_value):
#                         return False
#         return True

#     def __eq__(self, __o: object) -> bool:
#         return self.__op_exec__(__o, lambda c, o: c == o)
