# Modelación de Dependencias Contextuales para AutoGOAL

        autor: Daniel Orlando Ortiz Pacheco
        carrera: Ciencia de la Computación grupos: C-512

        tutor: Lic. Frank Sadan Naranjo
        co-tutor: Doc. Alejandro Piad Morffis

<!--

Prototype

Introduce Example, that AutoGOAL can't resolver

What is Search Space?
What is DSL? Classification By Reference, and selected features

Reference Description and Classification
Table
Conclusion

-->

## Marco Teórico

<!--
DSL
Metodologías  Bottom-Up Top-Down
-->

## Estado del Arte

<!--
¿Quiénes ya han tratado el mismo tema?
¿Cuáles son sus hipótesis y teorías?
¿Qué bibliografía existe en mi área de estudio?
¿Qué avances se han hecho en el estudio de la temática?
¿Cómo se trabajó sobre este tema a lo largo del tiempo?


Tema: Tratamiento del realismo mágico en la literatura latinoamericana actual.
Límites espaciotemporales: Latinoamérica (o autores latinoamericanos), siglo XXI.
Palabras clave: Realismo mágico, literatura siglo XXI, autores latinoamericanos modernos.
Subtemas: recuperación de corrientes literarias, temas del realismo mágico, funciones del realismo mágico.

Ficha Bibliografica
Referencias de los textos: Hazlas según las normativas que exijan tu trabajo (APA, Vancouver, etc.).
Tema: Reseña de qué trata cada texto.
Tesis: Describe brevemente la postura del autor de cada documento recuperado.
Propósito: Sintetiza qué se quiere demostrar en estos textos.
Ideas centrales: Enumera los puntos principales que desarrolla cada autor.
Conceptos claves: Trata de manera breve los conceptos esenciales para los trabajos recolectados.
Conclusiones: Explica cuál es la conclusión a la que llega cada autor con su texto.


Resúmenes para redactar Estados del Arte
Otro elemento para organizar la información que irá en un estado del arte son los resúmenes. Estos pueden tener, por ejemplo, la siguiente estructura:

Un párrafo introductorio, que incluya el título del texto, su autor y año de publicación. Asimismo, debe reseñar el tema general, la tesis y el propósito que se tratan.
El desarrollo de las ideas principales de los documentos. En cada párrafo de tus resúmenes explica cada una de las ideas fundamentales tratadas por los textos.
Una conclusión. Es decir, breve exposición de los resultados más importantes a los que se llega.


Introducción
Aquí se presenta el tema; el objetivo general y la pregunta de investigación del trabajo en el que el estado del arte se enmarca. Sirve, en consecuencia, para guiar al lector acerca de los motivos e interrogantes que guían la redacción de ese estado del arte.

Desarrollo del Estado del Arte
En esta sección es que debe volcarse toda la información recuperada (y debidamente analizada) de la bibliografía. Es necesario que contenga los siguientes puntos:

Una presentación a grandes rasgos de los resultados que obtuviste de la bibliografía de tu estado del arte. Clasifícalos según las temáticas y factores comunes.
Explicación y comparación de tales temáticas y factores en común. Debes citar y dar las referencias adecuadas para cada texto.
Identificación de las conclusiones generales que tengan incidencia para el trabajo.
Estos aspectos de este segmento de tu proyecto no pueden faltar, además de que su correcta estructuración es clave.

Conclusiones
En este punto, debes escribir las conclusiones que es necesario que el lector tenga en cuenta para comprender tu investigación y cómo se relaciona con tu estado del arte. Como ejemplo, puedes reseñar los campos y líneas de investigación del tema de tu investigación que no están explorados. De este modo, indicas qué dirección tomará tu trabajo.
 -->

El espacio de búsqueda es una de las componentes principales de los sistemas
de _AutoML_, independientemente de la naturaleza de los mismo. La gran mayoría
de las herramientas de sector cuentan con una espacio de búsqueda muy definido,
normalmente determinado por el tipo de problema al que dan solución o a las
herramientas de _ML_ subyacente. En dichos casos, usualmente, llaman "description
del espacio de búsqueda" a la caracterización de los hyperparámetros de los
distintos modelos que se incluyen en dicha definición previa

Como se muestra en las investigaciones previas realizadas por [5] casi ninguna
de las herramientas del sector _AutoML_ cuenta con la capacidad real de describir,
en su totalidad y de forma detallada, su espacio de búsqueda. Independientemente
de esto, todo mecanismo y sintaxis que tenga como objetivo la descripción estructural
del campo de investigación, tiene su lugar en el procesos investigativo de la presente
tesis.

#### Marco Teórico

##### _Espacio de Búsqueda_

Subconjunto del universo tal que cada uno de sus elementos son soluciones factibles
para una problema dado.

##### _Descripción del Espacio de Búsqueda_

Proceso mediante el cual, según las características del medio, se define una
jerarquía de estructuras y datos de forma tal que el receptor de dicha descripción  
pueda entender las dimensiones y características del espacio y sea capaz de generar
muestras del mismo.

En el casos específico del sector computacional el medio no suele ser un lenguaje
de programación de uso general, sino que las distintas herramientas de optimización, _ML_
o _AutoML_, suele implementar _DSL's_ o _frameworks_ en los que las descripciones se
pueda acercar un poco más al lenguaje natural.

##### _DSL_ (_Lenguaje de Dominio Específico_,_Domain Specific Language_ )

Según [6] un lenguaje específico de dominio es un lenguaje especializado que sirve
para elevar el nivel de abstracción del software y facilitar el desarrollo del mismo.
Los DSL cuentan con múltiples formas de representación e implementación, desde
micro-modificaciones realizadas a lenguajes subyacentes, hasta proyectos a gran escala.

