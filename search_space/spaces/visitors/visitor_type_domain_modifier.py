from copy import copy
from search_space.errors import ArgumentFunctionError, NotEvaluateError
from search_space.spaces.asts.naturals_values.__base__ import NaturalValuesNode
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from . import VisitorLayer
from .visitor_natural_ast import NaturalAstVisitor


class TypeDomainModifierVisitor(VisitorLayer):
    def __init__(self) -> None:
        super().__init__()
        self.natural_visitor = NaturalAstVisitor()

    @property
    def do_transform_to_check_sample(self):
        return False

    def domain_optimization(self, node, domain):
        self.domain, self._context = domain, None
        return self.visit(node)

    def transform_to_modifier(self, node, domain, context):
        self.domain, self._context = domain, context
        return self.visit(node)

    def __op_apply__(self, a, b, op):
        if visitor.WithoutDispatcher in [type(a), type(b)]:
            return visitor.without_dispatcher

        if a is None:
            if b is None or isinstance(b, type):
                self.domain = op(self.domain, b)
            return None

        if b is None:
            if isinstance(b, type):
                self.domain = op(a, self.domain)
            return None

        return op(b, a)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node: constraints.AstRoot):

        for n in node.asts:
            self.visit(n)

        return node, self.domain

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(constraints.AndOp)
    def visit(self, node):
        a = self.visit(node.target)

        if type(a) == bool and not a:
            return

        b = self.visit(node.other)

        return self.__op_apply__(a, b, lambda a, b: a & b)

    @visitor.when(constraints.OrOp)
    def visit(self, node):
        current_domain = copy(self.domain)
        a = self.visit(node.target)

        if type(a) == bool and a:
            return

        current_domain, self.domain = self.domain, current_domain
        b = self.visit(node.other)

        if type(a) == bool and b is None:
            return

        return self.__op_apply__(a, b, lambda a, b: a | b)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.LessOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x < y)

    @visitor.when(constraints.LessOrEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x <= y)

    @visitor.when(constraints.GreatOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x > y)

    @visitor.when(constraints.GreatOrEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x >= y)

    @visitor.when(constraints.NotEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x != y)

    @visitor.when(constraints.EqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x == y)

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        pass

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):
        if isinstance(node.target, NaturalValuesNode):
            return self.natural_visitor.get_value(
                node.target, context=self._context
            )

        return node.target

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg)

        return node.func(*new_args, **new_kw)

    @visitor.when(constraints.AdvancedFunctionNode)
    def visit(self, node: constraints.FunctionNode):
        raise ArgumentFunctionError()

    @visitor.when(constraints.NotEvaluate)
    def visit(self, node):
        raise NotEvaluateError()
