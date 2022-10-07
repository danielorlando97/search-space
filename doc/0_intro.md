# Modelación de Dependencias Contextuales para AutoGOAL

        autor: Daniel Orlando Ortiz Pacheco
        carrera: Ciencia de la Computación grupos: C-512

        tutor: Lic. Frank Sadan Naranjo
        co-tutor: Doc. Alejandro Piad Morffis

## Resumen

AutoGOAL es una de las bibliotecas del estado del arte que analiza la
problemática del AutoML. Esta se distingue del resto por ser transversal
a la naturaleza del problema, característica que es consecuencia directa
de su elección y diseño de la estrategia de búsqueda,
Evolución Gramatical Probabilística
(Probabilistic Grammatical Evolution, PGE).

PGE realiza el proceso de búsqueda y optimización a partir de una
gramática previamente definida. Por tanto, mientras mejor sea la
capacidad de la biblioteca para describir espacios de búsqueda y generar
sus respectivas gramáticas, más amplio será el conjunto de los problemas
que esta podrá intentar resolver. Las herramientas existentes previas al
desarrollo de la presente tesis se limitaban a la definición e inferencia
de gramáticas libres del contexto

En este documento se presenta una nueva herramienta, que al integrarse con
AutoGOAL podría ampliar el poder descriptivo de este hasta la
generación de gramáticas sensibles al contextos sin dependencias circulares.
Dicha nueva biblioteca define un DSL
(Lenguaje de Dominio Específico, Domain Specific Language) capaz de
describir, con una filosofía Bottom-Up, la composición de los
espacios de búsqueda y las relaciones y restricciones entre sus
componentes internos, para posteriormente generar muestras apoyándose en  
dichas descripciones

## Introducción

El aprendizaje automático (machine learning, ML) es uno de los más famosos
y poderosos campos de la inteligencia artificial. Sin embargo, es un campo
donde el tiempo de aprendizaje e investigación es muy superior al de desarrollo
y donde la experiencia de los investigadores juega un papel fundamental tanto
en los resultados finales como en la efectividad del procesos investigativo.

AutoML (Automated Machine Learning), según [2], es un campo de investigación
que persigue la automatización incremental de todas las fases del desarrollo
de aplicaciones de aprendizaje automático. A diferencia del proceso de diseño
manual, AutoML permite explorar inteligentemente las mejores combinaciones
de algoritmos e hiperparámetros para la construcción de posibles soluciones.

Se han creado varias bibliotecas que aprovechan las tecnologías de ML
existentes para aplicar técnicas AutoML y asi ofrecer una forma óptima
o semi óptima de combinar dichas tecnologías para dar solución a
los problemas que puedan ser resueltos con las mismas. La mayoría de dichas  
herramientas se centran en una familia específica de algoritmos (como las
redes neuronales) o en un entorno de problema específico (como el
aprendizaje supervisado a partir de datos tabulares). Sin embargo, en
escenarios prácticos, los investigadores necesitan combinar tecnologías de
diferentes marcos que no siempre están diseñados para interactuar entre sí.
En muchos escenarios la herramienta ideal de AutoML es aquella que sea
transversal a la naturaleza del problema, flexible para combinar herramientas
en principio incompatibles y extensible para agregar nuevas tecnologías o
implementaciones propias. Estas características describen y definen a
Automatic Generation, Optimization And Artificial Learning (AutoGOAL).

AutoGOAL se autodefine en su documentación oficial[4] como:

    "... Una biblioteca de Python para encontrar automáticamente la
    mejor manera de resolver una tarea determinada ....
    Técnicamente hablando, _AutoGOAL_ es un marco para la síntesis de
    programas, es decir, encontrar el mejor programa para resolver un
    problema dado, siempre que el usuario pueda describir el espacio
    de todos los programas posibles"

Para que el usuario pueda describir el espacio de todos los programas posibles,
la biblioteca se apoya en un de sus submódulos principales, Grammar. El mismo
proporciona una abstracción de lo que se define como un algoritmo y un conjunto
de tipos (números, booleanos, etc.), para poder definir la naturaleza de los
valores de entrada, salida e hiperparámetros de los algoritmos que formen parte
del espacio de interés del usuario.

Con la lista de descripciones del usuario se infiere una gramática libre
del contexto que describe el lenguaje de todos los potenciales programas validos
que se pueden construir combinando los algoritmos aportados. Al momento de inferir
la gramática se analizan los tipos de entrada y salida de todos los algoritmos y se
excluyen los programas donde se intente secuenciar dos implementaciones tales que
la salida de una no sea consistente con la entrada de la siguiente. De esta
manera se logra descarta una gran cantidad de secuencias invalidas, incluso
antes de empezar a buscar, pero como se puede ver en los resultados de [1]
todavía quedan algunas instancias invalidas.

