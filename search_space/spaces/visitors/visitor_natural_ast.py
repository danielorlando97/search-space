from search_space.errors import DetectedRuntimeDependency
from . import VisitorLayer
from search_space.utils import visitor
from search_space.spaces.asts import naturals_values
from search_space.spaces.asts.naturals_values import NaturalValuesNode


class NaturalAstVisitor:
    def get_value(self, node, current_index=[], context=None):
        self.current_index, self._context = current_index, context
        return self.visit(node)

    @property
    def context(self):
        try:
            if self._context != None:
                return self._context
        except AttributeError:
            pass

        raise DetectedRuntimeDependency()

    @visitor.on("node")
    def visit(self, node):
        pass

    #################################################################
    #                                                               #
    #                 Arithmetic Visit                              #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.ModOp)
    def visit(self, node: naturals_values.ModOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a % b

    @visitor.when(naturals_values.AddOp)
    def visit(self, node: naturals_values.AddOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a + b

    @visitor.when(naturals_values.SubOp)
    def visit(self, node: naturals_values.SubOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a - b

    @visitor.when(naturals_values.MultiOp)
    def visit(self, node: naturals_values.MultiOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a * b

    @visitor.when(naturals_values.DivOp)
    def visit(self, node: naturals_values.DivOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a / b

    #################################################################
    #                                                               #
    #                  Logic Visit                                  #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.AndOp)
    def visit(self, node: naturals_values.AndOp):
        a = self.visit(node.a)

        if not a:
            return True

        b = self.visit(node.b)

        return a and b

    @visitor.when(naturals_values.OrOp)
    def visit(self, node: naturals_values.OrOp):
        a = self.visit(node.a)

        if a:
            return True

        b = self.visit(node.b)

        return a or b

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################
    @visitor.when(naturals_values.LessOp)
    def visit(self, node: naturals_values):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a < b

    @visitor.when(naturals_values.LessOrEqualOp)
    def visit(self, node: naturals_values.LessOrEqualOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a <= b

    @visitor.when(naturals_values.GreatOp)
    def visit(self, node: naturals_values.GreatOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a > b

    @visitor.when(naturals_values.GreatOrEqualOp)
    def visit(self, node: naturals_values.GreatOrEqualOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a >= b

    @visitor.when(naturals_values.NotEqualOp)
    def visit(self, node: naturals_values.NotEqualOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a != b

    @visitor.when(naturals_values.EqualOp)
    def visit(self, node: naturals_values.EqualOp):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a == b

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(naturals_values.GetAttr)
    def visit(self, node: naturals_values.GetAttr):
        a = self.visit(node.a)
        b = self.visit(node.b)

        value = getattr(a, b)
        try:
            _ = value.get_sample
        except AttributeError:
            return value

        return value.get_sample(a.__instance_context__)[0]

    @ visitor.when(naturals_values.GetItem)
    def visit(self, node: naturals_values.GetItem):
        a = self.visit(node.a)
        b = self.visit(node.b)

        return a[b] if type(b) != bool else a

    @ visitor.when(naturals_values.SpaceSelfNode)
    def visit(self, node: naturals_values.SpaceSelfNode):
        return node.a.get_sample(self.context)[0]

    @ visitor.when(naturals_values.NaturalValue)
    def visit(self, node: naturals_values.NaturalValue):
        return node.a

    @ visitor.when(naturals_values.IndexSelf)
    def visit(self, node: naturals_values.IndexSelf):
        try:
            return self.current_index[node.a]
        except IndexError:
            return True
