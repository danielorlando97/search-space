# Modelación de Dependencias Contextuales para AutoGOAL

        autor: Daniel Orlando Ortiz Pacheco
        carrera: Ciencia de la Computación grupos: C-512

        tutor: Lic. Frank Sadan Naranjo
        co-tutor: Doc. Alejandro Piad Morffis

## Resumen

_AutoGOAL_ es uno de las bibliotecas del estado del arte que analiza la
problemática del AutoML. Esta se distingue del resto pues su elección
y diseño de la estrategia de búsqueda, _Evolución Gramatical Probabilística_
(**Probabilistic Grammatical Evolution**, **PGE**), le permite ser
independiente a la naturaleza del problema.

**PGE** requiere de la definición previa de una gramática, sobre la cual
realizar el procesos de búsqueda y optimización, por tanto la biblioteca
puede analizar todos los problemas cuyo espacio de búsqueda pueda ser
expresada como una de dichas gramáticas. Las herramientas existentes
previas al desarrollo de la presente tesis se limitaban a la definición e
inferencia de gramáticas libres del contexto

Este documento define una serie de políticas y reglas para ampliar el poder
descriptivo de herramientas como _AutoGOAL_ hasta la generación de gramáticas
sensibles al contextos sin dependencias circulares. Como resultado del
procesos investigativo se desarrollo una nueva biblioteca con la implementación
de las pautas antes mencionadas, dando lugar a la definición de un **DSL**
(_Lenguaje de Dominio Específico_,_Domain Specific Language_ ) capas de
describir, con una filosofía _Bottom-Up_, la composición de los distintos
espacios de búsqueda y las diferentes dependencias entre los componentes
del mismo, para posteriormente generar muestras de este

## Introducción

El _aprendizaje automático_ (_machine learning_, ML) es uno de los más famosos
y poderosos campos de la inteligencia artificial. Sin embargo, es un campo
donde el tiempo de aprendizaje e investigación es muy superior al de desarrollo
y donde la experiencia de los investigadores juega un papel fundamental tanto
en los resultados finales como de la efectividad del procesos investigativo.

El _AutoML_ (_Automated Machine Learning_), según [2], es un campo de investigación
que persigue la automatización incremental de todas las fases del desarrollo
de aplicaciones de aprendizaje automático. A diferencia del proceso de diseño
manual, el _AutoML_ permite explorar inteligentemente las mejores combinaciones
de algoritmos e hiperparámetros para la construcción de posibles soluciones.
Se han creado varias bibliotecas que aprovechan las tecnologías de _ML_
existentes para aplicar técnicas _AutoML_ y asi ofrecer una forma óptima
o semi óptima de combinar dichas tecnologías para dar solución de
los distintos problemas que puedan ser resueltos con las mismas.

La mayoría de estas tecnologías se centran en una familia específica de
algoritmos (como las redes neuronales) o en un entorno de problema específico
(como el aprendizaje supervisado a partir de datos tabulares). Sin embargo,
en escenarios prácticos, los investigadores necesitan combinar tecnologías de
diferentes marcos que no siempre están diseñados para interactuar entre sí,
por lo que, en muchos escenarios la herramienta ideal de _AutoML_ es aquella
que sea transversal a la naturaleza del problema y, extensible y flexible para
agregar y combinar dichas herramientas. Esta características describen y define a
_Automatic Generation, Optimization And Artificial Learning_ (_AutoGOAL_).

_AutoGOAL_ se autodefine en su documentación oficial[4] como:

    "... Una biblioteca de Python para encontrar automáticamente la
    mejor manera de resolver una tarea determinada ....
    Técnicamente hablando, _AutoGOAL_ es un marco para la síntesis de
    programas, es decir, encontrar el mejor programa para resolver un
    problema dado, siempre que el usuario pueda describir el espacio
    de todos los programas posibles"

Para que el usuario pueda describir el espacio de todos los programas posibles,
la biblioteca se apoya en un de sus submódulos principales, _Grammar_. El mismo
proporciona una abstracción de lo que se define como un algoritmo y un conjunto
de tipos (números, booleanos, etc.), para poder definir la naturaleza de los
valores de entrada, salida e hiperparámetros de los algoritmos que formen parte
del espacio de interés del usuario.

Con la lista de implementaciones del usuario se infiere una gramática libre
del contexto que describe el lenguaje de todos los potenciales programas validos
que se pueden construir anidando los algoritmos aportados. Gracias a toda esta
ingeniería de tipos y las interfaces que se brindan para describir el espacio
de búsqueda, al momento de inferir la gramática se puedan analizar
los tipos de entrada y salida de todos los algoritmos y asi excluir
los programas donde se intente secuenciar dos implementaciones tales que
la salida de una no sea consistente con la entrada de la siguiente. De esta
manera se logra descarta una gran cantidad de secuencias invalidas, incluso
antes de empezar a buscar, pero como se puede ver en los resultados de [1]
todavía quedan algunas instancias invalidas.

En muchos problemas las instancias invalidad en una ejecución de _AutoGOAL_
se pueden deber a parámetros iniciales de la ejecución, como tiempo de espera o
capacidad de memoria, dichas instancias al intentar ejecutarse superan los límites
prefijados y automáticamente son descartadas. Como para la biblioteca un algoritmo
es una función de la cual solo conoce sus tipos de entrada y salida, prever el
fallo de las instancias antes descritas previo a su ejecución, es equiva- \
lente al _Halting Problem_, problema que _Alan Turing_ demostró en 1936 que es
indecidible en una máquinas de _Turing_ [3].

