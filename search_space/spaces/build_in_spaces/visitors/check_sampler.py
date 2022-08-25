from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import InvalidSampler

class ValidateSampler:
    def __init__(self, context, space) -> None:
        self.context = context
        self.space = space

    @visitor.on("node")
    def visit(self, sample, node):
        pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def visit(self, sampler, node: ast.GreatEqual):
        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a >= b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} >= {b}")

    @visitor.when(ast.Great)
    def visit(self, sampler, node: ast.Great):
        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a > b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} > {b}")


    @visitor.when(ast.LessEqual)
    def visit(self, sampler, node: ast.LessEqual):
        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a <= b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} <= {b}")


    @visitor.when(ast.Less)
    def visit(self, sampler, node: ast.Less):
        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a < b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} < {b}")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def visit(self, sampler, node: ast.SelfValue):
        return sampler

    @visitor.when(ast.NaturalValue)
    def visit(self, sampler, node: ast.NaturalValue):
        try:
            return node.other.get_sampler(context=self.context)[0]
        except AttributeError:
            return node.other
