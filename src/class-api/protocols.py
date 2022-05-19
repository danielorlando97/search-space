from typing import Protocol

class Sampler(Protocol):
    """iterator by its probability distribution, defined domain"""

class Domain(Protocol):
    """context in defined a sampler"""

class FiniteDomain(Domain):
    """In this context the options are numerable"""

class InfiniteDomain(Domain):
    """In this context the options aren't numerable"""

class SearchSpace(Protocol):
    """Is the union between one domain and one sampling"""


"""
SearchSpace = Object's set
Sampling = get an object of set
Optimal Sampling = get the best object of set by objective function  
Valid Sampling = get an object of set that it complies with all rules of the describe
"""