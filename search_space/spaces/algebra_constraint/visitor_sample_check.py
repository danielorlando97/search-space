from search_space.utils import visitor
from search_space.spaces.algebra_constraint import ast
from search_space.errors import InvalidSampler
from . import VisitorLayer
from search_space.utils.singleton import Singleton


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

    @visitor.on("node")
    def transform_to_check_sample(self, node, sample, context=None):
        pass

    @visitor.when(ast.AstRoot)
    def transform_to_check_sample(self, node, sample, context=None):
        for n in node.asts:
            self.transform_to_check_sample(n, sample)

    #################################################################
    #                                                               #
    #                  Binary Cmp Visit                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.LessOp)
    def transform_to_check_sample(self, node, sample, context=None):

        a = self.transform_to_check_sample(node.target, sample)
        b = self.transform_to_check_sample(node.other, sample)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    #################################################################
    #                                                               #
    #                  Simple Transform                             #
    #                                                               #
    #################################################################

    @visitor.when(ast.GetItem)
    def transform_to_check_sample(self, node: ast.GetItem, sample, context=None):

        a = self.transform_to_check_sample(node.target, sample)
        b = self.transform_to_check_sample(node.other, sample)

        if a < b:
            return self

        raise InvalidSampler(
            f"inconsistent sampler => [ {a} < {b} ]")

    @visitor.when(ast.SelfNode)
    def transform_to_check_sample(self, node, sample, context=None):
        return sample

    @visitor.when(ast.NaturalValue)
    def transform_to_check_sample(self, node, sample, context=None):
        try:
            return node.target.get_sample(context=context)[0]
        except AttributeError:
            return node.target
        except TypeError:
            pass
