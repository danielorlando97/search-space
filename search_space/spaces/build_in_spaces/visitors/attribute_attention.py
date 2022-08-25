from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.utils.singleton import Singleton

class AttributeAttention(metaclass=Singleton):

    @visitor.on("node")
    def visit(self, attribute, node):
        pass

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GreatEqual)
    def visit(self, attribute, node: ast.GreatEqual):
        father: ast.AstNode = self.visit(attribute, node.father)
        other : ast.AstNode = self.visit(attribute, node.other)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.GreatEqual(other, father)

    @visitor.when(ast.Great)
    def visit(self, attribute, node: ast.Great):
        father: ast.AstNode = self.visit(attribute, node.father)
        other : ast.AstNode = self.visit(attribute, node.other)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.Great(other, father)


    @visitor.when(ast.LessEqual)
    def visit(self, attribute, node: ast.LessEqual):
        father: ast.AstNode = self.visit(attribute, node.father)
        other : ast.AstNode = self.visit(attribute, node.other)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.LessEqual(other, father)


    @visitor.when(ast.Less)
    def visit(self, attribute, node: ast.Less):
        father: ast.AstNode = self.visit(attribute, node.father)
        other : ast.AstNode = self.visit(attribute, node.other)

        if not father.can_evaluate:
            return ast.NoEvaluate()

        return ast.Less(other, father)

    #################################################################
    #                                                               #
    #                  Simple Visit                                 #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetAttribute)
    def visit(self, attribute, node: ast.GetAttribute):
        if node.father.is_self:
            if attribute == node.name:
                return ast.SelfValue()
            return ast.NoEvaluate()
        
        return ast.GetAttribute(node.name, self.visit(attribute, node.father))

    @visitor.when(ast.SelfValue)
    def visit(self, attribute, node: ast.Less):
        return ast.NoEvaluate()

    @visitor.when(ast.NaturalValue)
    def visit(self, attribute, node: ast.NaturalValue):
        return ast.NaturalValue(node.other)