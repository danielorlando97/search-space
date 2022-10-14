from . import __namespace__ as nsp


class Domain(nsp.DomainProtocol):

    def __rlt__(self, other):
        return self.__gt__(other)

    def __rgt__(self, other):
        return self.__lt__(other)

    def __rle__(self, other):
        return self.__ge__(other)

    def __rge__(self, other):
        return self.__le__(other)


class NumeralDomain(Domain, nsp.NumeralDomainProtocol):
    pass
    # def __mod__(self, factor):

    # def __add__(self, factor):
    #     return LinearTransformedDomain(
    #         original_domain=self,
    #         transformer=lambda x: x - factor,
    #         inverse=lambda x: x + factor
    #     )

    # def __sub__(self, factor):
    #     return LinearTransformedDomain(
    #         original_domain=self,
    #         transformer=lambda x: x + factor,
    #         inverse=lambda x: x - factor
    #     )

    # def __mult__(self, factor):
    #     return LinearTransformedDomain(
    #         original_domain=self,
    #         transformer=lambda x: x/factor,
    #         inverse=lambda x: x * factor
    #     )

    # def __div__(self, factor):
    #     return LinearTransformedDomain(
    #         original_domain=self,
    #         transformer=lambda x: x * factor,
    #         inverse=lambda x: x / factor
    #     )
