from typing import Optional
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class BasicClassExamples(TestCase):

    #################################################################
    #                                                               #
    #                     Main Test                                 #
    #                                                               #
    #################################################################

    def test_example_line(self):
        """
        We want to find the line that best interpolates our data.
        And for some reason, we know that the slope is an integer
        between 50 and 100, but it is not 65. We also know that
        the intercept of the line is less than 50
        """

        class Line:
            def __init__(
                self,
                m: int = Domain[int](min=50, max=100) | (lambda x: x != 65),
                n: float = Domain[float]() | (lambda x: x < 50)
            ) -> None:
                self.m, self.n = m, n

        space = Domain[Line]()

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.m >= 50
            assert v.m <= 100
            assert v.m != 65
            assert v.n < 50

    def test_example_center_point(self):
        """
        We want to find the pointer more centered and with more density
        around it. For some reason, we know that our data looks like
        a heavy diagonal 20u thick. So, for every points on the line x = y
        our points are between (x-10, y) and (x+10, y)
        """

        class CenterPoint:
            Y_Domain = Domain[int]()

            def __init__(
                self,
                x: float = Domain[float]() | (
                    lambda x, y=Y_Domain: (x < y - 10) | (x > y + 10)
                ),
                y: int = Y_Domain
            ) -> None:
                self.x, self.y = x, y

        space = Domain[CenterPoint]()

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert abs(v.x - v.y) >= 10

    def test_example_param_opt_sklearn(self):
        """
        By Sklearn (Details about LogisticRegression):

        intercept_scaling float, default=1
            Useful only when the solver 'liblinear' is used and
            self.fit_intercept is set to True. In this case, x
            becomes [x, self.intercept_scaling], i.e. a “synthetic”
            feature with constant value equal to intercept_scaling
            is appended to the instance vector. The intercept
            becomes intercept_scaling * synthetic_feature_weight.

        random_state int, RandomState instance, default=None
            Used when solver == 'sag', 'saga' or 'liblinear' to shuffle the data.

        solver {'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'}, default='lbfgs'
            Algorithm to use in the optimization problem. Default is 'lbfgs'.
        """

        class LogisticRegression:
            Solver_Domain = Domain[str](
                options=['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'])

            def __init__(
                self,
                solver: str = Solver_Domain,
                intercept_scaling: float = Domain[float] | (
                    lambda x, s=Solver_Domain: (s != 'liblinear') & (x == 1)
                ),
                random_state: int = Domain[Optional[int]] | (
                    lambda x, s=Solver_Domain: (s != [
                        'liblinear', 'sag', 'saga']) & (x == None)
                )
            ) -> None:
                self.s, self.i, self.r = solver, intercept_scaling, random_state

        space = Domain[LogisticRegression]()

        @ replay_function
        def ______():
            v, _ = space.get_sample()

            if v.s != 'liblinear':
                assert v.i == 1

            if not v.s in ['liblinear', 'sag', 'saga']:
                assert v.r == None

    def test_work_deadlines_opt(self):
        """
        We want to optimize a company's deadline selection.
        This org wants to plan two deadlines, one to start
        developing new features and the other to review the
        functional requirements. The deadlines cannot
        intercept each other, so the times have to be relative
        primes.
        """

        def list_div(x: int):
            result = [1, x]
            for i in range(2, x/2):
                if x % i == 0:
                    result.append(i)

            return result

        DivList = FunctionalConstraint(list_div)

        class WorkPlanning:
            Review_Work_Domain = Domain[int](max=5)

            def __init__(
                self,
                init_time: int = Domain[int] | (
                    lambda x, y=Review_Work_Domain: (
                        x != DivList(y), x < y
                    )
                ),
                review_time: int = Review_Work_Domain,
            ) -> None:
                self.init, self.review = init_time, review_time

        space = Domain[WorkPlanning]()

        @ replay_function
        def ______():
            v, _ = space.get_sample()

            for i in range(2, v.review):
                assert not (
                    v.review % i == 0
                    and v.init % i == 0
                )
