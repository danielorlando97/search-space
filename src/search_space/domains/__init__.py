# try:
#     from .numeral_search_space import NaturalSearchSpace, ContinueSearchSpace
#     from .categorical_search_space import CategoricalSearchSpace, BooleanSearchSpace
#     from .object_search_space import ObjectSearchSpace, ListSearchSpace
# except (ModuleNotFoundError, ImportError):
#     from numeral_search_space import NaturalSearchSpace, ContinueSearchSpace
#     from categorical_search_space import CategoricalSearchSpace, BooleanSearchSpace
#     from object_search_space import ObjectSearchSpace, ListSearchSpace

from .numeral_search_space import NaturalSearchSpace, ContinueSearchSpace
from .categorical_search_space import CategoricalSearchSpace, BooleanSearchSpace
from .object_search_space import ListSearchSpace, ObjectSearchSpace
