from search_space.errors import DetectedRuntimeDependency
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import VisitorLayer
from search_space.utils.singleton import Singleton


class DomainModifierVisitor(VisitorLayer):
    @property
    def do_transform_to_check_sample(self):
        return False

    @property
    def context(self):
        try:
            if self._context != None:
                return self._context
        except AttributeError:
            pass

        raise DetectedRuntimeDependency()

    def domain_optimization(self, node, domain):
        self.domain, self._context = domain, None
        return self.visit(node)

    def transform_to_modifier(self, node, domain, context):
        self.domain, self._context = domain, context
        return self.visit(node)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node: ast.AstRoot):

        for n in node.asts:
            self.visit(n)

        return node, self.domain

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def visit(self, node):
        _ = self.visit(node.target)
        limit = self.visit(node.other)

        self.domain = self.domain < limit

    @visitor.when(ast.LessOrEqualOp)
    def visit(self, node):
        _ = self.visit(node.target)
        limit = self.visit(node.other)

        self.domain = self.domain <= limit

    @visitor.when(ast.GreatOp)
    def visit(self, node):
        _ = self.visit(node.target)
        limit = self.visit(node.other)

        self.domain = self.domain > limit

    @visitor.when(ast.GreatOrEqualOp)
    def visit(self, node):
        _ = self.visit(node.target)
        limit = self.visit(node.other)

        self.domain = self.domain >= limit

    @visitor.when(ast.NotEqualOp)
    def visit(self, node):
        _ = self.visit(node.target)
        limit = self.visit(node.other)

        self.domain = self.domain != limit

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfNode)
    def visit(self, node):
        pass

    @visitor.when(ast.NaturalValue)
    def visit(self, node):

        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target
