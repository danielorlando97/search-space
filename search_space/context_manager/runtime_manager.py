from typing import Union
from search_space.utils.singleton import Singleton


class SearchSpacePrinter:

    tabs: str

    def init_search(self, id_space, name_space):
        pass

    def sample_value(self, value, caching_value=False):
        pass

    def domain_init(self, domain):
        pass

    def ast_transformation(self, domain, ast):
        pass

    def sample_error(self, sample, error, sample_num):
        pass


class SearchSpaceConfig(metaclass=Singleton):
    def __init__(
        self,
        verbose: bool = False,
        replay_nums: Union[int, None] = None,
        ast_optimizations:  bool = True,
        printer: SearchSpacePrinter = None
    ) -> None:
        self.verbose = verbose
        self.replay_nums = replay_nums
        self.ast_optimizations = ast_optimizations
        self.printer = printer

    @property
    def printer_class(self) -> SearchSpacePrinter:
        return SearchSpacePrinter() if not self.verbose else self.printer
