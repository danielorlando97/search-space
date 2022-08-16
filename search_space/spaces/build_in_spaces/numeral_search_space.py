from unittest.mock import seal
from search_space.spaces import SearchSpace, SearchSpaceConstraint
from search_space.sampler.distribution_names import UNIFORM
from search_space.utils import visitor
from search_space.spaces.asts import universal_variable_ast as Val_AST
from search_space.spaces.asts import numeral_ast as N_AST


class NumeralSearchSpace(SearchSpace):
    def __init__(self, min, max, distribute_like, log_name) -> None:
        super().__init__((min, max), distribute_like, log_name)

    def _great_equal(self, other):
        self.constraint_list.append(GreatEqual(other, self))
        return self.constraint_list[-1]

    def _less_equal(self, other):
        self.constraint_list.append(LessEqual(other, self))
        return self.constraint_list[-1]

    def _great(self, other):
        self.constraint_list.append(Great(other, self))
        return self.constraint_list[-1]

    def _less(self, other):
        self.constraint_list.append(Less(other, self))
        return self.constraint_list[-1]

    def _not_equal(self, other):
        self.constraint_list.append(NotEqual(other, self))
        return self.constraint_list[-1]

    ####################################
    #                                  #
    #       Add Constraint Visitor     #
    #                                  #
    ####################################

    @visitor.on('constraint')
    def add_constraint(self, constraint):
        pass

    @visitor.when(Val_AST.GreatEqual)
    def add_constraint(self, constraint: Val_AST.GreatEqual):
        target = self.add_constraint(constraint.father)
        other = self.add_constraint(constraint.other)
        return N_AST.GreatEqualNumeralConstraint(target, other)

    ####################################
    #                                  #
    #  Transform Domain by Constraints #
    #                                  #
    ####################################

    @visitor.on('constraint')
    def transform_domain(self, constraint, domain):
        pass

    @visitor.when(N_AST.GreatEqualNumeralConstraint)
    def transform_domain(self, constraint: N_AST.GreatEqualNumeralConstraint, domain):
        a, b = self.transform_domain(constraint.target, domain)
        return (max(a, self._real_value), b)

    ####################################
    #                                  #
    #       Specific Search Spaces     #
    #                                  #
    ####################################


class ContinueSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None, distribute_like=UNIFORM) -> None:
        super().__init__(min, max, distribute_like, log_name)

    def _get_random_value(self, domain):
        return self._distribution.get_float(*domain)


class NaturalSearchSpace(NumeralSearchSpace):
    def __init__(self, min=0, max=100000, log_name=None,
                 distribute_like=UNIFORM) -> None:

        super().__init__(min, max, distribute_like, log_name)

    def _get_random_value(self, domain):
        return self._distribution.get_int(*domain)


class GreatEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def _func_transform(self, domain):
        a, b = domain
        return (max(a, self._real_value), b)


class LessEqual(SearchSpaceConstraint):
    @property
    def is_transformer(self):
        return True

    def _func_transform(self, domain):
        a, b = domain
        return (a, min(b, self._real_value))


class Great(GreatEqual):
    @property
    def is_condition(self):
        return True

    def _func_condition(self, sampler):
        return self._real_value < sampler


class Less(LessEqual):
    @property
    def is_condition(self):
        return True

    def _func_condition(self, sampler):
        return self._real_value > sampler


class NotEqual(SearchSpaceConstraint):
    @property
    def is_condition(self):
        return True

    def _func_condition(self, sampler):
        return self._real_value != sampler
