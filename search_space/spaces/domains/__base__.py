from . import __namespace__ as nsp


class Domain(nsp.DomainProtocol):
    def is_invalid(self):
        return False

    def __rlt__(self, other):
        return self.__gt__(other)

    def __rgt__(self, other):
        return self.__lt__(other)

    def __rle__(self, other):
        return self.__ge__(other)

    def __rge__(self, other):
        return self.__le__(other)

    def __or__(self, __o):
        return nsp.New[nsp.BachedDomain](self, __o)


class NumeralDomain(Domain, nsp.NumeralDomainProtocol):
    def is_invalid(self):
        return self.min > self.max

    def extend(self, top):
        if self.max < top:
            self.max = top

    def __add__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x - factor,
            inverse=lambda x: x,
            independent_value=0
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x + factor,
            inverse=lambda x: x,
            independent_value=0
        )

    def __rsub__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x,
            inverse=lambda x: factor - x,
            independent_value=0
        )

    def __mul__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x / factor,
            inverse=lambda x: x,
            independent_value=0
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x * factor,
            inverse=lambda x: x,
            independent_value=0
        )

    def __rtruediv__(self, factor):
        return nsp.New[nsp.LinealTransformed](
            original_domain=self,
            transformer=lambda x: x * factor,
            inverse=lambda x: x / factor,
            independent_value=0
        )

    def __contains__(self, value):
        return self.min <= value and value <= self.max
