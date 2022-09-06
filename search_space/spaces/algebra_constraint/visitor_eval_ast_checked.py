from search_space.errors import CircularDependencyDetected, NotEvaluateError
from search_space.utils.singleton import Singleton
from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import ast_index
from . import VisitorLayer


class EvalAstChecked(VisitorLayer, metaclass=Singleton):

    def transform_to_modifier(self, node, domain=None, context=None):
        return self.visit(node, context=context), domain

    def transform_to_check_sample(self, node, sample, context=None):
        return self.visit(node, context=context)

    def choice_result(self, a, b):
        if a is None:
            return b
        if b is None:
            return a
        return a and b

    @visitor.on("node")
    def visit(self, node, context=None):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node, context=None):
        result = ast.AstRoot()

        for n in node.asts:
            if self.visit(n, context):
                result.add_constraint(n, context)

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.UniversalVariableBinaryOperation)
    def visit(self, node, context):
        a = self.visit(node.target, context=context)
        b = self.visit(node.other, context=context)

        return self.choice_result(a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node, context):
        return self.visit(node.target, context)

    @visitor.when(ast.SelfNode)
    def visit(self, node, context):
        return True

    @visitor.when(ast.NaturalValue)
    def visit(self, node, context):
        return None

    @visitor.when(ast.NotEvaluate)
    def visit(self, node, context):
        return False
