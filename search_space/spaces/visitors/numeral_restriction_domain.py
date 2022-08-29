from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.errors import UnSupportOpError, NotEvaluateError
from search_space.context_manager import SamplerContext, ConstraintInfo


class NumeralRestrictionDomain:
    """
        Restriction := Const || Restriction
                     | Const && Restriction
                     | Const
              Const := self CmpOp naturalValue
                     | naturalValue CmpOp self
              CmpOp := < | <= | > | >=
    """

    def __init__(self, _min, _max, context: SamplerContext, space) -> None:
        self.min, self.max = _min, _max
        self.context = context
        self.space = space

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

    @visitor.when(ast.GreatEqual)
    def visit(self, node: ast.GreatEqual):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        a, b = max(self.min, limit), max(self.max, limit)
        self.context.push_log(ConstraintInfo(
            self.space, "GreatEqual", (self.min, self.max), (a, b)))

        self.min, self.max = a, b
        return self

    @visitor.when(ast.Great)
    def visit(self, node: ast.Great):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        a, b = max(self.min, limit), max(self.max, limit)
        self.context.push_log(ConstraintInfo(
            self.space, "Great", (self.min, self.max), (a, b)))

        self.min, self.max = a, b
        return self

    @visitor.when(ast.LessEqual)
    def visit(self, node: ast.LessEqual):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        a, b = min(self.min, limit), min(self.max, limit)
        self.context.push_log(ConstraintInfo(
            self.space, "LessEqual", (self.min, self.max), (a, b)))

        self.min, self.max = a, b
        return self

    @visitor.when(ast.Less)
    def visit(self, node: ast.Less):
        _ = self.visit(node.father)
        limit: float = self.visit(node.other)

        a, b = min(self.min, limit), min(self.max, limit)
        self.context.push_log(ConstraintInfo(
            self.space, "Less", (self.min, self.max), (a, b)))

        self.min, self.max = a, b
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
