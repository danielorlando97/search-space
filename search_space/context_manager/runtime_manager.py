from typing import Protocol, Union
from search_space.utils.singleton import Singleton
from search_space.utils import infinity
from search_space.sampler import SamplerFactory


class SearchSpacePrinter:

    def __init__(self) -> None:
        self.tabs = 0

    def init_search(self, id_space, name_space):
        pass

    def sample_value(self, value, caching_value=False):
        pass

    def domain_init(self, domain):
        pass

    def ast_transformation(self, domain, ast, visitor_name=''):
        pass

    def sample_error(self, sample, error, sample_num, domain):
        pass

    def context_name(self, context):
        pass


class SearchSpaceConfig(metaclass=Singleton):
    def __init__(
        self,
        verbose: bool = False,
        replay_nums: Union[int, None] = None,
        ast_optimizations:  bool = True,
        printer: SearchSpacePrinter = None,
        minimal_numeral_limit=None,
        maximal_numeral_limit=None,
        sampler_manager: SamplerFactory = SamplerFactory
    ) -> None:
        self.verbose = verbose
        self.replay_nums = replay_nums
        self.ast_optimizations = ast_optimizations
        self.printer = printer
        self.attempts = []
        self.sampler_manager = sampler_manager()

        if minimal_numeral_limit:
            infinity.INFINITY_MIN_VALUE = minimal_numeral_limit

        if maximal_numeral_limit:
            infinity.INFINITY_MAX_VALUE = maximal_numeral_limit

    @property
    def printer_class(self) -> SearchSpacePrinter:
        return SearchSpacePrinter() if not self.verbose else self.printer
