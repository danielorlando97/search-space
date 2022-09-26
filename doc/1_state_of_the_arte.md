# Modelación de Dependencias Contextuales para AutoGOAL

        autor: Daniel Orlando Ortiz Pacheco
        carrera: Ciencia de la Computación grupos: C-512

        tutor: Lic. Frank Sadan Naranjo
        co-tutor: Doc. Alejandro Piad Morffis

El espacio de búsqueda es una de las componentes principales de los sistemas
de _AutoML_, independientemente de la naturaleza de los mismo. La gran mayoría
de las herramientas de sector cuentan con una espacio de búsqueda muy definido,
normalmente determinado por el tipo de problema al que dan solución o a las
herramientas de _ML_ subyacente. En dichos casos, usualmente, llaman "description
del espacio de búsqueda" a la delimitación de los hyperparámetros de los
distintos modelos que se incluyen en dicha definición previa

Como se muestra en las investigaciones previas realizadas por [5] casi ninguna
de las herramientas del sector _AutoML_ cuenta con la capacidad real de describir,
en su totalidad y de forma detallada, su espacio de búsqueda. Independientemente
de esto, todo mecanismo y sintaxis que tenga como objetivo la descripción estructural
del campo de investigación, tiene su lugar en el procesos investigativo de la presente
tesis.

## Marco Teórico

### _Espacio de Búsqueda_

Subconjunto del universo tal que cada uno de sus elementos son soluciones factibles
para una problema dado.

### _Descripción del Espacio de Búsqueda_

Proceso mediante el cual, según las características del medio, se define una
jerarquía de estructuras y datos de forma tal que el receptor de dicha descripción  
pueda entender las dimensiones y características del espacio y sea capaz de generar
muestras del mismo.

En el casos específico del sector computacional el medio no suele ser un lenguaje
de programación de uso general, sino que las distintas herramientas de optimización, _ML_
o _AutoML_, suele implementar _DSL's_ o _frameworks_ en los que las descripciones se
pueda acercar un poco más al lenguaje natural.

### _DSL_ (_Lenguaje de Dominio Específico_,_Domain Specific Language_ )

Según [6] un lenguaje específico de dominio es un lenguaje especializado que sirve
para elevar el nivel de abstracción del software y facilitar el desarrollo del mismo.
Los DSL cuentan con múltiples formas de representación e implementación, desde
micro-modificaciones realizadas a lenguajes subyacentes, hasta proyectos a gran escala.

Para la presente investigación solo son de interés aquellos _DSLs_ que se construyen e
incorporan a un lenguaje subyacente, elevando el nivel de abstracción y la expresividad
del código con respecto a un domino específico.

### _DSLs_ orientados a descripciones

Los _DSLs_ pertenecientes al domino de la presente investigación tiene como objetivo
la descripción de una serie de conceptos para su posterior explotación. Esto supone que
los mismos cuenten con una ejecución separada en dos fases, que puede recordar a las
tradicionales estabas de los programas (_compilación_ y _ejecución_), pues en un
primer momento los desarrolladores escriben toda una serie de reglas y descripciones
que posteriormente serán utilizadas para la ejecución o ejecuciones en búsqueda de un
propósito final.

Debido al hecho de que estas herramientas, como se señalo anteriormente, representa un
pequeño engranaje en softwares mucho más grandes, entonces generalmente las dos fases
antes descritas suele tener lugar en al momento de la ejecución del sistema como un todo.
Por tanto depende en gran medida de las características del sistema general, el que se
pueda pensar en estos 'componentes descriptivos' como una herramienta de dos fases o
en un único componente

Precisamente los sistemas que son objeto de estudio de esta tesis presentan las
características necesarias para pensar en sus _DSLs_ como mecanismos de dos fases.
Esos sistemas de búsquedas, _ML_ y _AutoML_ suelen tener un alto costo temporal de
explotación e investigación del espacio, razón por la cual podemos considerar un costo
fijo todas las declaraciones e instancias iniciales necesarias para orquestar toda
la búsqueda y luego tener un segundo análisis temporal sobre la dilatación de dicho
sondeo del elemento optimo.

En estos casos específicos el autor considera razonable hablar de las dos fases de
estos _DSLs_ como _tiempo de compilación del DSL_ y _tiempo de ejecución del DSL_

