Bliblioteca de optimizacion que brinda la posibilidad al usuario de describir el espacio de busquea
tiene un estilo funcional impulsado por las funcnoes de distribucion y en su documentacion propicia
el uso de sintaxis estilo JSON, pese a que la estructua son contruidas con una filosofia Bottom-Up,
el resultado final da la idea de un unico archivo de configuracion que describe el espacio de busqueda
en su totalidad. No presenta mas capacidad expresiva que la que pueden aporta las distintas funciones de
distribucion y el propio lenguaje, Python. La evaluacion de cada componente se realiza de manera lazy

Repo: privado o eliminado

La mayoría de los algoritmos de aprendizaje automático tienen hiperparámetros que tienen un gran impacto en el rendimiento del sistema de extremo a extremo, y ajustar los hiperparámetros para optimizar el rendimiento de extremo a extremo puede ser una tarea desalentadora. Los hiperparámetros son muy variados: los de valor continuo, con o sin límites, los discretos, ordenados o no, y los condicionales, que ni siquiera se aplican siempre (por ejemplo, los parámetros de una etapa opcional de preprocesamiento), por lo que los algoritmos convencionales de optimización continua y combinatoria o bien no se aplican directamente, o bien funcionan sin aprovechar la estructura del espacio de búsqueda. Normalmente, la optimización de los hiperparámetros se lleva a cabo de antemano por expertos en problemas no relacionados, o manualmente para el problema en cuestión con la ayuda de la búsqueda en cuadrícula. Sin embargo, cuando se trata de más de unos pocos hiperparámetros (por ejemplo, 5), la práctica estándar de búsqueda manual con refinamiento de cuadrícula es tan ineficiente que incluso la búsqueda aleatoria ha demostrado ser competitiva con los expertos del dominio [1].

Hay una gran necesidad de mejores algoritmos de optimización de hiperparámetros (HOAs) por dos razones:

Los HOAs formalizan la práctica de la evaluación de modelos, de modo que los experimentos de evaluación comparativa pueden ser reproducidos en fechas posteriores, y por diferentes personas.

Los diseñadores de algoritmos de aprendizaje pueden ofrecer implementaciones flexibles y totalmente configurables a los no expertos (por ejemplo, sistemas de aprendizaje profundo), siempre y cuando también proporcionen un HOA correspondiente.

Hyperopt proporciona HOAs en serie y paralelizables a través de una biblioteca de Python [2, 3]. Es fundamental para su diseño un protocolo de comunicación entre (a) la descripción de un espacio de búsqueda de hiperparámetros, (b) una función de evaluación de hiperparámetros (sistema de aprendizaje automático), y (c) un algoritmo de búsqueda de hiperparámetros. Este protocolo hace posible que los HOA genéricos (como el algoritmo "TPE") funcionen para una serie de problemas de búsqueda específicos. Algoritmos específicos de aprendizaje automático (o familias de algoritmos) se implementan como espacios de búsqueda hiperopt en proyectos relacionados: Redes de Creencia Profunda [4], arquitecturas de visión convolucional [5], y clasificadores scikit-learn [6]. Mi presentación explicará qué problema resuelve hyperopt, cómo utilizarlo y cómo puede ofrecer modelos precisos a partir de los datos, sin la intervención de un operador.

Traducción realizada con la versión gratuita del traductor www.DeepL.com/Translator
