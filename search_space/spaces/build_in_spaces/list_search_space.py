from search_space.spaces import SearchSpace, SearchSpaceDomain
import inspect
from search_space.utils import visitor
from search_space.spaces import ast_constraint as ast
from search_space.context_manager import SamplerContext, ConstraintInfo
from search_space.errors import UnSupportOpError, InvalidSampler
from .numeral_search_space import NaturalSearchSpace


class ListDomain(SearchSpaceDomain):
    pass


class ListSearchSpace(SearchSpace):
    def __init__(self, type_space: SearchSpace, len_space: NaturalSearchSpace = NaturalSearchSpace(), log_name=None) -> None:
        super().__init__(None, None, log_name)
        self.len_space = len_space
        self.typ_space = type_space

    def _create_domain(self, domain) -> SearchSpaceDomain:
        index, actual_list = domain
        return ListDomain(index, self.typ_space)
