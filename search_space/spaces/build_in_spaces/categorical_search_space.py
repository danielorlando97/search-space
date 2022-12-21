from xml import dom
from search_space.sampler.factory import SamplerFactory
from search_space.spaces import SearchSpace, BasicSearchSpace
from search_space.sampler.distribution_names import UNIFORM
from search_space.spaces.visitors import visitors
from search_space.spaces.build_in_spaces.space_manager import SpacesManager
from search_space.spaces.domains.categorical_domain import CategoricalDomain

__all__ = [
    "BasicCategoricalSearchSpace",
    "BasicBooleanSearchSpace",
]


@SpacesManager.registry(str)
class BasicCategoricalSearchSpace(BasicSearchSpace):
    def __init__(self, *domain, distribute_like=UNIFORM) -> None:
        super().__init__(CategoricalDomain(domain), distribute_like=distribute_like)

    # def __advance_space__(self, ast):

    #     advance_space = CategoricalSearchSpace(
    #         self.initial_domain, distribute_like=self.__distribute_like__)

    #     advance_space.ast_constraint = ast
    #     return advance_space


# class CategoricalSearchSpace(SearchSpace):
#     def __init__(self, domain, distribute_like=UNIFORM) -> None:
#         super().__init__(domain, distribute_like=distribute_like)
#         self.visitor_layers.append(visitors.DomainModifierVisitor())

#     def __sampler__(self, domain, context):
#         return domain.get_sample(self._distribution), context

#     def __domain_filter__(self, domain, context):
#         c_domain = CategoricalDomain(domain)
#         return super().__domain_filter__(c_domain, context)

#     def __copy__(self):
#         clone = CategoricalSearchSpace(*self.initial_domain)
#         clone.set_sampler(SamplerFactory().create_sampler(
#             self._distribution.__distribute_name__, search_space=clone))
#         return clone


@SpacesManager.registry(bool)
class BasicBooleanSearchSpace(BasicSearchSpace):
    def __init__(self, *domain, distribute_like=UNIFORM) -> None:
        if len(domain) == 0:
            domain = [True, False]

        super().__init__(CategoricalDomain(domain), distribute_like=distribute_like)

    # def __advance_space__(self, ast):
    #     advance_space = BooleanSearchSpace(
    #         self.initial_domain, distribute_like=self.__distribute_like__)

    #     advance_space.ast_constraint = ast
    #     return advance_space


# class BooleanSearchSpace(CategoricalSearchSpace):
#     def __init__(self, domain, distribute_like=UNIFORM) -> None:
#         super().__init__(domain, distribute_like=distribute_like)

#     def __copy__(self):
#         clone = BooleanSearchSpace()
#         clone.set_sampler(SamplerFactory().create_sampler(
#             self._distribution.__distribute_name__, search_space=clone))
#         return clone