### Tiempo de compilación del _DSL_

Definimos el tiempo de compilación de un _DSL_ como todas las operaciones puntuales que se
realizan para orquestar la infraestructura que dará soporte a la ejecución del objetivo
final del mismo. Dicha infraestructura debería permanecer inmutable en su mayoría
durante todos los procesos posteriores a la "compilación" del _DSL_.

### Tiempo de ejecución del _DSL_

Definimos el tiempo de ejecución del _DSL_ como todas las operaciones que realiza
la herramienta, posteriores a la "compilación" del mismo, para lograr su objetivo básico y
principal.

Véase por ejemplo el proceso de ejecución del módulo _Grammar_ de _AutoGOAL_, el cual es
la componente descriptiva del sistema. En un primer momento se analizan todas las descripciones
aportadas para inferir una gramática libre del contexto que describa el espacio de todos los
programas factibles, proceso que se pudiera interpretar como la "compilación del sistema". Y
posteriormente, de forma iterativa, se generan nuevas instancias de dicha gramática para ser
evaluadas y realizar otras operaciones ajenas al componente descriptivo. Si se interpreta que
el objetivo final del modulo _Gramar_ es la generación de soluciones factibles, entonces se
podrían decir que una vez que inicia una ejecución de _AutoGOAL_, luego de la "compilación"
de sus descripciones, su _DSL_ se ejecuta múltiples veces hasta que el sistema encuentra una
respuesta al problema planteado.

### Python para _DSL_

Como el resultado de la presente tesis es un _DSL_ atado a un lenguaje de propósito general
subyacente. Dicho lenguaje de contar con una serie de características especiales,
que permita a el autor modificar la semántica de su sintaxis original. Y aunque la gran mayoría
de los sistemas de la actualidad que podrían estar interesados en la explotación de la solución
propuesta están escritos en _Python_. La elección de dicho lenguaje como lenguaje subyacente
para la implementación de la propuesta planteada no se encuentra influenciada solo por dicha
situación, sino que además _Python_ cuenta con potentes y cómoda herramientas para modificar  
la semántica de su sintaxis y desarrollar la metaprogramación.

Según [14], _Python_ es un lenguaje de programación de alto nivel y de propósito general.
Python es de tipado dinámico y fuerte, pero existen bibliotecas, como _typing_, que haciendo
uso de la metaprogramación y otras técnicas, son capaces de modificar la semántica del
lenguaje para ofrecer una experiencia de usuario similar a la de los lenguajes estéticamente
tipados.

Una de las características que hacen a este lenguaje tan flexible e ideal para la metaprogramción,
es la filosofía bajo la que describe todos los procesos y transiciones de sus objetos. El
interprete del lenguaje define una lista de "métodos mágicos", uno por cada operación básica
de software, los cuales cuanta con sus propias implementaciones básicas, pero que pueden ser
redefinidos en todo momento. Como señala [14], los "métodos mágicos" son los que comienzan y
terminan con el doble guión bajo, entre los que se pueden citar por ejemplo; `__and__`,
`__sub__`, `__div__`, `__mul__` y otra larga lista de funciones que hacen referencia
a las operaciones aritméticas y de comparación, `__call__` método que describe el comportamiento
de un objeto cuando se intenta usar como función, `__getattribute__` o `__getitem__`
que describen los comportamientos cuando se intenta acceder a los miembros de una clase o a
un indice determinado respectivamente. La lista es extremadamente larga y crece a medida
que aparecen nuevos bibliotecas del lenguaje.

En [14] se define el término metaprogramación como a la posibilidad de que un programa tenga
conocimiento o se manipule a sí mismo. En _Python_ cada pequeño elemento del lenguaje
representa un objeto. A diferencia de otros lenguajes, donde la declaración de funciones y
clases no son más que punteros a direcciones de memoria donde se alojan sus respectivos códigos,
en _Python_ cada definición tiene como resultado la instancia de una determinada clase que se
referencia a partir del nombre de dicha definición y que desde el preciso momento de su
definición dicha instancia puede ser modificada de todas las maneras que soporte el lenguaje
y la semántica del contexto.

