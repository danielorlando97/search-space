from xml import dom
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, NotEvaluateError
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints, naturals_values
from . import VisitorLayer
from .visitor_natural_ast import NaturalAstVisitor, NaturalValuesNode


class MemberAstModifierVisitor(VisitorLayer):
    def __init__(self, space, member) -> None:
        self.member = member
        self.space = space
        self.natural_visitor = NaturalAstVisitor()

    @property
    def context(self):
        try:
            if self._context != None:
                return self._context
        except AttributeError:
            pass

        raise DetectedRuntimeDependency()

    def domain_optimization(self, node, domain):
        self._context = None
        return self.visit(node), domain

    def transform_to_modifier(self, node, domain=None, context=None):
        self._context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        self._context = context
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node):
        result = constraints.AstRoot([])

        for n in node.asts:
            result.add_constraint(
                self.visit(n))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node):
        a = self.visit(node.target)
        b = self.visit(node.other)

        if isinstance(node, constraints.SegmentationExprNode):
            c = self.visit(node.value)
            return type.__call__(node.__class__, a, b, c)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node):
        index = self.visit(node.other)
        target = self.visit(node.target)

        if type(index.target) == bool:
            return target

        return constraints.GetItem(target, index)

    @visitor.when(constraints.GetAttr)
    def visit(self, node: constraints.GetAttr):
        target = self.visit(node.target)
        other = self.visit(node.other)

        if target.is_self and isinstance(other, constraints.NaturalValue):
            if other.target == self.member:
                return target
            else:
                return constraints.NaturalValue(naturals_values.SpaceSelfNode(self.space[other.target]))

        return constraints.GetAttr(target, other)

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        return node

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):
        if isinstance(node.target, NaturalValuesNode):
            try:
                result = self.natural_visitor.get_value(
                    node.target, context=self._context
                )
                return constraints.NaturalValue(result)
            except CircularDependencyDetected:
                return constraints.NotEvaluate()

        return node

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg)

        return constraints.FunctionNode(node.func, new_args, new_kw)

    @visitor.when(constraints.AdvancedFunctionNode)
    def visit(self, node: constraints.AdvancedFunctionNode):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg)

        return constraints.AdvancedFunctionNode(
            (node.args_target, node.kw_target),
            node.func, new_args, new_kw,
            node.cls
        )
