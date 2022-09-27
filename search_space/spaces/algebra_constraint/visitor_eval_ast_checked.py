from token import EXACT_TOKEN_TYPES
from search_space.errors import CircularDependencyDetected, InvalidSpaceDefinition, NotEvaluateError
from search_space.utils.singleton import Singleton
from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import ast_index
from . import VisitorLayer


class EvalAstChecked(VisitorLayer, metaclass=Singleton):
    SELF = 'self'
    NATURAL = 'natural'
    NOT_EVAL = 'not_eval'

    def transform_to_modifier(self, node, domain=None, context=None):
        self.context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        return self.visit(node)

    def domain_optimization(self, node, domain):
        self.context = None
        return self.visit(node), domain

    def choice_result(self, a, b, two_self_func):
        if a == self.SELF and b == self.SELF:
            return two_self_func()
        if a == self.NOT_EVAL or b == self.NOT_EVAL:
            raise NotEvaluateError()
        if not self.SELF in [a, b]:
            raise NotEvaluateError()

        return a if b == self.NATURAL else b

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node):
        result = ast.AstRoot([])

        for n in node.asts:
            try:
                _ = self.visit(n)
                result.add_constraint(n)
            except NotEvaluateError:
                pass

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.UniversalVariableBinaryOperation)
    def visit(self, node):
        a = self.visit(node.target)
        b = self.visit(node.other)

        def f():
            raise InvalidSpaceDefinition('Auto Constraint Definition')

        return self.choice_result(a, b, f)

    @visitor.when(ast.EqualOp)
    def visit(self, node):
        a = self.visit(node.target)
        b = self.visit(node.other)

        def f():
            raise NotEvaluateError()

        return self.choice_result(a, b, f)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node):
        return self.visit(node.target)

    @visitor.when(ast.SelfNode)
    def visit(self, node):
        return self.SELF

    @visitor.when(ast.NaturalValue)
    def visit(self, node):
        if not self.context is None:
            try:
                return node.target.get_sample(context=self.context)[0]
            except AttributeError:
                pass
            except CircularDependencyDetected:
                return self.NOT_EVAL

        return self.NATURAL

    @visitor.when(ast.NotEvaluate)
    def visit(self, node):
        return self.NOT_EVAL
