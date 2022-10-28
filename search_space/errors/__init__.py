class UnSupportOpError(Exception):
    def __init__(self, a, b, op: object, sub="") -> None:
        if b is None:
            super().__init__(
                f"{op} isn't support by {type(a).__name__} \n {sub}")
        else:
            super().__init__(
                f"{op} isn't support between {type(a).__name__} and {type(b).__name__} \n {sub}")


class InvalidSampler(Exception):
    @property
    def text(self):
        return self.args[0]


class InvalidSpaceDefinition(Exception):
    @property
    def text(self):
        return self.args[0]


class NotEvaluateError(Exception):
    pass


class InvalidSpaceConstraint(Exception):
    @property
    def text(self):
        return self.args[0]


class SpaceBuildingError(Exception):
    pass


class CircularDependencyDetected(Exception):
    pass


class TypeWithoutDefinedSpace(Exception):
    pass


class UndefinedSampler(Exception):
    pass


class DetectedRuntimeDependency(Exception):
    pass


class ArgumentFunctionError(Exception):
    pass


class RecursionErrorSpaceDefinition(Exception):
    pass
