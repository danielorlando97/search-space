class UnSupportOpError(Exception):
    def __init__(self, a, b, op: object) -> None:
        super().__init__(
            f"{op} isn't support between {type(a).__name__} and {type(b).__name__} ")


class InvalidSampler(Exception):
    @property
    def text(self):
        return self.args[0]
