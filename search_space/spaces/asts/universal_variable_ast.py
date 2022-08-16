from search_space.spaces.universal_variable import UniversalVariable


class UniversalVariable:
    def __init__(self, *other, father=None) -> None:
        self.father = father
        self.other = other

    def __ge__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return GreatEqual(other, father=self)


UniversalVariableInstance = UniversalVariable()


class GreatEqual(UniversalVariable):
    pass


class NaturalValue(UniversalVariable):
    pass
