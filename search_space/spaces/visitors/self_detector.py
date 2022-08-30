from tokenize import Single
from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import InvalidSampler
from .index_solution import IndexSolutionVisitor
from search_space.spaces.ast_index import AstIndexNode
from search_space.utils.singleton import Singleton


class SelfDetector(metaclass=Singleton):

    @visitor.on("node")
    def visit(self, node):
        pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def visit(self, node: ast.GreatEqual):
        a: bool = self.visit(node.father)
        b: bool = self.visit(node.other)

        return a or b

    @visitor.when(ast.Great)
    def visit(self, node: ast.Great):
        a: bool = self.visit(node.father)
        b: bool = self.visit(node.other)

        return a or b

    @visitor.when(ast.LessEqual)
    def visit(self, node: ast.LessEqual):
        a: bool = self.visit(node.father)
        b: bool = self.visit(node.other)

        return a or b

    @visitor.when(ast.Less)
    def visit(self, node: ast.Less):
        a: bool = self.visit(node.father)
        b: bool = self.visit(node.other)

        return a or b

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetAttribute)
    def visit(self, node: ast.GetAttribute):
        return self.visit(node.father)

    @visitor.when(ast.SelfValue)
    def visit(self, node: ast.SelfValue):
        return True

    @visitor.when(ast.NaturalValue)
    def visit(self, node: ast.NaturalValue):
        return False
