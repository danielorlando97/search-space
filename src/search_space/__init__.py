# try:
#     from .abs_search_space import SearchSpace, ContextManagerSearchSpace
#     from .universal_variable import UniversalVariable
#     from .ss_constraint import SearchSpaceConstraint, Predication
# except (ModuleNotFoundError, ImportError):
#     from abs_search_space import SearchSpace, ContextManagerSearchSpace
#     from universal_variable import UniversalVariable
#     from ss_constraint import SearchSpaceConstraint, Predication

from .abs_search_space import SearchSpace, ContextManagerSearchSpace
from .universal_variable import UniversalVariableInstance as UniversalVariable
from .ss_constraint import SearchSpaceConstraint, Predication
