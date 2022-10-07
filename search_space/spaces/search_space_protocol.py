from typing import Protocol


from search_space.context_manager import SamplerContext


class SearchSpaceProtocol(Protocol):
    def get_sample(self, context: SamplerContext = None, local_domain=None):
        """
        """
