from xml import dom
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, NotEvaluateError
from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
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

    @visitor.when(ast.AstRoot)
    def visit(self, node):
        result = ast.AstRoot([])

        for n in node.asts:
            result.add_constraint(
                self.visit(n))

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

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node):
        index = self.visit(node.other)
        target = self.visit(node.target)

        return ast.GetItem(target, index)

    @visitor.when(ast.GetAttr)
    def visit(self, node: ast.GetAttr):
        target = self.visit(node.target)
        other = self.visit(node.other)

        if target.is_self and isinstance(other, ast.NaturalValue):
            if other.target == self.member:
                return target
            else:
                return ast.NaturalValue(self.space[other])

        return ast.GetAttr(target, other)

    @visitor.when(ast.SelfNode)
    def visit(self, node):
        return node

    @visitor.when(ast.NaturalValue)
    def visit(self, node):
        try:
            return ast.NaturalValue(node.target.get_sample(context=self.context)[0])
        except AttributeError:
            pass
        except TypeError:
            pass

        return ast.NaturalValue(node.target)
