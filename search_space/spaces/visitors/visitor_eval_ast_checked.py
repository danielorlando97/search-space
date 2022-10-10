from secrets import choice
from token import EXACT_TOKEN_TYPES
from search_space.errors import CircularDependencyDetected, InvalidSpaceDefinition, NotEvaluateError
from search_space.utils.singleton import Singleton
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints
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

    @visitor.when(constraints.AstRoot)
    def visit(self, node):
        result = constraints.AstRoot([])

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

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node):
        a = self.visit(node.target)
        b = self.visit(node.other)

        def f():
            raise InvalidSpaceDefinition('Auto Constraint Definition')

        return self.choice_result(a, b, f)

    @visitor.when(constraints.EqualOp)
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

    @visitor.when(constraints.GetItem)
    def visit(self, node):
        return self.visit(node.target)

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode):
        tag_set = set()
        for arg in node.args:
            tag_set.add(self.visit(arg))

        for name, arg in node.kwargs:
            tag_set.add(self.visit(arg))

        if (
            len(tag_set) == 3
            or self.SELF in tag_set
            or self.NOT_EVAL in tag_set
        ):
            raise NotEvaluateError()

        return self.NATURAL

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        return self.SELF

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):
        if not self.context is None:
            try:
                _ = node.target.get_sample(context=self.context)
                return self.NATURAL
            except AttributeError:
                pass
            except CircularDependencyDetected:
                return self.NOT_EVAL

        return self.NATURAL

    @visitor.when(constraints.NotEvaluate)
    def visit(self, node):
        return self.NOT_EVAL
