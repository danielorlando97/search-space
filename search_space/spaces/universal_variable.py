# TODO: Change to AST Constraints

class UniversalVariable:
    def __init__(self, *other, father=None) -> None:
        self.father = father
        self.other = other

    def __ge__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return GreatEqual(other, father=self)

    # def __or__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._great_equal(other)
    #         except AttributeError:
    #             return ss >= other
    #     return UniversalVariable(father=self, func=func)

    # def __eq__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._equal(other)
    #         except AttributeError:
    #             return ss == other
    #     return UniversalVariable(father=self, func=func)

    # def __gt__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._great(other)
    #         except AttributeError:
    #             return ss > other
    #     return UniversalVariable(father=self, func=func)

    # def __le__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._less_equal(other)
    #         except AttributeError:
    #             return ss <= other
    #     return UniversalVariable(father=self, func=func)

    # def __lt__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._less(other)
    #         except AttributeError:
    #             return ss < other
    #     return UniversalVariable(father=self, func=func)

    # def __ne__(self, other):
    #     def func(ss):
    #         try:
    #             return ss._not_equal(other)
    #         except AttributeError:
    #             return ss != other
    #     return UniversalVariable(father=self, func=func)

    # def __getattr__(self, name):
    #     if name == 'i':
    #         return UniversalVariable(father=self)

    #     def func(ss):
    #         try:
    #             return ss.__class__.__dict__[name]
    #         except KeyError:
    #             return ss.__dict__[name]

    #     return UniversalVariable(father=self, func=func)

    # def __rrshift__(self, other):
    #     return UniversalVariable(father=self, func=lambda ss: other >> ss)

    # def __getitem__(self, index):
    #     def func(ss):
    #         try:
    #             return ss._getitem(index)
    #         except AttributeError:
    #             return ss[index]

    #     return UniversalVariable(father=self, func=func)

    # def __call__(self, ss) -> None:
    #     if self.func is None:
    #         return ss

    #     return self.func(self.father(ss))
