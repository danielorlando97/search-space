from search_space.errors import CircularDependencyDetected, NotEvaluateError
from . import ast
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import VisitorLayer


class MemberAstModifierVisitor(VisitorLayer):
    def __init__(self, space, member) -> None:
        self.member = member
        self.space = space

    def transform_to_modifier(self, node, domain=None, context=None):
        return self.visit(node, context=context), domain

    def transform_to_check_sample(self, node, sample, context=None):
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node, context=None):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node, context=None):
        result = ast.AstRoot()

        for n in node.asts:
            result.add_constraint(
                self.visit(n, context=context))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.UniversalVariableBinaryOperation)
    def visit(self, node, context):
        a = self.visit(node.target, context=context)
        b = self.visit(node.other,  context=context)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetAttr)
    def visit(self, node: ast.GetAttr, context):
        target = self.visit(node.target, context)
        other = self.visit(node.other, context)

        if target.is_self and isinstance(other, ast.NaturalValue):
            if other.target == self.member:
                return target
            else:
                return ast.NaturalValue(self.space[other])

        return ast.GetAttr(target, other)

    @visitor.when(ast.SelfNode)
    def visit(self, node, context):
        return node

    @visitor.when(ast.NaturalValue)
    def visit(self, node,  context):
        try:
            return ast.NaturalValue(node.target.get_sample(context=context)[0])
        except AttributeError:
            return ast.NaturalValue(node.target)