En muchos casos las instancias invalidas son consecuencias de los
parámetros iniciales de la búsqueda, como el tiempo de espera o la capacidad de memoria.
En estos casos durante la ejecución de la instancia en cuestión se superan los límites
prefijados y automáticamente es descartada como posible solución. Como para la
biblioteca un algoritmo es una función de la cual solo conoce sus tipos de entrada y
salida, prever el fallo de las instancias antes descritas previo a su ejecución,
es equivalente al Halting Problem, problema que Alan Turing demostró en 1936 que es
indecidible en una máquinas de Turing [3].

Sin embargo existe otro conjunto de instancias invalidas relacionadas a la validez y
consistencia de los hiperparámtros iniciales. A lo largo del proceso de búsqueda
se exploran las "posibles soluciones" a partir de las distintas instancias generadas
por la gramática que se infirió de las definiciones del usuario. Como la misma
es libre del contexto los valores que se generan para cada terminal son
independientes entre si, pero, existen modelos en los que por definición o por
experiencia práctica se presenta una cierta dependencia entre los valores de sus
hiperparámetros.

Para describir dicho modelo en el contexto de AutoGOAL se presentan dos opciones;
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
tiempo de ejecución de AutoGOAL.

Dichas limitaciones dieron lugar a que los autores de la biblioteca propusieran
nuevo problema a resolver, el desarrollo de una herramienta capaz de describir de
la forma más expresiva y simple posible la estructura interna de los
distintos espacios de búsqueda, las dependencias y relaciones existentes entre sus
componentes, y con la capacidad de generar muestras, dada una descripción
previa, de forma tal que cada uno de los dominio internos se reajuste al contexto
específico del procesos generativo en cuestión.

En respuesta a este nuevo problema el presente documento plantea el desarrollo de una
nueva biblioteca que cuente con todas las arquitecturas y herramientas necesarias para
crear un DSL capaz de describir los distintos espacios de búsquedas bajo una
filosofía "de abajo hacia arriba" (Bottom-Up), mediante el cual apoyado en la definición
de algunos tipos básicos el usuario pueda ser capaz de componer la estructura interna de
su espacio de interés. Dicha herramienta cuenta además con una sintaxis, inspirado en el
paradigma funcional, para declararles restricciones y relaciones a cada uno de los
distintos subespacios, declaraciones que dan lugar a la definición de varios AST's
(Astract Syntaxis Trees, Árboles de Sintaxis Abstracta) los cuales son
visitados al momento del muestreo, para acotar los distintos subdominos y validar cada
uno de las selecciones internas.

Toda esta investigación y desarrollo se realizó con el objetivo de crear una
herramienta con la que se pueda describir detalladamente, en un lenguaje de alto nivel,
los distintos espacios de búsqueda. Descripciones que debían ser,
por las características de la biblioteca, escalables, mantenibles, expresivas,
independientes de los procesos y algoritmos de generación de muestras, pero a
su vez capaz de transmitirle a estos los distintos dominios dinámicos para
cada contextos en cuestión.

Luego en un plano más general se esperaba darle respuesta a las limitaciones
de AutoGOAL que dieron lugar al problema inicial y que el resultado final sea
de utilidad en todos aquellos escenarios donde sea de interés describir espacios
aleatorios y generar muestras del mismo, como pueden ser los algoritmos genéticos,
donde puede ser interesante que la descripción de la población sea lo más expresiva
posible.

El documento esta organizado en tres capítulos. Un primer capítulo donde se analiza
el marco teórico en que se realizaron las implementaciones y los trabajos realizados
en el sector hasta la fecha. Otro donde se detalla la propuesta, objetivos, alcance e
implementación. Y por último un capítulo donde apoyado en ejemplos se evidenciara
la efectividad y expresividad de la propuesta.

# Referencias

1 - Suilan Estevez-Velarde, Yoan Gutierrez, Andres Montoyo and Yudivian Almeida-Cruz. AutoML strategy based on grammatical evolution: A case study about knowledge discovery from text

2 - Hutter, F., Kotthoff, L., & Vanschoren, J., editors (2018). Automated Machine Learning: Methods, Systems, Challenges. Springer (doi: 10.1007/978-3-030-05318-5). Recuperado de http://link.springer.com/978-3-030-05318-5, última visita Mayo del 2022.

3 - Hopcroft, John E.; Ullman, Jeffrey D. (1979). Introduction to Automata Theory, Languages, and Computation (1st ed.). Addison-Wesley. ISBN 81-7808-347-7.. See Chapter 7 "Turing Machines." A book centered around the machine-interpretation of "languages", NP-Completeness, etc.

4 - Sitio Oficial de la Biblioteca de Python AutoGOAL (https://autogoal.github.io), última visita Junio del 2022
