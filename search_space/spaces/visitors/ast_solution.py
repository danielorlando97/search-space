from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import UnSupportOpError, NotEvaluateError
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.utils.singleton import Singleton


class AstSolution():

    def __init__(self, context: SamplerContext) -> None:
        self.context = context

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.UniversalVariable)
    def visit(self, node):
        raise UnSupportOpError(self, node, "transform")

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def visit(self, node: ast.GreatEqual):
        a = self.visit(node.father)
        b = self.visit(node.other)

        return a >= b

    @visitor.when(ast.Great)
    def visit(self, node: ast.Great):
        a = self.visit(node.father)
        b = self.visit(node.other)

        return a > b

    @visitor.when(ast.LessEqual)
    def visit(self, node: ast.LessEqual):
        a = self.visit(node.father)
        b = self.visit(node.other)

        return a <= b

    @visitor.when(ast.Less)
    def visit(self, node: ast.Less):
        a = self.visit(node.father)
        b = self.visit(node.other)

        return a < b
    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.NoEvaluate)
    def visit(self, node: ast.NoEvaluate):
        raise NotEvaluateError()

    @visitor.when(ast.NaturalValue)
    def visit(self, node: ast.NaturalValue):
        try:
            return node.other.get_sampler(context=self.context)[0]
        except AttributeError:
            return node.other
