# Taller de análisis sintáctico: algoritmos de primeros, siguientes y predicción

## 1. Propósito general

Este repositorio contiene la solución conceptual y computacional para el cálculo de los conjuntos fundamentales del análisis sintáctico descendente: primeros, siguientes y predicción. El objetivo es contrastar el desarrollo analítico formal con algoritmos de punto fijo implementados en Python, evaluando además si las gramáticas estudiadas cumplen con las condiciones de determinismo para ser clasificadas como LL(1).

---

## 2. Contenido del repositorio

El repositorio se divide en dos carpetas según la gramática trabajada:

- **`gramatica_1/`**: Contiene el cálculo analítico paso a paso, el script en Python y el informe comparativo para la primera gramática del taller, enfocada en la propagación de símbolos iniciales y el tratamiento de producciones vacías.
- **`gramatica_2/`**: Contiene el cálculo analítico, la implementación en Python y la documentación técnica para la segunda gramática, la cual presenta recursión izquierda directa y dependencias complejas de anulabilidad, evidenciando los conflictos que impiden el análisis predictivo sin transformaciones previas.
