class BachedDomain:
    def __init__(self, *domains) -> None:
        self.domains = domains

    def __copy__(self):
        return BachedDomain(*self.domains)
