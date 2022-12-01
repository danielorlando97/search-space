# 🔭 Python Search Space

[![wakatime](https://wakatime.com/badge/github/danielorlando97/search-space.svg)](https://wakatime.com/badge/github/danielorlando97/search-space)
[![unit and statistic testing](https://github.com/danielorlando97/search-space/actions/workflows/test.yml/badge.svg)](https://github.com/danielorlando97/search-space/actions/workflows/test.yml)

## 🤔 What's it?

A Python library that defines a DSL to describe search spaces. The DSL defines
design patterns with which the user can decorate their Python classes to describe
their space of interest. The resulting descriptions are declarative, expressive,
context sensitive, extensible and scalable. In addition, the system has a sample
generator system that is consistent and coherent with the selected description.\
**Principal Skills**: `Python` `Metaprogramming` `DSL` `AST` `Visitor Pattern`

## 🤓 Motivation

After a study of the different systems that try to solve search problems,
parametric optimization or AutoML, it was detected that there were limitations
to describe in detail the search spaces. As well as the lack of a tool whose
main objective is the description and generation of samples of such spaces.
Except for the tools with imperative syntax, none of the tools studied can
express constraints with contextual or conditional dependencies or dynamic
dimension spaces. The list of tools studied include a:
[`@autogoal`](https://github.com/autogoal/autogoal/),
[`@optuna`](https://github.com/optuna/optuna),
[`@hyperopt`](http://hyperopt.github.io/hyperopt),
[`@auto-sklearn`](https://github.com/automl/auto-sklearn),
[`@autogluon`](https://github.com/awslabs/autogluon)

## ⭐ Quickstart

### Factory of Search Space

The `Domain` space factory is the main public interface to the Python Search Space.
This factory is generic to the type of space you want to generate. In addition,
its constructor can use the following parameters to modify the characteristics of the generated space:

- `min` and `max`: with which the limits of a number space can be defined.
- `options`: list of options to choose from, this parameter transforms any space to a categorical space.
- `distribute_like`: string that refers to the random distribution with which the samples of the resulting space will be generated.
  Its default value is uniform distribution.

```python
# binary space
B = Domain[bool]()
# space of real numbers, (-oo, +oo)
R = Domain[float]()
# space of natural numbers, [0, +oo)
N = Domain[int](min=0)
# space of negative integers plus zero, [-oo, 0]
_N = Domain[int](max=0)
# categorical space of the first 100 powers of 10
ten_powers = [pow(10, i) for i in range(100)]
P = Domain[int](options = ten_powers)
# space of colors
C = Domain[str](options = ['Red', 'Blue', 'Black', 'White'])
```

Any space generated by the Domain factory define the `get_sample`
method generates random samples according to the respective distribution.

```python
space = Domain[int](min=0, max=1)
value, sample_context = sample.get_sample()
# value is 1 or 0
```

The `get_sample` method, in addition to the generated sample,
returns the sampling context relative to that sample.
This context can be used as a parameter to the `get_sample`
function and ensures that whenever an attempt is made to
generate a sample from the same space with the same context,
the same sample will be generated.

```python
space = Domain[int](min=0, max=1)
value, sample_context = sample.get_sample()
# Let value = 1, so
value1, _ = sample.get_sample(context = sample_context)
# value1 = 1
```

### Tensorial Spaces

With the `Domain` factory we can also create tensor spaces.
To describe each of the dimensions of the tensors that belong
to the resulting space, the DSL allows to use ints or random spaces
previously defined.

```python
# space of integer lists with size 10
L10 = Domain[int][10]()
# space of all integer lists
random_len = Domain[int]()
Ln = Domain[int][random_len]()
# Space of all square matrices
Mnxn = Domain[float][random_len][random_len]()
# Space of all lists of tuple with size 2
Mnx2 = Domain[float][random_len][2]()
```

In the case of tensor spaces, the parameters of the constructor of the Domain
factory are applied to each of the internal spaces of the domain.

### Constraint Function

The DSL defines a syntax to be able to describe the details of the search
spaces we are defining. This syntax is inspired by the definition of
mathematical domains, where a set is described from the particular
characteristics of any element of the set. To describe these characteristics we use
the lambda function syntax of Python. And to use these restriction functions we must
know the following characteristics.

- The constraint functions can define as many parameters as we need,
  but the first one always refers to any element of the space we are
  describing. The rest of the variables, if they do not have a default
  value declared, will represent dimensions of the space we are describing.

  ```python
  # x is a any element of A space,
  # So A = {x in Z, x != 10}
  A = Domain[int] | (lambda x: x != 10)
  # B is the space of all strictly increasing lists with size 10
  B = Domain[int][10] | (lambda x, i: x[i] > x[i+1])
  # C is the space of all symmetric square matrices with size 10
  C = Domain[int][10][10] | (lambda x, i, j: x[i][j] == x[j][i])
  ```

- The constraint functions support all Python arithmetic and
  comparison operations but some settings are not valid.
  Check these tests for some of the [valid](https://github.com/danielorlando97/search-space/blob/main/tests/constraint/test_syntaxes_valid.py) and [invalid](https://github.com/danielorlando97/search-space/blob/main/tests/constraint/test_syntaxes_invalid.py) combinations

  ```python
  valid_space = Domain[int] | (lambda x : x / 10 < 0) # OK
  invalid_space = Domain[int] | (lambda x : 10 / x < 0) # raise UnSupportOpError
  ```

- If we want to describe more than one constraint within the same function
  we must write them all between parentheses and separated by commas.

  ```python
  # So A = {x in Z, x, in (0, 20) x != 10}
  A = Domain[int] | (lambda x: (x != 10, x > 0, x < 20)),
  ```

- The `&`(AND) and `|`(OR) operators have a cutting behavior that allows
  you to define conditional constraints. If either of these operators
  can know its result only by evaluating the most left expression then
  the expression on the right will never be evaluated. In cases where
  the operands would be constraints then the `&` operator works like
  commas and the `|` operator defines a segmented domain.

  ```python
  A = Domain[int] | (lambda x: False & (x == 0)) # A = Z (integer domain)
  A = Domain[int] | (lambda x: True & (x == 0)) # A = { 10 }
  B = Domain[int] | (lambda x: True | (x == 0)) # B = Z (integer domain)
  # C is a segmented domain, C = [(-oo, -1), (101, +oo)]
  # This means that in order to generate samples,
  # you must first choose between the following segments
  C = Domain[int] | (lambda x: (x < 0) | (x > 100))
  ```

### Custom Spaces

Among the main objectives of the DSL is to define a design pattern
for writing a search space using Python's classes. To define a custom
space we only have to assign to each of the parameters of the functions
of the classes a search space as a default value.

```python
class Line:
  """
    We want to find the line that best interpolates our data.
    And for some reason, we know that the slope is an integer
    between 50 and 100, but it is not 65. We also know that
    the intercept of the line is less than 50
  """

  def __init__(
      self,
      m: int = Domain[int](min=50, max=100) | (lambda x: x != 65),
      n: float = Domain[float]() | (lambda x: x < 50)
  ) -> None:
      self.m, self.n = m, n

  def get_point(self, x: float = Domain[float](min=0, max=10))
    return x, self.m * x + self.n

  def contains(self, x, y):
    return y == self.m * x + self.n
```

If we use these decorated classes as a generic type of the Domain
factory we can create random spaces where the samples are instances of
these classes.

```python
space = Domain[Line]()
line_instance, _ = space.get_sample()
type(line_instance) # Line

#If a class method was decorated with the DSL design pattern
#then its parameters become optional.
#If no values are specified for those parameters
#then random ones are generated.
random_point = line_instance.get_point()
specific_point = line_instance.get_point(1)

line_instance.contains(0, 0) # OK
line_instance.contains() # Error
```

### Contextual Dependencies

To describe contextual dependencies, a reference to a previously
defined search space is needed. This reference will be used as the
default value of one of the parameters of the restriction function
of the dependent space. In the same way that we describe the
characteristics of a set by means of the particular characteristics
of any element of it, we will describe the relation between two
sets by means of the particular relation of any two elements of them.

```python
class CenterPoint:
  """
  We want to find the pointer more centered and with more
  density around it. For some reason, we know that our data
  looks like a heavy diagonal 20u thick.
  All points in the dataset lie between the lines
  y = x + 10 and y = x - 10.
  """

  Y_Domain = Domain[int]() # previous definition

  def __init__(
      self,
      x: float = Domain[float]() | (
          #Let y be any element of the domain Y_Domain
          lambda x, y=Y_Domain: (x - 10 < y, y < x + 10)
      ),
      y: int = Y_Domain # use the previous definition
  ) -> None:
      self.x, self.y = x, y
```

### Examples of Use Cases

- [Simple Cases, Lines, CenterPoint and LogisticRegression](https://github.com/danielorlando97/search-space/blob/main/tests/examples/basic_class_example_test.py)
- [Graph Description, Adjacency Matrix and Object Oriented](https://github.com/danielorlando97/search-space/blob/main/tests/examples/graph_examples_test.py) (integration with typing, `Optional` and `Self` spaces)
- [Transformation of classical problems to search problems, The Bag](https://github.com/danielorlando97/search-space/blob/main/tests/examples/greedy_or_dp_example.py) (hierarchical descriptions, inheritance and reference between classes)
- [Detailed description of combinatorial spaces, Color Map](https://github.com/danielorlando97/search-space/blob/main/tests/examples/ia_examples_test.py) (Imperative constrains)
- [AutoML, model selection and parametric description, Semi-supervised Model](https://github.com/danielorlando97/search-space/blob/main/tests/examples/auto_ml_example_test.py)

<!-- 
#### Valid Syntaxes

```python
Domain[int] | (lambda x: x | True)
Domain[int] | (lambda x: True | x)
Domain[int] | (lambda x: x & True)
Domain[int] | (lambda x: True & x)
Domain[str] | (lambda x: x == 'a') # (lambda x: 'a' == x)
Domain[int] | (lambda x: x != [1, 2]) # (lambda x: [1, 2] != x)
Domain[int] | (lambda x: x < 10) # (lambda x: 10 < x)
Domain[int] | (lambda x: x > 10) # (lambda x: 10 > x)
Domain[int] | (lambda x: x <= 10) # (lambda x: 10 <= x)
Domain[int] | (lambda x: x >= 10) # (lambda x: 10 >= x)
Domain[int] | (lambda x: x + 10) # (lambda x: 10 + x)
Domain[int] | (lambda x: x - 10) # (lambda x: 10 - x)
Domain[int] | (lambda x: x * 10) # (lambda x: 10 * x)
Domain[int] | (lambda x: x / 10) # (lambda x: 10 / x)
Domain[int] | (lambda x: x % 10)
Domain[int] | (lambda x: x % 10 % 10)
Domain[int] | (lambda x: x % 10 + 10)
Domain[int] | (lambda x: x % 10 - 10)
Domain[int] | (lambda x: x % 10 * 10)
Domain[int] | (lambda x: x % 10 / 10)
Domain[int] | (lambda x: x % 10 == 10)
Domain[int] | (lambda x: x % 10 != 10)
Domain[int] | (lambda x: x % 10 < 10)
Domain[int] | (lambda x: x % 10 <= 10)
Domain[int] | (lambda x: x % 10 > 10)
Domain[int] | (lambda x: x % 10 >= 10)
```

#### Invalid Syntaxes

```python
Domain[int] | (lambda x: 10 % x)
Domain[int] | (lambda x: False | x < 3)
Domain[int] | (lambda x: x > 5 | x < 3)
Domain[int] | (lambda x: True & x < 3)
Domain[int] | (lambda x: x > 5 & x < 3)
Domain[int] | (lambda x: (x == x) < 3)
Domain[int] | (lambda x: (x == x) + 3)
Domain[int] | (lambda x: (x != x) > 3)
Domain[int] | (lambda x: (x != x) - 3)
Domain[int] | (lambda x: (x < x) == 3)
Domain[int] | (lambda x: (x < x) * 3)
Domain[int] | (lambda x: (x > x) <= 3)
Domain[int] | (lambda x: (x > x) % 3)
Domain[int] | (lambda x: (x + 3)[3])
Domain[int] | (lambda x: (x + 3).member)
Domain[int] | (lambda x: (x % 3 == 1) + 5)
Domain[int] | (lambda x: (x % 3 == 1) < 5)
Domain[int][6][6][6]() | (lambda x, i, j: x[i][j] == x[j][i])

```
-->
<!--
#### Imperative Restrictions

## ⚙️ Installation

## 📚 Documentation
-->
