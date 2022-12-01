<!-- Q' Bola πkt 😃 \
I would like to tell you about one of my favorite projects of the last years
and that I'll present as a bachelor thesis in the next week.\
It's about:\
🐍 Python\
🔁 Metaprogramming\
⌨️ Languages Theory\
🔍 Description of Search Spaces\
⚙️ Generation of random samples\

--- -->

🤔What's it?

A Python library that defines a DSL to describe search spaces.
It defines design patterns to decorate Python's classes and to describe
the spaces. The library has a sample generator system that is consistent
and coherent with the selected descriptions.

---

🤓 Motivation

After a study of the different systems that try to solve search problems,
params opt or AutoML, it was detected that there were limitations to
describe in detail the search spaces.

Some of tools studied: @auto_goal , @OptunaAutoML, @autogluon, autosklearn, ...

---

1️⃣) The domains are only described by their limits and types. The mechanisms
for expressing constraints are imperative and subsequent to sample generation.
Therefore the resulting descriptions are not very expressive and represent
spaces with many invalid elements.

```python
class Line:
    """
    Search space for lines whose slope is an integer
    between 50 and 100, but not equal to 65, and whose
    intercept with the x-axis is a decimal less than 50.
    """

    def __init__(
        self,
        # The DSL can describe domains using limits and types,
        # but it also defines a syntax to express more detail
        m: int = Domain[int](min=50, max=100) | (lambda x: x != 65),
        # Even limits may not be necessary
        n: float = Domain[float]() | (lambda x: x < 50)
    ) -> None:
        self.m, self.n = m, n

space = Domain[Line]() # Create new space of lines
line, _ = space.get_sample() # Get a random instance of Line class
# line.m and line.n comply with the described restrictions
```

---

2️⃣) The way constraints are written doesn't allow describing contextual dependencies.  
Sklearn, for example, has many models that define relationships between its hyperparameters,
where an invalid combination is equivalent to a run-time error.

```python
class LogisticRegression:
    "Space described in Sklean Documentation"

    # To describe the contextual dependencies
    # it's necessary to define a reference to
    # the independent space
    Solver_Domain = Domain[str](
        options=['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'])

    def __init__(
        self,
        solver: str = Solver_Domain,
        intercept_scaling: float = Domain[float] | (
            # To reference a previously defined space within a constraint function,
            # simply define a new parameter and
            # assign the space in question as the default value.
            lambda x, s=Solver_Domain: (s != 'liblinear') & (x == 1)
        ),
        random_state: int = Domain[Optional[int]] | (
            lambda x, s=Solver_Domain: (
                # The DSL doesn't define any flow control structure,
                # but proposes the use of the logical operators AND and OR
                # to describe conditional constraints (these operators present a
                # cut-through implementation).
                (s != ['liblinear', 'sag', 'saga']) & (x == None)
            )
        )
    ) -> None:
        self.s, self.i, self.r = solver, intercept_scaling, random_state
```

---

3️⃣) The systems studied cannot easily express random-dimensional spaces.
Consequently, they also do not present syntaxes for sequential constraints.

```python
class Set:
    NDomain = Domain[int](min=0, max=1000)

    def __init__(
        self,
        # The DSL defines a syntax similar to that of
        # statically typed languages for defining tensor types.
        # But in this case the dimension does not necessarily have to be a fixed value.
        values: List[int] = Domain[int][NDomain] | (

            # Comparison operators also support lists as second operators.
            # In addition, as long as the constraint doesn't make comparisons of type
            # x == x the system can find the topological order of the described sequence.
            lambda x, i: x[i] != x[:i]
        )
    ) -> None:
        self.values = values


class GraphByAdjMatrix:
    NDomain = Domain[int](min=0, max=1000)

    def __init__(
        self, n: int = NDomain,
        adj_matrix: List[int] = Domain[bool][NDomain][NDomain] | (
            # The DSL's design pattern in principle doesn't allow circular dependencies,
            # except for circular constraints within a structure (class or tensor).
            # In these cases, since the native comparators are symmetric,
            # the system simply ignores one of the edges.
            lambda x, i, j: x[i][j] == x[j][i]
        )
    ) -> None:
        self.n, self.matrix = n, adj_matrix
```

---

4️⃣) High-level operations, such as recursion or type algebra, have a primitive
presentation. Others, such as imperative constraints, are often used as validations
and not as domain delimitations. A better use of these tools can be an important
evolution in expressive terms.

```python
from typing import List, Optional, Union
from typing_extensions import Self

# There are many constraints that cannot be expressed
# as a combination of the operations defined by the DSL's grammar.
# Therefore, a mechanism for expressing imperative constraints is needed.
@FunctionalConstraint
def if_is_int_then_is_even(x):
    if type(x) != int:
        return True

    for i in range(2, x//2 + 1):
        if x % i == 0:
            return False
    return True


class Sum:
    def __init__(
        self,
        a: Union[Self, int] = Domain[Union[Self, int]] | (
            #Imperative constraints will be
            #considered as "black box functions" or natural values,
            #which can be added to the dynamic domain inheritance process,
            #depending on their parameters.
            lambda x: if_is_int_then_is_even(x)
        ),

        # The DSL implements an integration with the typing library
        # to describe recursive spaces, multi-type spaces and optional spaces.
        b: Union[Self, int] = Domain[Union[Self, int]] | (
            lambda x: if_is_int_then_is_even(x)
        )
    ) -> None:
        self.a, self.b = a, b


optional_summation_space = Domain[Optional[Sum]]()
```

