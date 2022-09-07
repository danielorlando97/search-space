from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from . import VisitorLayer
from search_space.utils.singleton import Singleton


class DomainModifierVisitor(VisitorLayer):
    @property
    def do_transform_to_check_sample(self):
        return False

    @visitor.on("node")
    def transform_to_modifier(self, node, domain=None, context=None):
        pass

    @visitor.when(ast.AstRoot)
    def transform_to_modifier(self, node: ast.AstRoot, domain, context):
        self.domain = domain

        for n in node.asts:
            self.transform_to_modifier(n, context=context)

        return node, self.domain

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def transform_to_modifier(self, node, domain=None, context=None):
        _ = self.transform_to_modifier(node.target, context=context)
        limit = self.transform_to_modifier(node.other, context=context)

        self.domain = self.domain < limit

    @visitor.when(ast.LessOrEqualOp)
    def transform_to_modifier(self, node, domain=None, context=None):
        _ = self.transform_to_modifier(node.target, context=context)
        limit = self.transform_to_modifier(node.other, context=context)

        self.domain = self.domain <= limit

    @visitor.when(ast.GreatOp)
    def transform_to_modifier(self, node, domain=None, context=None):
        _ = self.transform_to_modifier(node.target, context=context)
        limit = self.transform_to_modifier(node.other, context=context)

        self.domain = self.domain > limit

    @visitor.when(ast.GreatOrEqualOp)
    def transform_to_modifier(self, node, domain=None, context=None):
        _ = self.transform_to_modifier(node.target, context=context)
        limit = self.transform_to_modifier(node.other, context=context)

        self.domain = self.domain >= limit

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfNode)
    def transform_to_modifier(self, node, domain=None, context=None):
        pass

    @visitor.when(ast.NaturalValue)
    def transform_to_modifier(self, node, domain=None, context=None):
        try:
            return node.target.get_sample(context=context)[0]
        except AttributeError:
            return node.target
