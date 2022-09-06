from search_space.errors import CircularDependencyDetected, NotEvaluateError
from search_space.utils.singleton import Singleton
from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import ast_index
from . import VisitorLayer


class IndexAstModifierVisitor(VisitorLayer):
    def __init__(self, space, index) -> None:
        self.current_index = index
        self.space = space
        self.index_solution = IndexSolutionVisitor()

    def transform_to_modifier(self, node, domain=None, context=None):
        return self.visit(node, context=context), domain

    def transform_to_check_sample(self, node, sample, context=None):
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node, current_index=[], context=None):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node, current_index=[], context=None):
        result = ast.AstRoot()

        for n in node.asts:
            result.add_constraint(
                self.visit(n, [], context=context))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.UniversalVariableBinaryOperation)
    def visit(self, node, current_index, context):
        a = self.visit(
            node.target, current_index, context=context)
        b = self.visit(
            node.other, current_index, context=context)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node, current_index, context):
        index = self.visit(node.other, current_index, context)
        return self.visit(node.target, [index.target] + current_index, context)

    @visitor.when(ast.SelfNode)
    def visit(self, node, current_index, context):
        if len(current_index) == 0:
            return node

        if tuple(current_index) == self.current_index:
            return node

        try:
            value = self.space[current_index].get_sample(context=context)
        except NotEvaluateError:
            return ast.NotEvaluate()
        except CircularDependencyDetected:
            return ast.NotEvaluate()

        return ast.NaturalValue(value)

    @visitor.when(ast.NaturalValue)
    def visit(self, node, current_index, context):
        if isinstance(node.target, ast_index.IndexNode):
            result = self.index_solution.visit(
                self.current_index, node.target, context)
            if type(result) == type(bool()):
                return ast.NaturalValue(self.current_index[-len(current_index) - 1])
            else:
                return ast.NaturalValue(result)

        # if not any(current_index):
        #     return node

        # try:
        #     return ast.NaturalValue(self.space.__get_index__(current_index, self.context))
        # except AttributeError:
        #     for i in reversed(current_index):
        #         node.target = node.target[i]

        return node


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
        try:
            return node.target.get_sample(context=context)[0]
        except AttributeError:
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
