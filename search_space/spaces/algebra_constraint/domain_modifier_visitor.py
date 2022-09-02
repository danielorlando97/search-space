from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast


class DomainModifierVisitor:
    def __init__(self, domain) -> None:
        self.domain = domain

    @visitor.on("node")
    def visit(self, node, context):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node: ast.AstRoot, context):
        for n in node.asts:
            self.visit(n, context)

        return self.domain

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def visit(self, node: ast.LessOp, context):
        _ = self.visit(node.target, context)
        limit = self.visit(node.other, context)

        self.domain = self.domain < limit

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfNode)
    def visit(self, node: ast.SelfNode, context):
        pass

    @visitor.when(ast.NaturalValue)
    def visit(self, node: ast.NaturalValue, context):
        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target