El más popular ejemplo de lo antes expresado son los decoradores. Estos representan una de las
cualidades de más alto nivel del paradigma funcional, las funciones de orden superior (funciones
que esperan funciones como parámetros). Los decoradores ya no son una sintaxis novedosa en el
mundo de los lenguajes de programación; pero la sencillez de estos en _Python_ sigue resaltando
por encima del resto, pues según su filosofía, los decoradores no son más que una función
simple donde el argumento es el objeto resultante de la definición subyacente. Esta es una
increíble herramienta para escribir metaprogramas pues con solo una linea de código más por
encima de una definición, ya sea de función o de clase, se puede transformar el objeto al que
apunta el nombre de la definición que cualquier otra instancia. Esto permite por ejemplo
simplificar la sintaxis para declarar una jerarquía de clases simple, donde la clase que hereda
únicamente le interesa sobreescribir un método en particular, pues bastaría con decorar la
una función "x" para que cuando se le intente ejecutar se cree la instancia clases "y"
que tiene un método "z" que llama a la función "x"

La más alta expresión de esta filosofía, donde toda definición es la instancia de un objeto,
son las metaclases. Una metaclase es el clase que describe la naturaleza de las instancias
resultantes de la declaración de nuevas clases. El lenguaje define la metaclases básica
**type** y brinda las herramientas necesarias para crear nuevas y personalizar la asignación
de su respectiva metaclases para cada clase que el usuario define. El procesos de instanciación
de una nueva clase definida por el usuarios pasa por un pipeline de 3 "métodos mágicos" que
tiene origen en el método `__call__` de la instancia de su metaclase. Esto es otra gran
característica para la flexibilización de la semántica pues por ejemplo, bajo el nombre de una
misma clase, en el momento de crear una nueva instancia, se podrían crear la instancia adecuada
de toda una jerarquía según las características de los parámetros iniciales.

Además la biblioteca estándar del lenguaje incluye el módulo _inspect_, que como indica [15],
proporciona varias funciones útiles para ayudar a obtener información sobre objetos vivos
como módulos, clases, métodos y funciones. Hay cuatro tipos principales de servicios que ofrece
este módulo: comprobación de tipos, obtención del código fuente, inspección de clases y funciones,
y examen de la pila del intérprete. Lo cual supone una inmensa fuente de metadatos que unido
a todo lo antes expuestos transforman a este lenguaje en el ambiente ideal para el desarrollo de
_DSLs_ y _framewors_ de gran expresividad.

## Estado del Arte

En función del marco teórico en que se desarrollo la investigación y teniendo en cuenta
que el estado del arte respecto a la descripción de espacios de búsqueda, en este momento,
se encuentra concentrado en los sistemas _AutoML_ y bibliotecas de optimización, entonces se
realizo una selección y estudio de las herramientas del sector, que contarán con algún
mecanismo para expresar la dimension o estructura de su espacio de búsqueda. Dicha
herramienta debía ser; un mecanismo integrado con el lenguaje de propósito general
subyacente, en los que el objetivo final de cada descripción fuera la generación de
muestras. El listado final quedo integrado por:

- AutoGOAL [4]: Biblioteca de _AutoML_, escrita en _Python_, transversal a la naturaleza
  de los problemas y de las herramientas subyacentes. Mediante su módulo _Grammar_ ofrece
  un listados de tipos y abstracciones con las que los desarrolladores pueden describir
  su espacio de búsqueda.
- HyperOpt [7]: Biblioteca de _Python_ que intenta resolver el problema de la optimización
  paramétrica siendo independiente a la función en cuestión. La misma define una sintaxis y
  una lista de funciones para expresar la definición de cada uno de los parámetro de la
  función en cuestión
- Ray AI Runtime (AIR) [8]: Ray es un marco unificado para escalar aplicaciones de IA y Python.
  Y AIR es su conjunto de herramientas de código abierto para crear aplicaciones de IA, en
  la cual incluye una lista de funciones con las que los desarrolladores pueden expresar
  las dimensiones de los distintos hiperparámetros
- Chocolate [9]: Chocolate es un marco de optimización completamente asíncrono que depende
  únicamente de una base de datos para compartir información entre los trabajadores. Chocolate
  ha sido diseñado y optimizado para la optimización de hiperparámetros, donde cada evaluación
  de funciones tarda mucho en completarse y es difícil de paralelizar. Y como tal define una
  sintaxis y una lista de funciones para definir los dominós de dichos hiperparámetros
