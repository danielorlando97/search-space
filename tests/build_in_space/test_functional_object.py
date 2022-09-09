from search_space import dsl as ss
from tests.config import validate_replay_count


# TODO: domains intro class definition

names = [
    "Sirius", "Canopus", "Arcturus",
    "Alpha Centauri A.", "Vega", "Rigel",
    "Procyon", "Achernar"
]


class SpaceFactory(ss.ClassFabricSearchSpace):
    def __space__(self, abi_class):
        self.years = ss.N(0, 100000)
        self.diameter = ss.R(0, 1000000000)
        self.name = ss.Categorical(*names)

        abi_class.registry('__init__', self.years, self.diameter, self.name)

        self.other_space_body = SpaceFactory(*self.initial_domain)
        abi_class.registry('__eq__', self.other_space_body)


class Stars:
    def __init__(self, years: int, diameter: int, name: str) -> None:
        self.years = years
        self.diameter = diameter
        self.name = name

    def __str__(self) -> str:
        return f'the start {self.name} has {self.years} years old and {self.diameter} km of diameter'

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Stars):
            return False

        return self.years == __o.years and self.diameter == __o.diameter and self.name == __o.name

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)


class StellarRock:
    def __init__(self, years: int, diameter: int, name: str) -> None:
        self.years = years
        self.diameter = diameter
        self.name = name

    def __str__(self) -> str:
        return f'the stellar rock {self.name} has {self.years} years old and {self.diameter} km of diameter'

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, StellarRock):
            return False

        return self.years == __o.years and self.diameter == __o.diameter and self.name == __o.name

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)


def test_random_values():
    n = SpaceFactory(Stars, StellarRock)

    for _ in range(validate_replay_count):
        v1, _ = n.get_sample()
        v2, _ = n.get_sample()

        assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"


def test_context_consistence():
    n = SpaceFactory(Stars, StellarRock)

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert len(values_list) == 0, """
        The same sampler generates the same value for the same context"""


def test_object_minimal():
    n = SpaceFactory(Stars, StellarRock)

    for _ in range(validate_replay_count):
        value, _ = n.get_sample()
        assert value.years % 1 == 0
        assert type(value.diameter) == type(float())
        assert value.name in names


# def test_dsl_constraint():
#     func = [
#         ("Less", lambda x: x < 50),
#         ("LessEq", lambda x: x <= 50),
#         ("Great", lambda x: x > 50),
#         ("GreatEq", lambda x: x >= 50)
#     ]

#     for op, f in func:
#         n = ss.N(0, 100) | f
#         for _ in range(validate_replay_count):
#             value, _ = n.get_sample()
#             assert f(value), f'Error with operator {op}'


# def test_dsl_context_sensitive():
#     m = ss.N(40, 60)

#     func = [
#         ("Less", lambda x: x < m, lambda x, y: x < y),
#         ("LessEq", lambda x: x <= m, lambda x, y: x <= y),
#         ("Great", lambda x: x > m, lambda x, y: x > y),
#         ("GreatEq", lambda x: x >= m, lambda x, y: x >= y)
#     ]

#     for op, f, test in func:
#         n = ss.N(0, 100) | f
#         for _ in range(validate_replay_count):
#             value, context = n.get_sample()
#             m_value, _ = m.get_sample(context=context)
#             assert test(
#                 value, m_value), f'Error with operator {op} => ({value}, {m_value})'
