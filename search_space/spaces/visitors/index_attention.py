from unittest import result
from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.spaces.ast_index import AstIndexNode
from search_space.utils.singleton import Singleton
from .index_solution import IndexSolutionVisitor


class IndexTransform():
    def __init__(self, list_space) -> None:
        self.list_space = list_space

    def sample_index_value(self, index, context, domain):
        _len, _ = self.list_space.len_space.get_sampler(context=context)

        if index >= _len:
            return ast.NoEvaluate()

        return ast.NaturalValue(self.list_space._getitem_(index, context, domain))

    @visitor.on("node")
    def visit(self, index, node, context, domain):
        pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def visit(self, index, node: ast.GreatEqual, context, domain):
        father: ast.AstNode = self.visit(index, node.father, context, domain)
        other: ast.AstNode = self.visit(index, node.other, context, domain)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.GreatEqual(other, father)

    @visitor.when(ast.Great)
    def visit(self, index, node: ast.Great, context, domain):
        father: ast.AstNode = self.visit(index, node.father, context, domain)
        other: ast.AstNode = self.visit(index, node.other, context, domain)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.Great(other, father)

    @visitor.when(ast.LessEqual)
    def visit(self, index, node: ast.LessEqual, context, domain):
        father: ast.AstNode = self.visit(index, node.father, context, domain)
        other: ast.AstNode = self.visit(index, node.other, context, domain)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.LessEqual(other, father)

    @visitor.when(ast.Less)
    def visit(self, index, node: ast.Less, context, domain):
        father: ast.AstNode = self.visit(index, node.father, context, domain)
        other: ast.AstNode = self.visit(index, node.other, context, domain)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.Less(other, father)

    #################################################################
    #                                                               #
    #                  Simple Visit                                 #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetAttribute)
    def visit(self, index, node: ast.GetAttribute, context, domain):
        if node.father.is_self and node.name == 'len_space':
            return ast.NaturalValue(self.list_space.len_space)

        if node.father.is_self:
            return ast.NoEvaluate()

        return ast.GetAttribute(node.name, self.visit(index, node.father, context, domain))

    @visitor.when(ast.GetIndex)
    def visit(self, index, node: ast.GetIndex, context, domain):
        if node.father.is_self:
            if isinstance(node.index, AstIndexNode):
                index_solution_visitor = IndexSolutionVisitor(context=context)
                real_index = index_solution_visitor.visit(index, node.index)
                if type(real_index) == type(True):
                    return ast.SelfValue() if real_index else ast.NoEvaluate()
                elif real_index == index:
                    return ast.SelfValue()
                else:
                    return self.sample_index_value(real_index, context, domain)
            elif node.index == index:
                return ast.SelfValue()
            else:
                return self.sample_index_value(node.index, context, domain)

        return ast.GetIndex(node.index, self.visit(index, node.father))

    @ visitor.when(ast.SelfValue)
    def visit(self, index, node: ast.SelfValue, context, domain):
        return ast.NoEvaluate()

    @ visitor.when(ast.NaturalValue)
    def visit(self, index, node: ast.NaturalValue, context, domain):
        return ast.NaturalValue(node.other)