- Optuna [10]: Optuna es un marco de software de optimización automática de hiperparámetros,
  especialmente diseñado para el aprendizaje automático. El cual inyecta la instancia de una
  clase predefinida para seguir la evolución de dichos hiperparámetros asi como
  una lista de funciones para describir las características de los mismos
- AutoGloun [11]: Biblioteca de _AutoML_, escrita en _Python_, que permite utilizar y ampliar
  AutoML de forma sencilla, centrándose en el ensamblaje automatizado de pilas, el aprendizaje
  profundo y las aplicaciones del mundo real que abarcan datos de imágenes, textos y tablas.
  Aprovechando el ajuste automático de hiperparámetros, la selección/ensamblaje de modelos,
  la búsqueda de arquitecturas y el procesamiento de datos. Mejorar/ajustar fácilmente sus
  modelos y pipelines de datos a medida, o personalizar AutoGluon para su caso de uso. Para
  dicha personalización la biblioteca combina la definición de una sintaxis para la descripción
  estructural de los hiperparámetros con una lista de tipos para expresar la dimension de los
  mismo
- AutoSklearn [12]: Biblioteca de _AutoML_, escrita en _Python_, sustentados sobre conjunto de
  herramientas de aprendizaje automático de scikit-learn. Permite a los desarrolladores personalizar
  sus modelos ofreciendo una lista de tipos con los que restringir los distintos dominios de cada
  hiperparámetro, junto con una sintaxis específica para la declaración de los mismo
- TPOT [13]: TPOT es una herramienta de aprendizaje automático en Python que optimiza los procesos
  de aprendizaje automático mediante programación genética. Este define una sintaxis para describir
  la lista de modelos a explorar y sus distintos hiperparámetros

Aunque la investigación realizada en [6] se enfoca más en la clasificación de DSL que
representas proyectos más grandes que aquellos que son objeto de estudio para esta
investigación en concreto, estudiando las clasificaciones y características que plantea,
el autor pudo seleccionar varias que son acordes para describir el estado del arte
de los DSL's que hasta el momento se dan la tarea de describir espacios de búsqueda.
A continuación se enumeran y detallan las características con las que se pretende
describir el estado y las propiedades de los trabajos realizados en el área hasta el
momento:

- Estilo de la Sintaxis Concreta: Esta puede ser imperativa o funcional
- Objetivo del Sistema Subyacente: En el caso particular del campo de interés de esta
  investigación la mayoría de las herramientas se encuentra relacionadas con el _ML_ o
  _AutoML_, pero dentro de ambos campos existen múltiples subdominios y razones por las que
  sería de interés describir un dominio determinado
- Activo Objetivo: Nombre con el que se describe el resultado esperado por las transformaciones
  del _DSL_. En los casos analizados por [6] suelen ser archivos de textos, gráficos o llamadas
  al sistema, pero en esta investigación el autor reinterpreto esta característica, debido a la
  naturales del campo de investigación, y por tanto los activos objetivos pasan a describir a
  los efectos que provoca el empleo del mismo dentro de un programa, las instancias que
  genera o las modificaciones que espera conseguir
- Integración con el Lenguaje Subyacente: Lista de herramientas y características de las
  que se valen los desarrolladores de cada uno de los DSL's para dar lugar a los mismo dentro
  del lenguaje subyacente

<!-- - Transformaciones Operativas: Esta parte abarca las características relacionadas con
  la aplicación de una transformación DSL. Se distinguen la técnica, la ejecución,
  la programación y la variabilidad -->

- Desacoplamientos Descripción - Generación: Describe el nivel de desacoplamiento entre
  las herramientas que soportan las descripciones de los distintos espacios de búsqueda con
  los mecanismos para generar las muestras de dichas descripciones. Un diseño ideal
  es aquel que permita para una misma definición probar varias formas de generar muestras.

