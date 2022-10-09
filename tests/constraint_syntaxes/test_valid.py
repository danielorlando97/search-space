from unittest import TestCase
from search_space.spaces.search_space import BasicSearchSpace
from search_space.spaces.asts import constraints


def cmp_ast(sample_ast, result_ast):
    if not isinstance(sample_ast, constraints.UniversalVariableNode):
        if isinstance(sample_ast, BasicSearchSpace):
            assert hash(sample_ast) == hash(result_ast)

        assert sample_ast == result_ast

    elif isinstance(sample_ast, constraints.SegmentationExprNode):

        assert type(sample_ast) == type(result_ast)
        cmp_ast(sample_ast.target, result_ast.target)
        cmp_ast(sample_ast.other, result_ast.other)
        cmp_ast(sample_ast.value, result_ast.value)

    elif isinstance(sample_ast, constraints.UniversalVariableBinaryOperation):
        assert type(sample_ast) == type(result_ast)
        cmp_ast(sample_ast.target, result_ast.target)
        cmp_ast(sample_ast.other, result_ast.other)

    else:
        assert False, type(sample_ast)


class ConstraintValidBasicSyntaxes(TestCase):
    def setUp(self) -> None:
        self.space = BasicSearchSpace((), None)

    #################################################################
    #                                                               #
    #                 Logic Ops                                     #
    #                                                               #
    #################################################################

    def test_basic_or(self):
        ast = self.space.__build_constraint__(lambda x: x | True)

        sample_ast = constraints.OrOp(
            constraints.SelfNode,
            constraints.NaturalValue(True)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_ror(self):
        ast = self.space.__build_constraint__(lambda x: True | x)

        sample_ast = constraints.OrOp(
            constraints.NaturalValue(True),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    def test_basic_and(self):
        ast = self.space.__build_constraint__(lambda x: x & True)

        sample_ast = constraints.AndOp(
            constraints.SelfNode,
            constraints.NaturalValue(True)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_rand(self):
        ast = self.space.__build_constraint__(lambda x: True & x)

        sample_ast = constraints.AndOp(
            constraints.NaturalValue(True),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    #################################################################
    #                                                               #
    #                 Cmp Ops                                       #
    #                                                               #
    #################################################################

    def test_basic_eq(self):
        ast = self.space.__build_constraint__(lambda x: x == 'a')

        sample_ast = constraints.EqualOp(
            constraints.SelfNode,
            constraints.NaturalValue('a')
        )

        cmp_ast(sample_ast, ast)

    def test_basic_req(self):
        ast = self.space.__build_constraint__(lambda x: 'a' == x)

        sample_ast = constraints.EqualOp(
            constraints.SelfNode,
            constraints.NaturalValue('a')
        )

        cmp_ast(sample_ast, ast)

    def test_basic_neq(self):
        ast = self.space.__build_constraint__(lambda x: x != [1, 2])

        sample_ast = constraints.NotEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue([1, 2])
        )

        cmp_ast(sample_ast, ast)

    def test_basic_rneq(self):
        ast = self.space.__build_constraint__(lambda x: [1, 2] != x)

        sample_ast = constraints.NotEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue([1, 2])
        )

        cmp_ast(sample_ast, ast)

    def test_basic_less(self):
        ast = self.space.__build_constraint__(lambda x: x < 10)

        sample_ast = constraints.LessOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_rless(self):
        ast = self.space.__build_constraint__(lambda x: 10 < x)

        sample_ast = constraints.GreatOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_great(self):
        ast = self.space.__build_constraint__(lambda x: x > 10)

        sample_ast = constraints.GreatOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_rgreat(self):
        ast = self.space.__build_constraint__(lambda x: 10 > x)

        sample_ast = constraints.LessOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_eless(self):
        ast = self.space.__build_constraint__(lambda x: x <= 10)

        sample_ast = constraints.LessOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_reless(self):
        ast = self.space.__build_constraint__(lambda x: 10 <= x)

        sample_ast = constraints.GreatOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_egreat(self):
        ast = self.space.__build_constraint__(lambda x: x >= 10)

        sample_ast = constraints.GreatOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_regrate(self):
        ast = self.space.__build_constraint__(lambda x: 10 >= x)

        sample_ast = constraints.LessOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    #################################################################
    #                                                               #
    #               Arithmetic Ops                                  #
    #                                                               #
    #################################################################

    def test_basic_add(self):
        ast = self.space.__build_constraint__(lambda x: x + 10)

        sample_ast = constraints.AddOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_radd(self):
        ast = self.space.__build_constraint__(lambda x: 10 + x)

        sample_ast = constraints.AddOp(
            constraints.NaturalValue(10),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    def test_basic_sub(self):
        ast = self.space.__build_constraint__(lambda x: x - 10)

        sample_ast = constraints.SubOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_rsub(self):
        ast = self.space.__build_constraint__(lambda x: 10 - x)

        sample_ast = constraints.SubOp(
            constraints.NaturalValue(10),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mul(self):
        ast = self.space.__build_constraint__(lambda x: x * 10)

        sample_ast = constraints.MultiOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_rmul(self):
        ast = self.space.__build_constraint__(lambda x: 10 * x)

        sample_ast = constraints.MultiOp(
            constraints.NaturalValue(10),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    def test_basic_div(self):
        ast = self.space.__build_constraint__(lambda x: x / 10)

        sample_ast = constraints.DivOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    def test_basic_rdiv(self):
        ast = self.space.__build_constraint__(lambda x: 10 / x)

        sample_ast = constraints.DivOp(
            constraints.NaturalValue(10),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    #################################################################
    #                                                               #
    #               Segmentation Ops                                #
    #                                                               #
    #################################################################

    def test_basic_mod(self):
        ast = self.space.__build_constraint__(lambda x: x % 10)

        sample_ast = constraints.SegmentationModOp(
            constraints.SelfNode,
            constraints.NaturalValue(10)
        )
        cmp_ast(sample_ast, ast)

    #################################################################
    #                                                               #
    #               Arithmetic Segmentation Ops                     #
    #                                                               #
    #################################################################

    def test_basic_mod_mod(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 % 10)

        sample_ast = constraints.SegmentationModOp(
            constraints.SegmentationModOp(
                constraints.SelfNode,
                constraints.NaturalValue(10)
            ),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_add(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 + 10)

        sample_ast = constraints.SegmentationAddOp(
            constraints.SegmentationModOp(
                constraints.SelfNode,
                constraints.NaturalValue(10)
            ),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_rest(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 - 10)

        sample_ast = constraints.SegmentationSubOp(
            constraints.SegmentationModOp(
                constraints.SelfNode,
                constraints.NaturalValue(10)
            ),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_mult(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 * 10)

        sample_ast = constraints.SegmentationMultiOp(
            constraints.SegmentationModOp(
                constraints.SelfNode,
                constraints.NaturalValue(10)
            ),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_div(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 / 10)

        sample_ast = constraints.SegmentationDivOp(
            constraints.SegmentationModOp(
                constraints.SelfNode,
                constraints.NaturalValue(10)
            ),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    #################################################################
    #                                                               #
    #               Cmp Segmentation Ops                            #
    #                                                               #
    #################################################################

    def test_basic_mod_eq(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 == 10)

        sample_ast = constraints.SegmentationEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_neq(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 != 10)

        sample_ast = constraints.SegmentationNotEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_less(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 < 10)

        sample_ast = constraints.SegmentationLessOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_eless(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 <= 10)

        sample_ast = constraints.SegmentationLessOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_great(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 > 10)

        sample_ast = constraints.SegmentationGreatOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)

    def test_basic_mod_egreat(self):
        ast = self.space.__build_constraint__(lambda x: x % 10 >= 10)

        sample_ast = constraints.SegmentationGreatOrEqualOp(
            constraints.SelfNode,
            constraints.NaturalValue(10),
            constraints.NaturalValue(10)
        )

        cmp_ast(sample_ast, ast)
