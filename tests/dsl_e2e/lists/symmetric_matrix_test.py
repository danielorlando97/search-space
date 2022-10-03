from unittest import TestCase
from search_space.dsl import Domain
from tests.config import replay_function


class SymmetricMatrix(TestCase):

    #################################################################
    #                                                               #
    #                     Main Test                                 #
    #                                                               #
    #################################################################

    def test_dynamic_int_space(self):
        matrix_size = Domain[int](min=4, max=8)
        matrix_space = Domain[int][matrix_size][matrix_size] | (
            lambda x, i, j: x[i][j] == x[j][i]
        )

        def test():
            matrix, context = matrix_space.get_sample()
            size, _ = matrix_size.get_sample(context)

            assert len(matrix) == size
            for i, row in enumerate(matrix):
                assert len(row) == size
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)

    #################################################################
    #                                                               #
    #                     Other Versions                            #
    #                     - Change Types                            #
    #                     - Change Dims                             #
    #                     - Change Constraint                       #
    #                                                               #
    #                                                               #
    #                                                               #
    #                                                               #
    #                                                               #
    #################################################################

    def test_basic_int_space(self):
        matrix_space = Domain[int][6][6] | (lambda x, i, j: x[i][j] == x[j][i])

        def test():
            matrix, _ = matrix_space.get_sample()

            for i, row in enumerate(matrix):
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)

    def test_float_space(self):
        matrix_space = Domain[float][6][6] | (
            lambda x, i, j: x[i][j] == x[j][i])

        def test():
            matrix, _ = matrix_space.get_sample()

            for i, row in enumerate(matrix):
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)

    def test_str_space(self):
        matrix_space = Domain[str][6][6](
            options=[f'{i}' for i in range(100)]
        ) | (
            lambda x, i, j: x[i][j] == x[j][i])

        def test():
            matrix, _ = matrix_space.get_sample()

            for i, row in enumerate(matrix):
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)

    def test_list_space(self):
        matrix_space = Domain[int][6][6][6]() | (
            lambda x, i, j: x[i][j] == x[j][i])

        def test():
            matrix, _ = matrix_space.get_sample()

            for i, row in enumerate(matrix):
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)

    def test_obj_space(self):

        class ATestClass:
            def __init__(self, a: int = Domain[int]()) -> None:
                self.a = a

            def __eq__(self, __o: object) -> bool:
                return self.a == __o.a

        matrix_space = Domain[ATestClass][6][6]() | (
            lambda x, i, j: x[i][j] == x[j][i])

        def test():
            matrix, _ = matrix_space.get_sample()

            for i, row in enumerate(matrix):
                for j, item in enumerate(row):
                    assert item == matrix[j][i]

        replay_function(test)
