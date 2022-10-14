from typing import Type, TypeVar, Generic

T = TypeVar('T')


# class Instanter(Generic[T]):
#     def __init__(self, cls) -> None:
#         super().__init__()
#         self.cls = cls

#     def __call__(self, *args, **kwg) -> T:
#         return self.cls(*args, **kwg)


class NewClass:
    def __getitem__(self, _type: Type[T]) -> Type[T]:
        return _type._class[_type]


New = NewClass()


class TypeClass:
    def __getitem__(self, _type: Type[T]) -> Type[T]:
        return _type._class[_type]


Type = TypeClass()


def default_init(cls):
    def f(self, *args, **kwg):
        super(cls,  self).__init__(*args, **kwg)
    return f


class InjectorMetaclass(type):
    _class = {}

    def __new__(cls, *args, **kwg):
        def __init__(self, *args, **kwg):
            super().__init__(*args, **kwg)
            try:
                _ = type(self)._class[type(self)]
            except KeyError:
                type(self)._class[type(self)] = self

        cls.__mro__[0].__init__ = __init__
        for i in range(1, len(cls.__mro__) - 2):
            cls.__mro__[i].__init__ = default_init(cls.__mro__[i + 1])
        return super().__new__(cls, *args, **kwg)
