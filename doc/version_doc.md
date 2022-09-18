## List de Versiones

- v1 -> v2 : Cambio de la interpretación de los constraint de lista de funciones a lista de AST's
- v2 -> v3 : Definición de espacio minimalista donde todos los tipos básicos y herramientas están bajo un mismo domino
- v3 -> v4 : Unificación de la interface bajo los dos únicos tipos Domain y RandomValue

## Minmalista vs Unificada

```python
from search_space import dsl as ss
from search_space.sampler.distributions_name import UNIFORM, NORMAL

@space
class CustomSpace:
    def __ini__(
        self,
        interger: ss.N(0, 100, distribute_like = UNIFORM),
        double: ss.R(0, 100) | (lambda x: x != 0.1),
        string: ss.Categorical('red', 'white', 'black', distribute_like = NORMAL),
        list: ss.Tensor(ss.N(0, 100), shape_space = (10, ss.N(10, 20))) | (lambda x, i, j: x[i][j] != i)
    )
        pass


custom_class = CustomSpace()
custom_instance, sampler_context = custom_class.get_sample()
```

Sintaxis de los tipos básicos es muy intuitiva y similar a las definiciones matemáticas, pero:

- Sintaxis confusa de los tipos customs, que custom_class no sea una instancia de CustomSpace es raro
- La declaración de listas no son precisamente minimalista
- El tipado de las clases no estaba trabajado, aunque no es un gran problema

```python
from search_space.dsl import Domain, RandomValue
from search_space.sampler.distributions_name import UNIFORM, NORMAL

@space
class CustomSpace:
    def __ini__(
        self,
        interger: Domain[int](min=0, max=100, distribute_like = UNIFORM),
        double: Domain[float](min=0, max=100) | (lambda x: x != 0.1),
        string: Domain[str](options=['red', 'white', 'black'], distribute_like = NORMAL),
        list: Domain[int][10][Domain[int](min=10, max=20)]() | (lambda x, i, j: x[i][j] != i)
    )
        pass


custom_instance = RandomValue[CustomSpace]()
```

La sintaxis unificada aunque un poco más verbosa, se presenta a mi entender un poco más coherente,
cuenta con inferencia de tipos (osea custom_instance es de tipo CustomSpace), ademas cuenta con inferencia
interna de dominós

```python
a = RandomValue[int](min=0, max=100) # domino infinito [0, 100], type(a) == int
a = RandomValue[int](options = [i for i in range(100)]) # domino finito, search space categorical [0 ... 100], type(a) == int
a = RandomValue[int](min=0, max=50, options = [i for i in range(100)]) # domino finito, search space categorical [0 ... 50], type(a) == int
a = RandomValue[int][100](min=0, max=50) # type(a) == List[int], len(a) == 10, a[i] en [0, 50]
```

## Sintaxis de Restricciones, lambdas vs tuples

```python
from search_space import dsl as ss

@space
class CustomClass
    natural = ss.N() | (lambda x: x < 10)
    space = ss.Tensor(ss.N(), shape_space = (10)) | (lambda x, i: x[i] < CustomClass.natural)

```

La idea inicial fue la sintaxis de expresiones lambdas pero la referencia a los otros subdominos se
tornaba muy verbosas al tener que hacer referencia siempre a la clase en cuestión

```python
from search_space import UniversalVariable as x
from search_space import UniversalIndex as i
from search_space import dsl as ss

natural = ss.N() | (x < 10)
space = ss.Tensor(ss.N(), shape_space = (10)) | (x[i] < natural)

_list, context = space.get_sample()
_len, _ = natural.get_sample(context = context)
```

Luego pensé en sintaxis de tuplas pero las variables tenia que ser declaradas de forma externas,
con dos o tres podría ser viables, pero pensando en un tensor de dimension n > 2 supondría declarar
n + 1 variables. Razón por la cual se retorna a la sintaxis de expresiones lambdas incluyendo una
sintaxis para la declaración de variables dentro de la misma

```python
from search_space.dsl import Domain, RandomValue


@space
class CustomClass
    natural = Domain[int] | (lambda x: x < 10)
    space = Domain[int][10] | (lambda x, y, i: ( y in CustomClass.natural,  x[i] < y))


len_space = Domain[int](min=1, max=9)
custom_instance = RandomValue[CustomClass](lambda x, y: (y in len_space, x.natural < y))
```

## Sintaxis para Customs Space

### Lista de Problemas

- Declaraciones globales y referencias en restricciones
- Inferencia de Tipos
- Matching en nombres u orden
- Patrón Open-Close, separación entre funcionalidad y espacio

### Lista de Propuestas

```python
class CustomSpace:
    def __ini__(
        self,
        a: Domain[int](min=0, max=100, distribute_like = UNIFORM),
        b: Domain[float](min=0, max=100, distribute_like = UNIFORM),
    )
        pass
```

Propuesta inicial, basada en AutoGOAL, con el defecto de que el linter no tiene forma
de interpretar los tipos de a y b, por el resto lo considero funcional y expresivo

```python
class CustomSpace:
    inner_b = Domain[float](min=0, max=100, distribute_like = UNIFORM)

    def __ini__(
        self,
        a: int = Domain[int] | (lambda x, y: (y in inner_b, x < y)),
        b: float = inner_b
    )
        pass
```

