from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import InvalidSampler
from .index_solution import IndexSolutionVisitor
from search_space.spaces.ast_index import AstIndexNode
from .ast_solution import AstSolution


class ValidateSampler:
    def __init__(self, context, space) -> None:
        self.context = context
        self.space = space
        self.index_solution = IndexSolutionVisitor(self.context)
        self.ast_solution = AstSolution(context)

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

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.ConditionalConstraint)
    def visit(self, sampler, node: ast.ConditionalConstraint):
        bool_: bool = self.ast_solution.visit(sampler, node.condition)
        if bool_:
            self.visit(sampler, node.father)

        return self

    @visitor.when(ast.GreatEqual)
    def visit(self, sampler, node: ast.GreatEqual):
        no_eval_node = self.check_is_not_eval_node(node.father, node.other)
        if not no_eval_node is None:
            return no_eval_node

        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a >= b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} >= {b}")

    @visitor.when(ast.Great)
    def visit(self, sampler, node: ast.Great):
        no_eval_node = self.check_is_not_eval_node(node.father, node.other)
        if not no_eval_node is None:
            return no_eval_node

        a = self.visit(sampler, node.father)
        b = self.visit(sampler, node.other)

        if a > b:
            return self

        raise InvalidSampler(
            f"{self.space.scope}[{sampler}]: inconsistent {a} > {b}")

    @visitor.when(ast.LessEqual)
    def visit(self, sampler, node: ast.LessEqual):
        no_eval_node = self.check_is_not_eval_node(node.father, node.other)
        if not no_eval_node is None:
            return no_eval_node

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

    @visitor.when(ast.GetAttribute)
    def visit(self, sampler, node: ast.GetAttribute):
        self.visit(sampler, node.father)

        result = self.context.get_sampler_value(self.space.__dict__[node.name])
        if result is None:
            return ast.NoEvaluate()

        return result

    @visitor.when(ast.SelfValue)
    def visit(self, sampler, node: ast.SelfValue):
        return sampler

    @visitor.when(ast.NaturalValue)
    def visit(self, sampler, node: ast.NaturalValue):
        try:
            return node.other.get_sampler(context=self.context)[0]
        except AttributeError:
            return node.other
