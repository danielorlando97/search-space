from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.errors import InvalidSampler


class ValidateSampler:
    def __init__(self, context) -> None:
        self.context = context

    def check_is_not_eval_node(self, *nodes):
        for node in nodes:
            try:
                if not node.can_evaluate:
                    return node
            except AttributeError:
                pass
        return None

    @visitor.on("node")
    def visit(self, sample, node):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, sample, node: ast.AstRoot):
        for n in node.asts:
            self.visit(sample, n)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def visit(self, sampler, node: ast.LessOp):

        a = self.visit(sampler, node.target)
        b = self.visit(sampler, node.other)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfNode)
    def visit(self, sampler, node: ast.SelfNode):
        return sampler

    @visitor.when(ast.NaturalValue)
    def visit(self, sampler, node: ast.NaturalValue):
        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target