Propuesta inmediatamente consecutiva, con referencia en FastApi, donde se resuelve el
problema del tipado de los parámetros, pero la expresividad queda determinada por el
usuario y los nombres de sus variables

```python
class SpaceFactory(ss.ClassFabricSearchSpace):
    def __space__(self, abi_class):
        self.b = Domain[float](min=0, max=100, distribute_like = UNIFORM)
        self.a = Domain[int](min=0, max=100, distribute_like = UNIFORM)
        self.b |= (lambda x, y: (y in self.a, x < y)),

        abi_class.registry('__init__', self.a, self.b)

class CustomClass:
    def __ini__(self, a: int, b: float)
        pass


n = SpaceFactory(CustomClass) # idea inicial
n = RandomValue[SpaceFactory](options = [CustomClass])
```

Intentando seguir una filosofía Open-Close, quería separar la definicion de la
clase de su descripción. La primera idea fue una factoría que describa la interface
que la misma puede samplear y luego aportar las distintas instancias. Aunque no es
una interface que me desagrada del todo, el procesos de declaración de la interface
no me convence, además de creer que los SS no son tan reutilizables como una interface. Elimina las declaraciones globales

```python
class DescriptionExample:

    def __init__(self, a: int, b:int) -> None:
        self.a = a
        self.b = b

@custom_space(_type = DescriptionExample)
class DescriptionExampleSpace():

    @parameters_space_description
    def __init__(self, a : Domain[int], b : Domain[float]) -> None:
        b |= (lambda x: x < a)

n = RandomValue[DescriptionExample]()
```

        Duda de diseño general, decoradores que alimentan factorías, como se
        manejan las duplicaciones

Continuando con la idea OC, pensé en la idea de la duplicación de implementaciones. Implica más código, fuerte desarrollo de meta-pro, y
la definición conjunta puede resultar bastante feo, supone matching en names o posición de los parámetros . Podría llegar a suponer
la optimización en cuanto a descripciones y elimina las declaraciones globales

```python
class ClassTest:
    a_domain = Domain[int][2](min= 10, max=100) | (lambda x, i: x[i] != 50 )

    # name matching :(
    @_('a', def_in = a_domain)
    def __init__(self, a: List[int]) -> None:
        pass
```

Ultima idea, referencia sly clase Parser, aunque implica name matching es la que más me gusta, es minimalista, expresiva, resuelve todos los problemas y aporta todas las ventajas, menos que se continuan con las definiciones globales

```python
class ClassTest:

    @space(
        lambda self, a: Domain[int][2], b: Domain[int],i: Index: (
            b > 10, b < 100,
            a[i] != 50, a[i] < b
    ))
    def __init__(self, a: List[int], b: int) -> None:
        pass


    @space(
        lambda self, x: Domain[int], y: Domain[float]: (
            x in self.a,
            y == self.b + x
    ))
    def method(self, x, y):
        pass
```

```python
class ClassTest:

    @space(
        lambda self, a, b, i: (
            b in Domain[int] | (b > 10, b < 100),
            a in Domain[int][2] | (a[i] != 50, a[i] < b)
    ))
    def __init__(self, a: List[int], b: int) -> None:
        pass


    @space(
        lambda self, x, y: (
            x in Domain[int] | (x in self.a),
            y in Domain[float] | (y == self.b + x)
    ))
    def method(self, x: float, y: float):
        pass
```

Dificultades:

- "Nuevos desarrollos"
- Perdida del orden de declaración, trayendo con sigo dependencia circulares
- Perdida de la referencia para relaciones externas, aparición del name maching

## Funciones y Predicados

##### Simples

```python

@SpaceDelegate
def simple_delegate(self, x: float, y: float):
    return x + y

X = Domain[int](min= 10, max = 100)
c = RandomValue[float]((lambda x: x < simple_delegate(X, 100))) # Restricción de domino
c = RandomValue[float]((lambda x: 120 < simple_delegate(x, 100))) # Backtraking aleatorio
```

##### Avanzados

```python

class AdvancedDelegate(SpaceDelegate):
    def __call__(self, x: float, y: float):
        return x + y


    # optimizacion de asts para evitar expresiones del tipo Sum(x, 10) > 100, cuando la forma ideal es x > Sub(100, 10)
    def __inverted__(self, x: float, y: float):
        pass

    # optimizacion de asts para evitar expresiones del tipo IsPar(x), cuando lo ideal seria x in [i for i in current_domain if i % 2 == 0]
    # para dominios infinitos current_domain = (min, max)
    def __modifier_infinite_domain__(self, x: float, y: float):
        pass


    # optimizacion de asts para evitar expresiones del tipo IsPar(x), cuando lo ideal seria x in [i for i in current_domain if i % 2 == 0]
    # para dominios infinitos current_domain = [m, n, o, ..... x]
    def __modifier_finite_domain__(self, x: float, y: float):
        pass
```

## Condicionales

```python

a = RandomValue[int](lambda x: (3 == 2) >> (x < 10)) # if () then ()
a = RandomValue[int](lambda x: (3 == 2) | (x < 10)) # if not x | then (cut or)
a = RandomValue[int](lambda x: (x > 5) | (x < 10))  # batch domain definition
a = RandomValue[int](lambda x: (3 == 2) & (x < 10)) # if x | then (cut and)
```
