from search_space.spaces import SearchSpace
from search_space.spaces.algebra_space import visitors


@visitors.ComputingSpace.inject_determinist_class
class DeterministSpace(SearchSpace):
    def __init__(self, value) -> None:
        super().__init__(value, None)

    def get_sample(self, context=None, local_domain=None):
        return self.initial_domain, context