---

The implementation of this tool is based on 4 fundamental ideas,
which I will explain based on this example:

```python
from search_space.dsl import Domain

class CustomClass:
    ValueDomain = Domain[int](min=0, max=1000)

    def __init__(
        self,
        value: int = ValueDomain,
        size: int = Domain[int](min=0, max=1000)
    ) -> None:
        self.value, self.size = value, size

random_limit = Domain[int](min=10, max=50)
tensor_of_custom_classes_space = Domain[CustomClass][10] | (
    lambda x, i, y = random_limit: (
        x[i > 3].ValueDomain != [20, 50, 30, 40],
        x[i > 3].ValueDomain < y
    )
)
```

---

1️⃣)Interpretation of constraint functions as ASTs.
For this purpose we model a class hierarchy describing all possible ASTs
of the constraint grammar. Finally we pass to the functions the Self, Index
and SeachSpace nodes of the hierarchy as parameters.

AST relative to the tensor space of type CustomClass
![](/doc/ast.png)

2️⃣) Transformation of ASTs to propagate constraints and
detect contextual dependencies. This process uses the visit
pattern to define a list of traversals and transformations
over the ASTs.

AST resulting from transmitting the tensor space constraints
to any of its internal spaces such that i>3.
For i<=3 these constraints are ignored.
![](/doc/ast_i.png)

AST resulting from transmitting the constraints of any CustomClass
space in the tensor, such that i>3, to the space of integers
describing the Value parameter of that class. Since these
constraints do not refer to the Size parameter, then they
are ignored by that parameter.
![](/doc/ast_member.png)

3️⃣) Definition of a domain algebra.
It allows compiling constraints without context dependencies
to define initial domains. In addition, it allows to infer
dynamic domains at generation time by performing a similar
analysis with context-sensitive constraints.

```python
# (-oo, oo) < 5 => (-oo, oo)
Domain[float]| (lambda x: x < 5)
# (-oo, oo) < 5 => (-oo, 4)
Domain[int]| (lambda x: x < 5)
# [1, ..., 10] < 5 => [1, ..., 4]
Domain[int](options=[i for i in range(10)])| (lambda x: x < 5)
# [1, ..., 10] != 5 = [1, ..., 4, 6, ... 10]
Domain[int](options=[i for i in range(10)])| (lambda x: x != 5)
#            (-oo, oo) != 5 => [(-oo, 4), (6, oo)]
# [(-oo, 4), (6, oo)] != 10 => [(-oo, 4), (6, 9), (11, oo)]
Domain[int]| (lambda x: x != 5, x != 10)
# (0, 15) | [20, 100,200] => [(0, 15), [20, 100,200]]
Domain[int]| (lambda x: (
    (0 <= x, x <= 15) | (x == [20, 100,200])
))
#LinealTransformationDomain => LTD(inner_domain, transformer, inverted)
#              (0, 15) + 10 => LTD((10, 25), lambda x: x, lambda x: x - 10)
# LTD((10, 25), ....) != 20 => LTD([(10, 19), (21, 25)], lambda x: x, lambda x: x - 10)
Domain[int](min = 0, max = 15) | (lambda x: x + 10 != 20)
```

Ending the interpretation period of the constraints. All the spaces
relative to the Value parameters of the CustomClass spaces with
index i > 3 within the tensor space store this AST

![](/doc/ast_dynamic_base.png)

Each of them are now defined within the segmented domain
[(0, 19), (21, 29), (31, 39), (41, 49), (50, 100)].

4️⃣) Context-consistent sample generation
Implemented with generation context where each space is mapped
to its sample, so that every time you try to generate a sample
from the same space with the same context, the same sample is
generated.

```python
# FOR EXAMPLE

#In order to generate a sample of the tensor
#it is necessary to generate a sample of random_limit.
#Assuming 35 is the internally generated sample for that space.
#Then the dynamic domain of each of the indices of the tensor space is
#SegmentationDomain[N(0, 19), N(21, 29), N(31, 34)].
tensor_instance, context = tensor_of_custom_classes_space.get_sample()
#So, tensor_instance can be equal to [1,21,33,2,25,31,7,27,22,1]
random_int, _ = random_limit.get_sample(context=context) # random_int = 35


#Similarly if we first generate a sample of random_limit and
#then pass the resulting context to the tensor space then:
random_int, context = random_limit.get_sample()
#If A equals 17 then the dynamic domain of each of
#the tensor indices would be N(0, 16)
tensor_instance, _ = tensor_of_custom_classes_space.get_sample(context=context)
#So, tensor_instance can be equal to [13,1,10,15,2,6,16,11,3,0]
```

<!-- Soon I will add the project to the python libraries collection.
If you liked the project and want to check more about it,
be aware of its release to use it or just give me a ⭐️,
here is the @github repo 😁
https://github.com/danielorlando97/search-space -->
