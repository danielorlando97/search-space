from search_space.spaces import SearchSpace
from search_space import ContinueSearchSpace as R
from search_space import UniversalVariable as X
from search_space.spaces.build_in_spaces.object_search_space import MetaClassFabricSearchSpace
import os

class Line(metaclass = MetaClassFabricSearchSpace):
    """Domain Description"""
    m_domain = R()
    n_domain = R()
    x_domain = R()

    """Class Description"""
    def __init__(self, m: float = m_domain, n: float = n_domain) -> None:
        self.m, self.n = m, n

    def get_point(self, x: float = x_domain) :
        return (x, self.m * x + self.n)


def test_instance_object():
    line: SearchSpace = Line()
    line1, _ = line.get_sampler()
    line2, _ = line.get_sampler()

    assert line1 != line2
    assert line1.m != line2.m
    assert line1.n != line.n
    assert line1.get_point() != line2.get_point()

    line1, context = line.get_sampler()
    line2, _ = line.get_sampler(context)

    assert line1 == line2
    assert line1.m == line2.m
    assert line1.n == line.n
    assert line1.get_point() != line2.get_point()

def test_context_sensitise():
    space : SearchSpace  = Line() | (X.m_domain < 10, X.n_domain > 50, X.x_domain < 3)
    line, _ = space.get_sampler()

    assert line.m < 10
    assert line.n > 50

    x, y = line.get_point()
    assert x < 3
    assert y == line.m * x + line.n