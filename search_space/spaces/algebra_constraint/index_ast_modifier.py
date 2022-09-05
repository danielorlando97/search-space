from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import ast_index


class IndexAstModifierVisitor:
    def __init__(self, context, space) -> None:
        self.context = context
        self.space = space

        self.index_solution = IndexSolutionVisitor(context)

    @visitor.on("node")
    def visit(self, node, current_index):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node: ast.AstRoot, current_index):
        self.current_index = current_index
        result = ast.AstRoot()
        for n in node.asts:
            result.add_constraint(self.visit(n, []))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.UniversalVariableBinaryOperation)
    def visit(self, node, current_index):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node: ast.GetItem, current_index):
        if isinstance(node.other, ast_index.IndexNode):
            result = self.index_solution.visit(self.current_index, node.other)
            if type(result) == type(bool()):
                index = self.current_index[-len(current_index) - 1]
            else:
                index = result
        else:
            index = self.visit(node.other, current_index)

        return self.visit(node.target, [index] + current_index)

    @visitor.when(ast.SelfNode)
    def visit(self, node: ast.SelfNode, current_index):
        if not any(current_index):
            return node

        if tuple(current_index) == self.current_index:
            return node

        return ast.NaturalValue(self.space.__get_index__(current_index, self.context))

    @visitor.when(ast.NaturalValue)
    def visit(self, node: ast.NaturalValue, current_index):
        if not any(current_index):
            return node

        try:
            return ast.NaturalValue(self.space.__get_index__(current_index, self.context))
        except AttributeError:
            for i in reversed(current_index):
                node.target = node.target[i]

            return node


class IndexSolutionVisitor:
    def __init__(self, context) -> None:
        self.context = context

    @visitor.on("node")
    def visit(self, index, node):
        pass

    @visitor.when(ast_index.SelfNode)
    def visit(self, index, node: ast_index.SelfNode):
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
    def visit(self, index, node: ast_index.NegOp):
        return - self.visit(index, node.item)

    @visitor.when(ast_index.NaturalValue)
    def visit(self, index, node: ast_index.NaturalValue):
        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.AddOp)
    def visit(self, index, node: ast_index.AddOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a + b

    @visitor.when(ast_index.MultiOp)
    def visit(self, index, node: ast_index.MultiOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a * b

    @visitor.when(ast_index.SubOp)
    def visit(self, index, node: ast_index.SubOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a - b

    @visitor.when(ast_index.DivOp)
    def visit(self, index, node: ast_index.DivOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a / b

    @visitor.when(ast_index.ModOp)
    def visit(self, index, node: ast_index.ModOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a % b

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast_index.AndOp)
    def visit(self, index, node: ast_index.AndOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a and b

    @visitor.when(ast_index.OrOp)
    def visit(self, index, node: ast_index.OrOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
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
    def visit(self, index, node: ast_index.EqualOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a == b

    @visitor.when(ast_index.NotEqualOp)
    def visit(self, index, node: ast_index.NotEqualOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a != b

    @visitor.when(ast_index.LessOp)
    def visit(self, index, node: ast_index.LessOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a < b

    @visitor.when(ast_index.GreatOp)
    def visit(self, index, node: ast_index.GreatOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a > b

    @visitor.when(ast_index.GreatOrEqualOp)
    def visit(self, index, node: ast_index.GreatOrEqualOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a >= b

    @visitor.when(ast_index.LessOrEqualOp)
    def visit(self, index, node: ast_index.LessOrEqualOp):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a <= b
