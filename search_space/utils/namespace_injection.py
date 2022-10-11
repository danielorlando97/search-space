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
        return _type._class


New = NewClass()


class TypeClass:
    def __getitem__(self, _type: Type[T]) -> Type[T]:
        return _type._class


Type = TypeClass()


class InjectorMetaclass(type):
    _class = None

    def __new__(cls, *args, **kwg):
        def __init__(self, *args, **kwg):
            InjectorMetaclass.__init__(self, *args, **kwg)
            if type(self)._class != None:
                if not issubclass(self, type(self)._class):
                    raise ImportError(
                        'Two def for one of the item in namespace')
            else:
                type(self)._class = self

        cls.__init__ = __init__
        return super().__new__(cls, *args, **kwg)
