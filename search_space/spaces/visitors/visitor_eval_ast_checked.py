from cProfile import label
from secrets import choice
from token import EXACT_TOKEN_TYPES
from search_space.errors import CircularDependencyDetected, InvalidSpaceDefinition, NotEvaluateError
from search_space.utils.singleton import Singleton
from ..asts import constraints
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from . import VisitorLayer
from .visitor_natural_ast import NaturalAstVisitor, NaturalValuesNode


class EvalAstChecked(VisitorLayer, metaclass=Singleton):
    SELF = 'self'
    NATURAL = 'natural'
    NOT_EVAL = 'not_eval'

    def __init__(self) -> None:
        super().__init__()
        self.natural_visitor = NaturalAstVisitor()

    def transform_to_modifier(self, node, domain=None, context=None):
        self.context = context
        return self.visit(node), domain

    def transform_to_check_sample(self, node, sample, context=None):
        return self.visit(node)

    def domain_optimization(self, node, domain):
        self.context = None
        return self.visit(node), domain

    def choice_result(self, a, b, two_self_func):
        if a == self.SELF and b == self.SELF:
            return two_self_func()
        if a == self.NOT_EVAL or b == self.NOT_EVAL:
            raise NotEvaluateError()
        # if not self.SELF in [a, b]:
        #     raise NotEvaluateError()

        return a if b == self.NATURAL else b

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node):
        result = constraints.AstRoot([])

        for n in node.asts:
            try:
                label, n = self.visit(n)
                if label == self.NATURAL:
                    continue

                result.add_constraint(n)
            except NotEvaluateError:
                pass

        return result

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node: constraints.UniversalVariableBinaryOperation):
        a, node_A = self.visit(node.target)
        b, node_B = self.visit(node.other)

        if isinstance(node, constraints.SegmentationExprNode):
            c, node_C = self.visit(node.value)

            s = list(set([a, b, c]))

            if (len(s) == 3):
                raise NotEvaluateError()

            def f():
                raise InvalidSpaceDefinition('Auto Constraint Definition')

            if len(s) == 1:
                if s[0] == self.SELF:
                    raise InvalidSpaceDefinition('Auto Constraint Definition')
                else:
                    raise NotEvaluateError()

            label = self.choice_result(s[0], s[1], f)
            n = type.__call__(node.__class__, node_A, node_B, node_C)
            return label, n

        def f():
            raise InvalidSpaceDefinition('Auto Constraint Definition')

        label = self.choice_result(a, b, f)
        result = type.__call__(node.__class__, node_A, node_B)
        # if a != self.SELF and b == self.SELF:
        #     result = node.inverted_op(node_A, node_B)
        # else:

        return label, result

    @visitor.when(constraints.EqualOp)
    def visit(self, node):
        a, node_A = self.visit(node.target)
        b, node_B = self.visit(node.other)

        def f():
            raise NotEvaluateError()

        return self.choice_result(a, b, f), constraints.EqualOp(node_A, node_B)

    @visitor.when(constraints.AndOp)
    def visit(self, node):
        a, node_A = self.visit(node.target)
        b, node_B = self.visit(node.other)

        def f():
            return self.SELF

        return self.choice_result(a, b, f), constraints.AndOp(node_A, node_B)

    @visitor.when(constraints.OrOp)
    def visit(self, node):
        a, node_A = self.visit(node.target)
        b, node_B = self.visit(node.other)

        def f():
            return self.SELF

        return self.choice_result(a, b, f), constraints.OrOp(node_A, node_B)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(constraints.GetItem)
    def visit(self, node):
        label, item = self.visit(node.target)
        return label, constraints.GetItem(item, node.other)

    @visitor.when(constraints.GetAttr)
    def visit(self, node):
        label, item = self.visit(node.target)
        return label, constraints.GetAttr(item, node.other)

    @visitor.when(constraints.FunctionNode)
    def visit(self, node: constraints.FunctionNode):
        tag_set, node_list = set(), []
        for arg in node.args:
            label, n = self.visit(arg)
            tag_set.add(label)
            node_list.append(n)

        kws = {}
        for name, arg in node.kwargs:
            label, n = self.visit(arg)
            tag_set.add(label)
            kws[name] = n

        if (
            len(tag_set) == 3
            or self.SELF in tag_set
            or self.NOT_EVAL in tag_set
        ):
            raise NotEvaluateError()

        return self.NATURAL, constraints.FunctionNode(node.func, node_list, kws)

    @visitor.when(constraints.AdvancedFunctionNode)
    def visit(self, node: constraints.AdvancedFunctionNode):
        tag_set, node_list, self_index = set(), [], node.args_target
        for i, arg in enumerate(node.args):
            label, n = self.visit(arg)
            tag_set.add(label)
            node_list.append(n)

            if i in self_index and label != self.SELF:
                self_index.remove(i)

        kws, self_kws = {}, node.kw_target
        for name, arg in node.kwargs:
            label, n = self.visit(arg)
            tag_set.add(label)
            kws[name] = n

            if name in self_kws and label != self.SELF:
                self_kws.remove(name)

        if (self.NOT_EVAL in tag_set):
            raise NotEvaluateError()

        if not (self.SELF in tag_set):
            return self.NATURAL, constraints.FunctionNode(node.func, node_list, kws)

        return self.NATURAL, constraints.AdvancedFunctionNode(
            (self_index, self_kws),
            node.func, node_list, kws,
            node.cls
        )

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        return self.SELF, node

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):

        if not self.context is None and isinstance(node.target, NaturalValuesNode):
            try:
                _ = self.natural_visitor.get_value(
                    node.target, context=self._context
                )
                return self.NATURAL, node
            except AttributeError:
                pass
            except CircularDependencyDetected:
                return self.NOT_EVAL, node

        return self.NATURAL, node

    @visitor.when(constraints.NotEvaluate)
    def visit(self, node):
        return self.NOT_EVAL, node
