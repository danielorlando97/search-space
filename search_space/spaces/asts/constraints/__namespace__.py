from search_space.utils.namespace_injection import InjectorMetaclass, New, Type


class ExprNode(InjectorMetaclass):
    def __init__(self, target, other):
        pass


class NaturalValueNode(ExprNode):
    def __init__(self, value):
        pass
