from threading import currentThread
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, NotEvaluateError
from search_space.spaces.visitors.functions_and_predicates import FunctionNode
from search_space.utils.singleton import Singleton
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from . import ast_index
from . import VisitorLayer


class IndexAstModifierVisitor(VisitorLayer):
    def __init__(self, space, index) -> None:
        self.current_index = index
        self.space = space
        self.index_solution = IndexSolutionVisitor()

    def domain_optimization(self, node, domain):
        self.context = None
        return self.visit(node), domain

    def transform_to_modifier(self, node, domain=None, context=None):
        self.context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        self.context = context
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node, current_index=[]):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node, current_index=[]):
        result = constraints.AstRoot([])

        for n in node.asts:
            result.add_constraint(self.visit(n, None))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node, current_index):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

# TODO: refactor to x[(i, j)]
    @visitor.when(constraints.GetItem)
    def visit(self, node, current_index):
        current_index = [] if current_index is None else current_index
        index = self.visit(node.other, current_index)
        return self.visit(node.target, [index.target] + current_index)

    @visitor.when(constraints.GetAttr)
    def visit(self, node, current_index):
        name = self.visit(node.other, current_index)
        target = self.visit(node.target, current_index)

        return constraints.GetAttr(target, name)

    @visitor.when(constraints.SelfNode)
    def visit(self, node, current_index):
        if current_index is None:
            return node

        if len(current_index) == 0:
            return constraints.NotEvaluate()

        if tuple(current_index) == self.current_index:
            return node

        try:
            if self.context is None:
                return constraints.NaturalValue(self.space[current_index])

            value = self.space[current_index].get_sample(context=self.context)
        except NotEvaluateError:
            return constraints.NotEvaluate()
        except CircularDependencyDetected:
            return constraints.NotEvaluate()

        return constraints.NaturalValue(value)

    def _index_solution(self, target, current_index):
        if not isinstance(target, ast_index.IndexNode):
            if self.context is None:
                return target

            try:
                _ = target.get_sample
            except AttributeError:
                return target

            return target.get_sample(context=self.context)[0]

        result = self.index_solution.visit(
            self.current_index, target, self.context)

        if type(result) == type(bool()):
            return self.current_index[-len(current_index) - 1]

        return result

    @visitor.when(constraints.NaturalValue)
    def visit(self, node, current_index):

        if isinstance(node.target, slice):
            start, stop, steep = (
                self._index_solution(node.target.start, current_index),
                self._index_solution(node.target.stop, current_index),
                self._index_solution(node.target.step, current_index)
            )

            return constraints.NaturalValue(slice(start, stop, steep))

        try:
            return constraints.NaturalValue(self._index_solution(node.target, current_index))
        except CircularDependencyDetected:
            return constraints.NotEvaluate()

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        return FunctionNode(node.func, new_args, new_kw)


class IndexSolutionVisitor(metaclass=Singleton):

    @visitor.on("node")
    def visit(self, index, node, context):
        pass

    @visitor.when(ast_index.SelfNode)
    def visit(self, index, node: ast_index.SelfNode, context):
        try:
            return index[node.shape_index]
        except IndexError:
            return index

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.NegOp)
    def visit(self, index, node: ast_index.NegOp, context):
        return - self.visit(index, node.item, context)

    @visitor.when(ast_index.NaturalValue)
    def visit(self, index, node: ast_index.NaturalValue, context):

        if hasattr(node.target, 'get_sample'):
            if context is None:
                raise DetectedRuntimeDependency()

            return node.target.get_sample(context=context)[0]

        return node.target

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.AddOp)
    def visit(self, index, node: ast_index.AddOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a + b

    @visitor.when(ast_index.MultiOp)
    def visit(self, index, node: ast_index.MultiOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a * b

    @visitor.when(ast_index.SubOp)
    def visit(self, index, node: ast_index.SubOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a - b

    @visitor.when(ast_index.DivOp)
    def visit(self, index, node: ast_index.DivOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a / b

    @visitor.when(ast_index.ModOp)
    def visit(self, index, node: ast_index.ModOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a % b

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.AndOp)
    def visit(self, index, node: ast_index.AndOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a and b

    @visitor.when(ast_index.OrOp)
    def visit(self, index, node: ast_index.OrOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a or b

# TODO
    # @visitor.when(ast.XorIndexNode)
    # def visit(self, index, node: ast.XorIndexNode):
    #     a = self.visit(index, node.a)
    #     b = self.visit(index, node.b)
    #     return a % b

    #################################################################
    #                                                               #
    #                 Binary Compare Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.EqualOp)
    def visit(self, index, node: ast_index.EqualOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a == b

    @visitor.when(ast_index.NotEqualOp)
    def visit(self, index, node: ast_index.NotEqualOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a != b

    @visitor.when(ast_index.LessOp)
    def visit(self, index, node: ast_index.LessOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a < b

    @visitor.when(ast_index.GreatOp)
    def visit(self, index, node: ast_index.GreatOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a > b

    @visitor.when(ast_index.GreatOrEqualOp)
    def visit(self, index, node: ast_index.GreatOrEqualOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a >= b

    @visitor.when(ast_index.LessOrEqualOp)
    def visit(self, index, node: ast_index.LessOrEqualOp, context):
        a = self.visit(index, node.a, context)
        b = self.visit(index, node.b, context)
        return a <= b
