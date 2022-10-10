from typing import Type, TypeVar, Generic

T = TypeVar('T')


class Instanter(Generic[T]):
    def __init__(self, cls) -> None:
        super().__init__()
        self.cls = cls

    def __call__(self, *args, **kwg) -> T:
        return self.cls(*args, **kwg)


class NewClass:
    def __getitem__(self, _type: Type[T]) -> Type[T]:
        return Instanter[_type](_type._class)


New = NewClass()


class InjectorMetaclass(type):
    _class = None

    def __new__(cls, *args, **kwg):
        def __init__(self, *args, **kwg):
            super().__init__(*args, **kwg)
            if type(self)._class != None:
                raise ImportError('Two def for one of the item in namespace')

            type(self)._class = self

        cls.__init__ = __init__
        instance = type.__new__(cls, *args, **kwg)

        return instance