Sin embargo existe otro conjunto de instancias invalidas relacionadas a la validez y
consistencia de los hiperparámtros iniciales. A lo largo del proceso de búsqueda
se exploran las "posibles soluciones" a partir de las distintas instancias generadas
por la gramática que se infirió de las definiciones del usuario. Como la misma
es libre del contexto los valores que se generan para cada terminal son
independientes entre si, pero, existen modelos en los que por definición o por
experiencia práctica se presenta una cierta dependencia entre los valores de sus
hiperparámetros.

Para describir dicho modelo en el contexto de _AutoGOAL_ se presentan dos opciones;
se puede definir el modelo tal cual, asignar a cada hiperparámetro la descripción
más extensa de su dominio y en el interior del algoritmo controlar que los mismos
cumplan con dichas reglas contextuales o de lo contrario lanzar un excepción en
tiempo de ejecución. O por el contrario, teniendo en cuanta dichas dependencias,
que el usuario defina un algoritmo por cada combinación de subdominios compatibles
de los hiperparámetros.

En la práctica, debido a las limitaciones de la biblioteca para describir dichas
dependencias contextuales, los desarrolladores prefieren incluir dichas instancias
invalidas a su espacio de búsqueda inicial, pues el procesos de evitarlas suele
ser bastante tediosos y poco escalable. Provocando consigo una dilatación del
tiempo de ejecución de _AutoGOAL_.

Dichas limitaciones dieron lugar a que los autores de la biblioteca propusieran
nuevo problema a resolver, el desarrollo de una herramienta capas de describir de
la forma más expresiva y simple posible la estructura interna de los
distintos espacios de búsqueda, las dependencias y relaciones existentes entre sus
componentes, y con la capacidad de generar muestras, dada una descripción
previa, de forma tal que cada uno de los dominio internos se reajuste al contexto
específico del procesos generativo en cuestión.

En respuesta este nuevo problema el presente documento plantea el desarrollo de una
nueva biblioteca que cuente con todas las arquitecturas y herramientas necesarias para
crear un _DSL_ capas de describir los distintos espacios de búsquedas bajo una
filosofía _"de abajo a arriba"_ (_Bottom-Up_), mediante el cual apoyado en la definición
de algunos tipos básicos el usuario pueda ser capas de componer la estructura interna de
su espacio de interés. Dicha herramienta cuenta además con una sintaxis, inspirado en el
paradigma funcional, para declararles restricciones y relaciones a cada uno de los
distintos subespacios, declaraciones que dan lugar a la definición de varios _AST's_
(_Astract Syntaxis Trees_, _Árboles de Sintaxis Abstracta_ ) los cuales son
visitados al momento del muestreo, para acotar los distintos subdominos y validar cada
uno de las selecciones internas.

Toda esta investigación y desarrollo se realizó con el objetivo de crear una
herramienta con la que se pueda describir al detalle, en un lenguaje de alto nivel,
los distintos espacios de búsqueda. Descripciones que debían ser,
por las características de la biblioteca, escalables, mantenibles, expresivas,
independientes de los procesos y algoritmos de generación de muestras, pero a
su vez capaz de transmitirle a estos los distintos dominios dinámicos para
cada contextos en cuestión.

Luego en un plano más generar se esperaba darle respuesta a las limitaciones
de _AutoGOAL_ que dieron lugar al problema inicial y que el resultado final sea
de utilidad en todos aquellos escenarios donde sea de interés describir espacios
aleatorios y generar muestras del mismo, como pueden ser los algoritmos genéticos,
donde puede ser interesante que la descripción de la población sea lo más expresiva
posible.

El documento continua con la descripción del procesos investigativo y de desarrollo
dividido en otros tres capítulos. Primero el _Estado del Arte_ donde se analizará
el marco teórico en que se realizaron las implementaciones y los trabajos realizados
en el sector hasta la fecha. Continuando con un segundo capitulo, _Propuesta de Solución_,
donde se detalla la propuesta planteada, partido de los objetivos iniciales y como
se cumplieron los mismo, hasta llegar al detalle de como se logró esto. Finalizando
con el capitulo de _Evaluación_, donde apoyado en ejemplos se evidenciara la efectividad
y expresividad de la propuesta.

# Referencias

1 - Suilan Estevez-Velarde, Yoan Gutierrez, Andres Montoyo and Yudivian Almeida-Cruz. AutoML strategy based on grammatical evolution: A case study about knowledge discovery from text

2 - Hutter, F., Kotthoff, L., & Vanschoren, J., editors (2018). Automated Machine Learning: Methods, Systems, Challenges. Springer (doi: 10.1007/978-3-030-05318-5). Recuperado de http://link.springer.com/978-3-030-05318-5, última visita Mayo del 2022.

3 - Hopcroft, John E.; Ullman, Jeffrey D. (1979). Introduction to Automata Theory, Languages, and Computation (1st ed.). Addison-Wesley. ISBN 81-7808-347-7.. See Chapter 7 "Turing Machines." A book centered around the machine-interpretation of "languages", NP-Completeness, etc.

4 - Sitio Oficial de la Biblioteca de Python AutoGOAL (https://autogoal.github.io), última visita Junio del 2022
