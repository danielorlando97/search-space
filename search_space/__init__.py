"""
A is a Python framework for describing search spaces and generating samples from them.

The tool defines a series of design patterns with which language classes can be 
decorated by expressing in detail each of the domains relative to the class parameters 
of those classes. Using the name of any previously decorated classes, the system offers 
the necessary mechanisms to generate random instances of the described space.
"""

# The [`sampler`](ref:search_space.sampler.__init__) submodule allows us to
# define the protocols for random number generation and selection of options.
from search_space import sampler
from search_space.sampler.default_implementations import *
from search_space.sampler.distributions import *

from search_space import context_manager

from search_space.dsl import Domain, RandomValue

from search_space import errors

from search_space import functions

from search_space import spaces

from search_space import utils
