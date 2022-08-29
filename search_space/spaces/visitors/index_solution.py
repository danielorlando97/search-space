from search_space.utils import visitor
from search_space.spaces import ast_index as ast


class IndexSolutionVisitor:
    def __init__(self, context) -> None:
        self.context = context

    @visitor.on("node")
    def visit(self, index, node):
        pass

    @visitor.when(ast.SelfIndex)
    def visit(self, index, node: ast.SelfIndex):
        return index

    #################################################################
    #                                                               #
    #                     Unary Operations                          #
    #                                                               #
    #################################################################

    @visitor.when(ast.NegativeIndexNode)
    def visit(self, index, node: ast.NegativeIndexNode):
        return - self.visit(index, node.item)

    @visitor.when(ast.NaturalValueIndexNode)
    def visit(self, index, node: ast.NaturalValueIndexNode):
        try:
            return node.item.get_sampler(context=self.context)[0]
        except AttributeError:
            return node.item

    #################################################################
    #                                                               #
    #              Binary Arithmetic Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast.AddIndexNode)
    def visit(self, index, node: ast.AddIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a + b

    @visitor.when(ast.MultIndexNode)
    def visit(self, index, node: ast.MultIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a * b

    @visitor.when(ast.SubIndexNode)
    def visit(self, index, node: ast.SubIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a - b

    @visitor.when(ast.DivIndexNode)
    def visit(self, index, node: ast.DivIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a / b

    @visitor.when(ast.ModIndexNode)
    def visit(self, index, node: ast.ModIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a % b

    #################################################################
    #                                                               #
    #                 Binary Logical Operations                     #
    #                                                               #
    #################################################################

    @visitor.when(ast.AndIndexNode)
    def visit(self, index, node: ast.AndIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a and b

    @visitor.when(ast.OrIndexNode)
    def visit(self, index, node: ast.OrIndexNode):
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

    @visitor.when(ast.EqualIndexNode)
    def visit(self, index, node: ast.EqualIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a == b

    @visitor.when(ast.NotEqualIndexNode)
    def visit(self, index, node: ast.NotEqualIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a != b

    @visitor.when(ast.LessIndexNode)
    def visit(self, index, node: ast.LessIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a < b

    @visitor.when(ast.GreatIndexNode)
    def visit(self, index, node: ast.GreatIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a > b

    @visitor.when(ast.GreatEqualIndexNode)
    def visit(self, index, node: ast.GreatEqualIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a >= b

    @visitor.when(ast.LessEqualIndexNode)
    def visit(self, index, node: ast.LessEqualIndexNode):
        a = self.visit(index, node.a)
        b = self.visit(index, node.b)
        return a <= b
