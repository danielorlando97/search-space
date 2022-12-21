from threading import currentThread
from search_space.errors import CircularDependencyDetected, DetectedRuntimeDependency, InvalidSpaceConstraint, NotEvaluateError
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints, naturals_values
from . import VisitorLayer
from .visitor_natural_ast import NaturalAstVisitor, NaturalValuesNode


class IndexAstModifierVisitor(VisitorLayer):
    def __init__(self, space, index) -> None:
        self.current_index = index
        self.space = space
        self.natural_visitor = NaturalAstVisitor()

    def domain_optimization(self, node, domain):
        self.context = None
        return self.visit(node), domain

    def transform_to_modifier(self, node, domain=None, context=None):
        self.context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        self.context = context
        return self.visit(node, context=context)

    @visitor.on("node")
    def visit(self, node, current_index=[]):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node, current_index=[]):
        result = constraints.AstRoot([])

        for n in node.asts:
            result.add_constraint(self.visit(n, None))

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node, current_index):
        a = self.visit(node.target, current_index)
        b = self.visit(node.other, current_index)

        if isinstance(node, constraints.SegmentationExprNode):
            c = self.visit(node.value, current_index)
            return type.__call__(node.__class__, a, b, c)

        return type.__call__(node.__class__, a, b)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node, current_index):
        current_index = [] if current_index is None else current_index
        _slice = node.other.target

        if isinstance(_slice, slice):
            start, stop, steep = (
                self.visit(
                    constraints.NaturalValue(_slice.start),
                    current_index
                ),
                self.visit(
                    constraints.NaturalValue(_slice.stop),
                    current_index
                ),
                self.visit(
                    constraints.NaturalValue(_slice.step),
                    current_index
                )
            )
            try:
                if bool in [type(start.target), type(stop.target), type(steep.target)]:
                    raise InvalidSpaceConstraint(
                        'the slice dont support dynamic indexes')

                index = constraints.NaturalValue(
                    slice(start.target, stop.target, steep.target)
                )
            except AttributeError:
                return constraints.NotEvaluate()
        else:
            index = self.visit(node.other, current_index)
            try:
                if type(index.target) == bool:
                    index.target = self.current_index[-len(current_index) - 1]
            except AttributeError:
                return constraints.NotEvaluate()

        return self.visit(node.target, [index.target] + current_index)

    @visitor.when(constraints.SelfNode)
    def visit(self, node, current_index):
        if current_index is None:
            return node

        if len(current_index) == 0:
            return constraints.NotEvaluate()

        if tuple(current_index) == self.current_index:
            return node

        try:
            if self.context is None:
                return constraints.NaturalValue(
                    naturals_values.SpaceSelfNode(self.space[current_index])
                )

            value = self.space[current_index].get_sample(
                context=self.context)[0]
        except NotEvaluateError:
            return constraints.NotEvaluate()
        except CircularDependencyDetected:
            return constraints.NotEvaluate()

        return constraints.NaturalValue(value)

    @visitor.when(constraints.NaturalValue)
    def visit(self, node, current_index):

        if isinstance(node.target, NaturalValuesNode):
            try:
                result = self.natural_visitor.get_value(
                    node.target,
                    context=self.context,
                    current_index=self.current_index
                )
                return constraints.NaturalValue(result)
            except CircularDependencyDetected:
                return constraints.NotEvaluate()

        return node

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        return constraints.FunctionNode(node.func, new_args, new_kw)

    @visitor.when(constraints.AdvancedFunctionNode)
    def visit(self, node: constraints.AdvancedFunctionNode, current_index):
        new_args = []
        for arg in node.args:
            new_args.append(self.visit(arg, current_index))

        new_kw = {}
        for name, arg in node.kwargs:
            new_kw[name] = self.visit(arg, current_index)

        return constraints.AdvancedFunctionNode(
            (node.args_target, node.kw_target),
            node.func, new_args, new_kw,
            node.cls
        )
