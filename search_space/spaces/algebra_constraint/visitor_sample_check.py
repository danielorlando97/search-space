from token import EXACT_TOKEN_TYPES
from search_space.spaces.algebra_constraint.visitor_index_ast_modifier import IndexSolutionVisitor
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.errors import InvalidSampler, NotEvaluateError
from . import VisitorLayer
from search_space.utils.singleton import Singleton
from search_space.spaces.algebra_constraint.functions_and_predicates import FunctionNode, AdvancedFunctionNode
from . import ast_index


class ValidateSampler(VisitorLayer, metaclass=Singleton):

    def __init__(self) -> None:
        self.index_solution = IndexSolutionVisitor()

    def check_is_not_eval_node(self, *nodes):
        for node in nodes:
            try:
                if not node.can_evaluate:
                    return node
            except AttributeError:
                pass
        return None

    @property
    def do_transform_to_modifier(self):
        return False

    def transform_to_check_sample(self, node, sample, context):
        self.sample, self.context = sample, context
        return self.visit(node)

    def check_sample_by_index(self, node, sample, context, index):
        self.current_index = index
        return self.transform_to_check_sample(node, sample, context)

    @visitor.on("node")
    def visit(self, node, current_index=[]):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node, current_index=[]):
        for n in node.asts:
            try:
                self.visit(n, current_index)
            except NotEvaluateError:
                pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.LessOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if a <= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.GreatOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if a > b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.GreatOrEqualOp)
    def visit(self, node, current_index=[]):

        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if a >= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def visit(self, node: ast.GetItem, current_index=[]):

        b = self.visit(node.other, current_index)
        return self.visit(node.target, current_index + [b])

    @ visitor.when(ast.SelfNode)
    def visit(self, node, current_index=[]):
        if len(current_index) == 0:
            return self.sample
        try:
            result = self.sample
            for i in current_index:
                result = result[i]

            return result
        except IndexError:
            raise NotEvaluateError()
        except TypeError:
            raise InvalidSampler(
                f"inconsistent sampler => {a} isn't indexed")

    @ visitor.when(ast.NaturalValue)
    def visit(self, node, current_index=[]):
        if isinstance(node.target, ast_index.IndexNode):
            result = self.index_solution.visit(
                self.current_index, node.target, self.context)
            if type(result) == type(bool()):
                return self.current_index[-len(current_index) - 1]
            else:
                return result

        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target
        except TypeError:
            pass

    @ visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg)

        return node.func(*new_args, **new_kw)
