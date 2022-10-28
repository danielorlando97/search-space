from copy import copy
from search_space.errors import ArgumentFunctionError, NotEvaluateError
from search_space.spaces.asts.naturals_values.__base__ import NaturalValuesNode
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from . import VisitorLayer
from .visitor_natural_ast import NaturalAstVisitor


class DomainModifierVisitor(VisitorLayer):
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
        if a is None:
            self.domain = op(self.domain, b)

        elif b is None:
            self.domain = op(a, self.domain)

        else:
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
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    @visitor.when(constraints.AddOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x + y)

    @visitor.when(constraints.SubOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x - y)

    @visitor.when(constraints.MultiOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x * y)

    @visitor.when(constraints.DivOp)
    def visit(self, node):
        target = self.visit(node.target)
        limit = self.visit(node.other)

        return self.__op_apply__(target, limit, lambda x, y: x / y)

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

        if not None in [a, b]:
            return target and limit

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

        if not None in [a, b]:
            return target or limit

        self.domain = self.domain | current_domain

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

    #################################################################
    #                                                               #
    #                 Segmentation Visit                            #
    #                                                               #
    #################################################################

    @visitor.when(constraints.SegmentationEqualOp)
    def visit(self, node: constraints.SegmentationEqualOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor == value

        self.domain = self.domain.__mod_eq__(factor, value)

    @visitor.when(constraints.SegmentationNotEqualOp)
    def visit(self, node: constraints.SegmentationNotEqualOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor != value

        self.domain = self.domain.__mod_neq__(factor, value)

    @visitor.when(constraints.SegmentationLessOp)
    def visit(self, node: constraints.SegmentationLessOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor < value

        self.domain = self.domain.__mod_lt__(factor, value)

    @visitor.when(constraints.SegmentationLessOrEqualOp)
    def visit(self, node: constraints.SegmentationLessOrEqualOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor <= value

        self.domain = self.domain.__mod_le__(factor, value)

    @visitor.when(constraints.SegmentationGreatOp)
    def visit(self, node: constraints.SegmentationGreatOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor > value

        self.domain = self.domain.__mod_gt__(factor, value)

    @visitor.when(constraints.SegmentationGreatOrEqualOp)
    def visit(self, node: constraints.SegmentationGreatOrEqualOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)
        value = self.visit(node.value)

        if not target is None:
            return target % factor >= value

        self.domain = self.domain.__mod_ge__(factor, value)

    @visitor.when(constraints.SegmentationAddOp)
    def visit(self, node: constraints.SegmentationAddOp):
        target = self.visit(node.target)
        factor = self.visit(node.value)

        if not target is None:
            return target + factor

        self.domain = self.domain.__mod_add__(factor, 0)

    @visitor.when(constraints.SegmentationSubOp)
    def visit(self, node: constraints.SegmentationSubOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)

        if not target is None:
            return target - factor

        self.domain = self.domain.__mod_sub__(factor, 0)

    @visitor.when(constraints.SegmentationMultiOp)
    def visit(self, node: constraints.SegmentationMultiOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)

        if not target is None:
            return target * factor

        self.domain = self.domain.__mod_mult__(factor, 0)

    @visitor.when(constraints.SegmentationDivOp)
    def visit(self, node: constraints.SegmentationDivOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)

        if not target is None:
            return target / factor

        self.domain = self.domain.__mod_div__(factor, 0)

    @visitor.when(constraints.SegmentationModOp)
    def visit(self, node: constraints.SegmentationModOp):
        target = self.visit(node.target)
        factor = self.visit(node.other)

        if not target is None:
            return target % factor

        self.domain = self.domain.__mod_eq__(factor, 0)

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    # @visitor.when(constraints.GetAttr)
    # def visit(self, node: constraints.GetAttr):
    #     target = self.visit(node.target)
    #     other = self.visit(node.other)

    #     return target.__dict__[other]

    @visitor.when(constraints.GetItem)
    def visit(self, node: constraints.GetItem):
        target = self.visit(node.target)
        other = self.visit(node.other)

        return target[other]

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
