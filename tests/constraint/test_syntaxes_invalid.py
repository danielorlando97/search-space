from unittest import TestCase
from search_space.errors import UnSupportOpError
from search_space.spaces.search_space import BasicSearchSpace
from search_space.spaces.asts import constraints
from test_syntaxes_valid import cmp_ast


class ConstraintInvalidBasicSyntaxes(TestCase):
    def setUp(self) -> None:
        self.space = BasicSearchSpace((), None)

    def test_basic_rmod(self):
        ast = self.space.__build_constraint__(lambda x: 10 % x)

        sample_ast = constraints.SegmentationModOp(
            constraints.NaturalValue(10),
            constraints.SelfNode
        )

        cmp_ast(sample_ast, ast)

    def test_invalid_or(self):
        try:
            ast = self.space.__build_constraint__(lambda x: False | x < 3)
            assert False, 'lambda x: False | x < 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: x > 5 | x < 3)
            assert False, 'lambda x: x > 5 | x < 3'
        except UnSupportOpError:
            pass

    def test_invalid_and(self):
        try:
            ast = self.space.__build_constraint__(lambda x: True & x < 3)
            assert False, 'lambda x: True & x < 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: x > 5 & x < 3)
            assert False, 'lambda x: x > 5 & x < 3'
        except UnSupportOpError:
            pass

    def test_invalid_eq(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x == x) < 3)
            assert False, 'lambda x: (x == x) < 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x == x) + 3)
            assert False, 'lambda x: x == x + 3'
        except UnSupportOpError:
            pass

    def test_invalid_neq(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x != x) > 3)
            assert False, 'lambda x: (x != x) > 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x != x) - 3)
            assert False, 'lambda x: x != x - 3'
        except UnSupportOpError:
            pass

    def test_invalid_less(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x < x) == 3)
            assert False, 'lambda x: (x < x) == 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x < x) * 3)
            assert False, 'lambda x: x < x * 3'
        except UnSupportOpError:
            pass

    def test_invalid_great(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x > x) <= 3)
            assert False, 'lambda x: (x > x) <= 3'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x > x) % 3)
            assert False, 'lambda x: x > x % 3'
        except UnSupportOpError:
            pass

    def test_invalid_sum(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x + 3)[3])
            assert False, 'lambda x: (x + 3)[3]'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x + 3).member)
            assert False, 'lambda x: (x + 3).member'
        except UnSupportOpError:
            pass

    def test_invalid_mod(self):
        try:
            ast = self.space.__build_constraint__(lambda x: (x % 3 == 1) + 5)
            assert False, 'lambda x: (x % 3 == 1) + 5'
        except UnSupportOpError:
            pass

        try:
            ast = self.space.__build_constraint__(lambda x: (x % 3 == 1) < 5)
            assert False, 'lambda x: x % 3 == 1 < 5'
        except UnSupportOpError:
            pass