- Características que Conduce el Diseño: Detrás de las descripciones de los espacios de
  búsqueda existe mucho carga teórica de diversas esferas no solo la computación y el _ML_,
  sino que también juegan un papel importante la estadística, las probabilidades y otros muchos
  campos de las matemáticas. Para la definición de los distintos DSL's los autores se inspiraron
  en muchos de estos campos para dar expresividad a los mismo, dicha inspiración es la que se
  intentara reflejar cuando se resalte esta detalle para cada uno de los trabajos previos
- Capacidad de Generación y Definición: En este punto se realizará una comparación según tres
  de los puntos fuertes de la solución presentada por este trabajo:
  - Definición de dependencias y relaciones entre los componentes internos de una misma descripción
  - Descripción y generación de espacio de búsqueda de dimensiones aleatorias, por ejemplo el espacio
    de los vectores de dimension aleatoria
  - Estructuras de controles de flujo para las descripción de espacios opcionales

| DSL                   | Estilo de la Sintaxis Concreta | Objetivo del Sistema Subyacente                                                    | Activo Objetivo                                                                                                                                                                                                                                                                                                                                 | Integración con el Lenguaje Subyacente                                                                                                                                                                                                                                                                                       | Desacoplamientos Descripción - Generación                                                                                                                                                              | Características que Conduce el Diseño                                                                                               | Capacidad de Generación y Definición                                                                                                                                                                                                                                                      |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AutoGOAL              | Funcional                      | AutoML, Selección de Modelos, Optimización paramétrica                             | - En tiempo de compilación: Gramática Libre del Contexto. <br />- En tiempo de ejecución: Instancia de la clase Pipeline                                                                                                                                                                                                                        | Hace uso de descripción de tipos de los parámetros y resultados de las funciones de cada clase                                                                                                                                                                                                                               | Cada uno de los tipos básicos tiene su propia definición de su mecanismo generativo                                                                                                                    | Orientado por tipos que hacen referencia a la función de la variables dentro del problema del AutoML                                | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias salvo el Pipeline principal<br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                         |
| HyperOpt              | Funcional                      | Biblioteca de optimización paramétrica                                             | - En tiempo de compilación: Diccionario que iguala el nombre del parámetro en cuestión a su función generadora <br />- En tiempo de ejecución: Copia de dicho diccionario con las muestras generadas                                                                                                                                            | Hace uso de los diccionarios y funciones del lenguaje                                                                                                                                                                                                                                                                        | Asigna explícitamente las funciones generadoras a cada una se las variables                                                                                                                            | Orientado por las distintas distribuciones con las que se generan las muestras de las distintas variables aleatorias                | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias <br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                    |
| Ray AI Runtime (AIR)  | Funcional                      | Marco unificado para escalar aplicaciones de IA y Python                           | - En tiempo de compilación: Diccionario que iguala el nombre del parámetro en cuestión a su función generadora <br />- En tiempo de ejecución: Copia de dicho diccionario con las muestras generadas                                                                                                                                            | Hace uso de los diccionarios y funciones del lenguaje                                                                                                                                                                                                                                                                        | Asigna explícitamente las funciones generadoras a cada una se las variables                                                                                                                            | Orientado por las distintas distribuciones con las que se generan las muestras de las distintas variables aleatorias                | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias <br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                    |
| Chocolate             | Funcional                      | Biblioteca de optimización paramétrica                                             | - En tiempo de compilación: Diccionario que iguala el nombre del parámetro en cuestión a su función generadora <br />- En tiempo de ejecución: Copia de dicho diccionario con las muestras generadas                                                                                                                                            | Hace uso de los diccionarios y funciones del lenguaje                                                                                                                                                                                                                                                                        | Asigna explícitamente las funciones generadoras a cada una se las variables                                                                                                                            | Orientado por las distintas distribuciones con las que se generan las muestras de las distintas variables aleatorias                | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias<br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                     |
| Optuna                | Imperativo                     | Biblioteca de optimización paramétrica                                             | - En tiempo de compilación: Orquesta la arquitectura necesaria para la optimización paramétrica. <br />- En tiempo de ejecución: Generación muestras para cada una de las variables definidas en el scope de la función                                                                                                                         | Basado en la inversión de dependencia inyecta el motor de generación a la función objetivo para que imperativamente genera las muestras necesarias                                                                                                                                                                           | Las descripciones se implementa de forma imperativa haciendo uso del scope de las funciones, las variables del lenguaje y las funciones implementadas por el generador de muestras                     | Orientado por las distintas distribuciones con las que se generan las muestras de las distintas variables aleatorias                | - Describe dependencias contextuales ordenado de forma topológica la generación de muestras <br />- Puede describir espacios de dimensiones aleatorias generando primero las dimensiones y luego las muestras <br />- Cuenta con las estructuras de control de flujo propias del lenguaje |
| AutoGloun             | Funcional                      | AutoML, Selección de Modelos, Optimización paramétrica                             | - En tiempo de compilación: Diccionario que iguala el nombre del parámetro en cuestión a la instancia de su clase generadora. <br />- En tiempo de ejecución: Copia de dicho diccionario con las muestras generadas                                                                                                                             | Hace uso de los diccionarios del lenguaje, junto a una lista de clases implementadas en el mismo                                                                                                                                                                                                                             | Cada uno de los tipos básicos tiene su propia definición de su mecanismo generativo                                                                                                                    | Orientado por tipos que hacen referencia a la función de la variable en cuestión dentro del problema del AutoML                     | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias <br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                    |
| AutoSklearn           | Funcional                      | AutoML, Selección de Modelos, Optimización paramétrica                             | - En tiempo de compilación: Mediante la ejecución del método estático `get_hyperparameter_search_space` se crea una instancia de la clase `ConfigurationSpace` que contiene cada una de las descripciones. <br />- En tiempo de ejecución: Instancia de clasificador personalizado al que se le inyectan las muestras como parámetros iniciales | Hace uso de los métodos estáticos del lenguaje, para instanciar cada una de las clases que describirá el espacio de los parámetros iniciales. Para enlazar dichas clases con su posición entre los parámetros del constructor usa los metadatos de la función para realizar la asignación según los nombres de las variables | Cada uno de los tipos básicos tiene su propia definición de su mecanismo generativo                                                                                                                    | Orientado por tipos que hacen referencia a la su mecanismo generativo                                                               | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias <br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                    |
| TPOT                  | Funcional                      | AutoML, Selección de Modelos, Optimización paramétrica                             | - En tiempo de compilación: Diccionario que enumera la lista de modelos seleccionables y describe las dimensiones de sus hiperparámetros . <br />- En tiempo de ejecución: Instancia de las distintas clases que pueden formar parte del pipeline final                                                                                         | Hace uso de descripción de la sintaxis de los diccionarios del lenguaje para describir su espacio                                                                                                                                                                                                                            | No hace referencia explicita a la distribución de sus hiperparámetros                                                                                                                                  | Orientado por los nombres de los algoritmos que forman parte del procesos de selección de modelos y los tipos de sus hiperparámetro | - No puede describir dependencias contextuales<br />- No puede describir espacios de dimensiones aleatorias <br />- No cuenta con estructuras de control de flujo en sus descripciones                                                                                                    |
| Propuesta de Solución | Funcional                      | Biblioteca para describir y generar muestras de los distintos espacios de búsqueda | - En tiempo de compilación: Instancia los mecanismo generadores y construye los AST's que describen las dependencias y relaciones internas. <br />- En tiempo de ejecución: Muestra del espacio que cumple con todas las restricciones descritas                                                                                                | Hace uso de descripción de tipos de los parámetros, en las que apoyado en una clase principal con la redefinición de alguno de sus operadores permite la descripción de restricciones mediante la sintaxis de funciones lambdas del lenguaje                                                                                 | Cada una de las instancias de los tipos básicos y personalizados hacen referencio al nombre de su mecanismo generador, que posteriormente puede ser mapeado a cualquier clase generadora personalizada | Orientado por tipos originales de las muestras que se generarán                                                                     | - Puede describir dependencias contextuales<br />- Puede describir espacios de dimensiones aleatorias <br />- Cuenta con estructuras de control de flujo en sus descripciones                                                                                                             |

