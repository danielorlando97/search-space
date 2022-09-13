import imp
from typing import Type
from search_space.utils.singleton import Singleton
from search_space.spaces import SearchSpace
from search_space.errors import TypeWithoutDefinedSpace


class SpacesManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__spaces = {}

    @staticmethod
    def registry(_type: Type = None):
        def f(cls):
            manager = SpacesManager()
            if _type is None:
                manager.__spaces[cls] = cls
            else:
                manager.__spaces[_type] = cls

            return cls
        return f

    def get_space_by_type(self, _type: Type) -> Type[SearchSpace]:
        try:
            return self.__spaces[_type]
        except KeyError:
            raise TypeWithoutDefinedSpace(
                f"SpaceManager don't has definition for {_type}")
