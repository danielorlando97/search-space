from search_space.errors import UnSupportOpError


class UniversalVariable:
    def __init__(self, father=None) -> None:
        self.father = father

    def __mod__(self, value):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return ModuleSegmentation(self, other)

    def __or__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return OrSegmentation(self, other)

    def __eq__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)

        return Equal(other, father=self)

    def __ne__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return NotEqualSegmentation(other, father=self)

    def __ge__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return GreatEqual(other, father=self)

    def __gt__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return Great(other, father=self)

    def __rgt__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return Less(other, father=self)

    def __le__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return LessEqual(other, father=self)

    def __lt__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return Less(other, father=self)

    def __rlt__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)
        return Great(other, father=self)

    #################################################################
    #                                                               #
    #           Binary Segmentation Constraint                       #
    #                                                               #
    #################################################################


class OrSegmentation(UniversalVariable):
    def __init__(self, left,  right) -> None:
        super().__init__(None)
        self.right = right
        self.left = left


class NotEqualSegmentation(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class ModuleSegmentation(UniversalVariable):
    def __init__(self, left,  right) -> None:
        super().__init__(None)
        self.right = right
        self.left = left

    def __mod__(self, value):
        raise UnSupportOpError(self, value, '%')

    def __or__(self, other):
        raise UnSupportOpError(self, other, '|')

    def __eq__(self, other):
        if not isinstance(other, UniversalVariable):
            other = NaturalValue(other)

        return EqualModuleSegmentation(self.left, self.right, other)

    # def __ne__(self, other):
    #     if not isinstance(other, UniversalVariable):
    #         other = NaturalValue(other)
    #     return NotEqualSegmentation(other, father=self)

    # def __ge__(self, other):
    #     if not isinstance(other, UniversalVariable):
    #         other = NaturalValue(other)
    #     return GreatEqual(other, father=self)

    # def __gt__(self, other):
    #     if not isinstance(other, UniversalVariable):
    #         other = NaturalValue(other)
    #     return Great(other, father=self)

    # def __le__(self, other):
    #     if not isinstance(other, UniversalVariable):
    #         other = NaturalValue(other)
    #     return LessEqual(other, father=self)

    # def __lt__(self, other):
    #     if not isinstance(other, UniversalVariable):
    #         other = NaturalValue(other)
    #     return LessEqual(other, father=self)


class EqualModuleSegmentation(UniversalVariable):
    def __init__(self, left,  right, cmp) -> None:
        super().__init__(None)
        self.right = right
        self.left = left
        self.cmp = cmp


# class NotEqualModuleSegmentation(UniversalVariable):
#     def __init__(self, other, father=None) -> None:
#         super().__init__(father)
#         self.other = other


# class GreatEqualModuleSegmentation(UniversalVariable):
#     def __init__(self, other, father=None) -> None:
#         super().__init__(father)
#         self.other = other


# class GreatModuleSegmentation(UniversalVariable):
#     def __init__(self, other, father=None) -> None:
#         super().__init__(father)
#         self.other = other


# class LessEqualModuleSegmentation(UniversalVariable):
#     def __init__(self, other, father=None) -> None:
#         super().__init__(father)
#         self.other = other


# class LessModuleSegmentation(UniversalVariable):
#     def __init__(self, other, father=None) -> None:
#         super().__init__(father)
#         self.other = other

    #################################################################
    #                                                               #
    #           Binary Restriction Constraint                       #
    #                                                               #
    #################################################################


class Equal(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class GreatEqual(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class Great(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class LessEqual(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class Less(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other

    #################################################################
    #                                                               #
    #                  Simple Constraint                            #
    #                                                               #
    #################################################################


class NaturalValue(UniversalVariable):
    def __init__(self, other, father=None) -> None:
        super().__init__(father)
        self.other = other


class SelfValue(UniversalVariable):
    pass


UniversalVariableInstance = SelfValue()