Analizando el estado del arte mediante la comparación antes expuesta se
resaltar varias puntos. La mayoría de las herramientas de la actualidad
no resuelven ninguno de los problemas a los que el presente trabajo intenta
dar respuesta. Todas las herramientas estudiadas interpretan que el mecanismo
generativo es un elemento integrado de forma natural en las descripciones de
los espacios de búsqueda, idea que el autor considera que no es el mejor
diseño con respecto a la escalabilidad y modularidad de las implementaciones.
Una cantidad considerable de los ejemplos de solución se apoyan en los diccionarios
y la comparación textual entre los nombres de los argumentos con las llaves
de dichos diccionarios o nombres que se le asignan a las distintas instancias de
las clases básicas.

Además cada uno de los **DSLs** analizado presentan diseños muy influenciado
por el domino de la herramienta subyacente. En los casos en que el objetivo
principal de la misma es la optimización paramétrica, las descripciones se
encuentran constituidas por los nombres de las distribuciones de cada una de
las variables aleatorias. Mientras que herramientas especializadas en la solución
del problema del **AutoML**, las herramientas descriptivas se ven más influenciada
por las funciones de estos parámetros dentro de los distintos algoritmos. Bajo este
análisis una herramienta con el propósito principal de describir los espacios de
búsqueda, como sería de propuesta de solución, debe presentar una sintaxis expresiva
respeto a los tipos que serán generados como resultado final.

