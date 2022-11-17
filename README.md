# 🔭 Python Search Space
 
[![wakatime](https://wakatime.com/badge/github/danielorlando97/search-space.svg)](https://wakatime.com/badge/github/danielorlando97/search-space)
[![unit and statistic testing](https://github.com/danielorlando97/search-space/actions/workflows/test.yml/badge.svg)](https://github.com/danielorlando97/search-space/actions/workflows/test.yml) 


## 🤔 What's it?

A Python library that defines a DSL to describe search spaces. The DSL defines 
design patterns with which the user can decorate their Python classes to describe 
their space of interest. The resulting descriptions are declarative, expressive, 
context sensitive, extensible and scalable. In addition, the system has a sample 
generator system that is consistent and coherent with the selected description.
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

#### Personalized Spaces 

```python
from typing import List
from search_space.dsl import Domain

class CustomSpace:
    def __init__(
        self,
        a: int = Domain[int](min=0, max=100),
        b: int = Domain[int] | (lambda x: (x != 10, x > 0, x < 20)),
        c: float = Domain[float](min=0) | (lambda x: x != 10),
        d: List[int] = Domain[int][10](max=20) | (lambda x, i: x[i] != 15)
        e: str = Domain[str][10](options = ["A","B","C","D","E"])
    ) -> None:
        self.a, self.b, self.c, self.d, self.e = a, b, c, d, e
        
custom_space = Domain[CustomSpace]()
value, _ = custom_space.get_sample()

assert type(value) == CustomSpace
assert value.a >= 0 and value.a <= 100 and type(value.a) == int
assert value.b >= 0 and value.b != 10 and value.b <= 100 and type(value.b) == int
assert value.c >= 0 and value.b != 10 and type(value.c) == float
assert value.e in ["A","B","C","D","E"] and type(value.e) == str

for sample in value.d:
  assert sample != 15 and sample <= 20 and type(sample) == int
```
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

<!--
#### Contextual dependencies
#### Conditional dependencies 
#### Tensor spaces  
#### Imperative Restrictions  

## ⚙️ Installation

## 📚 Documentation
-->