Para la presente investigación solo son de interés aquellos _DSLs_ que se construyen e
incorporan a un lenguaje subyacente, elevando el nivel de abstracción y la expresividad
del código con respecto a un domino específico.

##### _DSLs_ orientados a descripciones

Los _DSLs_ pertenecientes al domino de la presente investigación tiene como objetivo
la descripción de una serie de conceptos para su posterior explotación. Esto supone que
los mismos cuenten con una ejecución separada en dos fases, que puede recordar a las
tradicionales estabas de los programas (_compilación_ y _ejecución_), pues en un
primer momento los desarrolladores escriben toda una serie de reglas y descripciones
que posteriormente serán utilizadas para la ejecución del propósito final.

Debido al hecho de que estas herramientas, como se señalo anteriormente, representa un
pequeño engranaje en softwares mucho mas grandes, entonces generalmente las dos fases
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

##### Tiempo de compilación del _DSL_

Definimos el tiempo de compilación de un _DSL_ como todas las operaciones puntuales que se
realizan para orquestar la infraestructura que dará soporte a la ejecución del objetivo
final del mismo. Dicha infraestructura debería permanecer inmutable en su mayoría en
durante todos los procesos posteriores a la "compilación" del _DSL_.

##### Tiempo de ejecución del _DSL_

Definimos el tiempo de ejecución del _DSL_ como todas las operaciones que realiza
la herramienta, posteriores a la "compilación" del mismo, para lograr su objetivo básico y
principal.

Véase por ejemplo el proceso de ejecución del módulo _Grammar_ de _AutoGOAL_, el cual es
la componente descriptiva del sistema. En un primer momento se analizan todas las descripciones
aportados para inferir una gramática libre del contexto que describa el espacio de todos los
programas factibles, proceso que se pudiera interpretar como la "compilación del sistema". Y
posteriormente, de forma iterativa, se generan nuevas instancias de dicha gramática para ser
evaluadas y realizar otras operaciones ajenas al componente descriptivo. Si se interpreta que
el objetivo final del modulo _Gramar_ es la generación de soluciones factibles, entonces se
podrían decir que una vez que inicia una ejecución de _AutoGOAL_, luego de la "compilación"
de sus descripciones, su _DSL_ se ejecuta múltiples veces hasta que el sistema encuentra una
respuesta al problema planteado.

##### Python para _DSL_

Como el resultado de la presente tesis es un _DSL_ atado a un lenguaje de propósito general
subyacente. Dicho lenguaje de contar con una serie de características especiales,
que permita a el autor modificar la semántica de su sintaxis original. Y aunque la gran mayoría
de los sistemas de la actualidad que podrían estar interesados en la explotación de la solución
propuesta están escritos en _Python_. La elección de dicho lenguaje como lenguaje subyacente
para la implementación de la propuesta planteada no se encuentra influenciada por dicha
situación, sino que además _Python_ cuenta con potentes y cómoda herramientas para modificar  
la semántica de su sintaxis y desarrollar la metaprogramación.

#### Estado del Arte

En función del marco teórico en que se desarrollo la investigación y teniendo en cuenta
que el estado del arte respecto a la descripción de espacios de búsqueda, en este momento,
se encuentra concentrado en los sistemas _AutoML_ y bibliotecas de optimización, entonces se
realizo una selección y estudio de las herramientas del sector, que contarán con algún
mecanismo para expresar la dimension o estructura de su espacio de búsqueda. Dicha
herramienta debía ser, un mecanismo integrado con el lenguaje de propósito general
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
  especialmente diseñado para el aprendizaje automático. El cual define aporta una
  infraestructura predefinida para segur la evolución de dichos hiperparámetros asi como
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
representas proyectos más grandes que aquellos que son objetos de estudio para esta
investigación en concreto, estudiando las clasificaciones y características que plantea
el autor pudo seleccionar varias que son acordes para describir el estado del arte
de los DSL's que hasta el momento se dan la tarea de describir espacios de búsqueda

A continuación se enumeran y detallan las características con las que se pretende
describir el estado y las propiedades de los trabajos realizados en el área hasta el
momento:

- Estilo de la Sintaxis Concreta: Esta puede ser imperativa o funcional
- Objetivo del Sistema Subyacente: En el caso particular del campo de interés de esta
  investigación la mayoría de las herramientas se encuentra relacionadas con el _ML_ o
  _AutoML_, pero dentro de ambos campos existen múltiples subdominios y razones por las que
  sería de interés describir un dominio determinado
- Activo Objetivo: Nombre con el que se describe el resultado esperado por las transformaciones
  del dsl. En los casos analizados por [6] suelen ser archivos de textos, gráficos o llamadas
  al sistema, pero en esta investigación el autor reinterpreto esta característica, debido a la
  naturales del campo de investigación, pues como todos los trabajos del sector son DSL's
  integrados en un lenguaje de propósito general los activos objetivos pasan a describir a
  los efectos que provoca el empleo del mismo dentro de un programa, las instancias que
  genera o las modificaciones que espera conseguir
- Integración con el Lenguaje Subyacente: Lista de herramientas y características de las
  que se valen los desarrolladores de cada uno de los DSL's para dar lugar a los mismo dentro
  del lenguaje subyacente
- Transformaciones Operativas: Esta parte abarca las características relacionadas con
  la aplicación de una transformación DSL. Se distinguen la técnica, la ejecución,
  la programación y la variabilidad
- Características que Conduce el Diseño: Detrás de las descripciones de los espacios de
  busqueda existe mucho carga teórica de diversas esferas no solo la computación y el _ML_,
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

13 TPOT, http://epistasislab.github.io/tpot/using/#customizing-tpots-operators-and-parameters,
última visita Sept del 2022.
