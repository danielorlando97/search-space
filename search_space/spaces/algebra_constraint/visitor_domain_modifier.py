from copy import copy
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, NotEvaluateError, UnSupportOpError
from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.spaces.algebra_constraint.functions_and_predicates import FunctionNode, AdvancedFunctionNode
from . import VisitorLayer
from search_space.utils.singleton import Singleton


class DomainModifierVisitor(VisitorLayer):
    @property
    def do_transform_to_check_sample(self):
        return False

    @property
    def context(self):
        try:
            if self._context != None:
                return self._context
        except AttributeError:
            pass

        raise DetectedRuntimeDependency()

    def domain_optimization(self, node, domain):
        self.domain, self._context = domain, None
        return self.visit(node)

    def transform_to_modifier(self, node, domain, context):
        self.domain, self._context = domain, context
        return self.visit(node)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.AstRoot)
    def visit(self, node: ast.AstRoot):

        for n in node.asts:
            self.visit(n)

        return node, self.domain

    #################################################################
    #                                                               #
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    @visitor.when(ast.ModOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target % limit

        self.domain = self.domain % limit

    @visitor.when(ast.AddOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target + limit

        self.domain = self.domain + limit

    @visitor.when(ast.SubOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target - limit

        self.domain = self.domain - limit

    @visitor.when(ast.MultiOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target * limit

        self.domain = self.domain * limit

    @visitor.when(ast.DivOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target / limit

        self.domain = self.domain / limit

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(ast.AndOp)
    def visit(self, node):
        a = self.visit(node.target)

        if type(a) == bool and not a:
            return

        b = self.visit(node.other)

        if not None in [a, b]:
            return target and limit

    @visitor.when(ast.OrOp)
    def visit(self, node):
        current_domain = copy(self.domain)
        a = self.visit(node.target)

        if type(a) == bool and a:
            return

        current_domain, self.domain = self.domain, current_domain
        b = self.visit(node.other)

        if not None in [a, b]:
            return target or limit

        self.domain = self.domain | current_domain

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################
    @visitor.when(ast.LessOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target < limit

        self.domain = self.domain < limit

    @visitor.when(ast.LessOrEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target <= limit

        self.domain = self.domain <= limit

    @visitor.when(ast.GreatOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target > limit

        self.domain = self.domain > limit

    @visitor.when(ast.GreatOrEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target >= limit

        self.domain = self.domain >= limit

    @visitor.when(ast.NotEqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target != limit

        self.domain = self.domain != limit

    @visitor.when(ast.EqualOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        if not None in [target, limit]:
            return target == limit

        self.domain = self.domain == limit

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    # @visitor.when(ast.GetAttr)
    # def visit(self, node):
    #     raise UnSupportOpError(self.domain, '', 'GetAttr')

    # @visitor.when(ast.GetItem)
    # def visit(self, node):
    #     raise UnSupportOpError(self.domain, 1, 'GetItem')

    @visitor.when(ast.SelfNode)
    def visit(self, node):
        pass

    @visitor.when(ast.NaturalValue)
    def visit(self, node):

        try:
            return node.target.get_sample(context=self.context)[0]
        except AttributeError:
            return node.target

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg)

        return node.func(*new_args, **new_kw)

    @visitor.when(ast.NotEvaluate)
    def visit(self, node):
        raise NotEvaluateError()
