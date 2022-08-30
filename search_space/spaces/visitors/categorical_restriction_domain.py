from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import UnSupportOpError, NotEvaluateError
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.spaces import visitors


class CategoricalRestrictionDomain:
    """

    """

    def __init__(self, domain, context: SamplerContext, space) -> None:
        self.domain = domain
        self.context = context
        self.space = space
        self.solution = visitors.AstSolution(context)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.UniversalVariable)
    def visit(self, node):
        raise UnSupportOpError(self, node, "transform")

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.ConditionalConstraint)
    def visit(self, node: ast.ConditionalConstraint):
        bool_: bool = self.solution.visit(node.condition)
        if bool_:
            self.visit(node.father)

        return self

    @visitor.when(ast.GreatEqual)
    def visit(self, node: ast.GreatEqual):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item >= limit]
        self.context.push_log(ConstraintInfo(
            self.space, "GreatEqual", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    @visitor.when(ast.Great)
    def visit(self, node: ast.Great):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item > limit]
        self.context.push_log(ConstraintInfo(
            self.space, "Great", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    @visitor.when(ast.LessEqual)
    def visit(self, node: ast.LessEqual):

        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item <= limit]
        self.context.push_log(ConstraintInfo(
            self.space, "LessEqual", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    @visitor.when(ast.Less)
    def visit(self, node: ast.Less):

        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item < limit]
        self.context.push_log(ConstraintInfo(
            self.space, "Less", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    @visitor.when(ast.NotEqualSegmentation)
    def visit(self, node: ast.NotEqualSegmentation):

        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item != limit]
        self.context.push_log(ConstraintInfo(
            self.space, "Less", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    @visitor.when(ast.Equal)
    def visit(self, node: ast.Equal):

        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        new_domain = [item for item in self.domain if item == limit]
        self.context.push_log(ConstraintInfo(
            self.space, "Less", (self.domain,), (new_domain,)))

        self.domain = new_domain
        return self

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.SelfValue)
    def visit(self, node: ast.SelfValue):
        return self

    @visitor.when(ast.NoEvaluate)
    def visit(self, node: ast.NoEvaluate):
        raise NotEvaluateError()

    @visitor.when(ast.NaturalValue)
    def visit(self, node: ast.NaturalValue):
        try:
            return node.other.get_sampler(context=self.context)[0]
        except AttributeError:
            return node.other
