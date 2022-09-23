from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.errors import InvalidSampler
from . import VisitorLayer
from search_space.utils.singleton import Singleton
from search_space.spaces.algebra_constraint.functions_and_predicates import FunctionNode, AdvancedFunctionNode


class ValidateSampler(VisitorLayer, metaclass=Singleton):
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

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node):
        for n in node.asts:
            self.visit(n)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def visit(self, node):

        a = self.visit(node.target)
        b = self.visit(node.other)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.LessOrEqualOp)
    def visit(self, node):

        a = self.visit(node.target)
        b = self.visit(node.other)

        if a <= b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.GreatOp)
    def visit(self, node):

        a = self.visit(node.target)
        b = self.visit(node.other)

        if a > b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.GreatOrEqualOp)
    def visit(self, node):

        a = self.visit(node.target)
        b = self.visit(node.other)

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
    def visit(self, node: ast.GetItem):

        a = self.visit(node.target)
        b = self.visit(node.other)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @ visitor.when(ast.SelfNode)
    def visit(self, node):
        return self.sample

    @ visitor.when(ast.NaturalValue)
    def visit(self, node):
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