Por último, se destaca el caso de la biblioteca _Optuna_ que siendo la herramienta
que se decanta por una filosofía imperativa, cuenta con mecanismo para dar respuesta
a los problemas que dieron lugar a la presenta investigación. Pese a la flexibilidad
y la potencia de la propuesta no es la sintaxis ideal para las descripciones, como se
evidencia en la elección del resto de los sistemas que se decantan por el paradigma
funcional. Las descripciones resultantes de estas sintaxis, pese la amplia gama de
dominios que puede generar, a medida que los espacios se complejizan las implementaciones
se torna muy verbosa y relativamente poco legibles. Además esta en esta propuesta se
resolverían todas las restricciones y dependencias en tiempo de ejecución, mientras
que una sintaxis funcional da espacios a realizar múltiples optimizaciones para
minimizar el computo en tiempo de ejecución.

# Referencias

1 - Suilan Estevez-Velarde, Yoan Gutierrez, Andres Montoyo and Yudivian
Almeida-Cruz. AutoML strategy based on grammatical evolution: A case
study about knowledge discovery from text

2 - Hutter, F., Kotthoff, L., & Vanschoren, J., editors (2018). Automated
Machine Learning: Methods, Systems, Challenges. Springer
(doi: 10.1007/978-3-030-05318-5). Recuperado de
http://link.springer.com/978-3-030-05318-5, última visita Mayo del 2022.

3 - Wikipedia

4 - Sitio Oficial de la Biblioteca de Python AutoGOAL
(https://autogoal.github.io), última visita Junio del 2022

5 - Estevanell-Valladares, Ernesto Luis; Estevez-Velarde, Suilan;
Piad- Morffis, Alejandro; Gutiérrez, Yoan; Montoyo, Andrés; Almeida-Cruz,
Yudivian. Towards the Democratization of Machine Learning using AutoGOAL

6 - Benoît Langlois, Consuela-Elena Jitia, Eric Jouenne. DSL Classification

7 - Documentación de HyperOpt, Search Spaces Definition,
http://hyperopt.github.io/hyperopt/getting-started/search_spaces/, última
visita Sept del 2022.

8 - Documentación Ray,Search Space API,
https://docs.ray.io/en/latest/tune/api_docs/search_space.html, última
visita Sept del 2022.

9 - Chocolate, Search Space Representation,  
https://chocolate.readthedocs.io/en/latest/api/space.html, última
visita Sept del 2022.

10 - Optuna, Pythonic Search Space,
https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html,
última visita Sept del 2022.

11 - AutoGloun, Custom Model,
https://auto.gluon.ai/dev/tutorials/index.html?highlight=search%20space,
última visita Sept del 2022.

12 - Auto-Sklearn,
https://automl.github.io/auto-sklearn/master/examples/80_extending/example_restrict_number_of_hyperparameters.html?highlight=hyperparamete,
última visita Sept del 2022.

13 - TPOT, http://epistasislab.github.io/tpot/using/#customizing-tpots-operators-and-parameters,
última visita Sept del 2022.

14 - Block Online Real Python, https://realpython.com, última visita Sept del 2022.

15 - Documentación Online Oficial de Python, https://docs.python.org/3, última visita Sept del 2022.
