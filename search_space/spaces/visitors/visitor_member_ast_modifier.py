from xml import dom
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, NotEvaluateError
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from . import VisitorLayer


class MemberAstModifierVisitor(VisitorLayer):
    def __init__(self, space, member) -> None:
        self.member = member
        self.space = space

    @property
    def context(self):
        try:
            if self._context != None:
                return self._context
        except AttributeError:
            pass

        raise DetectedRuntimeDependency()

    def domain_optimization(self, node, domain):
        self._context = None
        return self.visit(node), domain

    def transform_to_modifier(self, node, domain=None, context=None):
        self._context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        self._context = context
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node):
        result = constraints.AstRoot([])

        for n in node.asts:
            result.add_constraint(
                self.visit(n))

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

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node):
        index = self.visit(node.other)
        target = self.visit(node.target)

        return constraints.GetItem(target, index)

    @visitor.when(constraints.GetAttr)
    def visit(self, node: constraints.GetAttr):
        target = self.visit(node.target)
        other = self.visit(node.other)

        if target.is_self and isinstance(other, constraints.NaturalValue):
            if other.target == self.member:
                return target
            else:
                return constraints.NaturalValue(self.space[other.target])

        return constraints.GetAttr(target, other)

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        return node

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):
        try:
            _ = node.target.get_sample
        except AttributeError:
            return constraints.NaturalValue(node.target)

        try:
            return constraints.NaturalValue(node.target.get_sample(self.context)[0])
        except CircularDependencyDetected:
            return constraints.NotEvaluate()
