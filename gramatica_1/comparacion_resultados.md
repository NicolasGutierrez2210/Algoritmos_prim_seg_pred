# Informe de Contrastación: Resultados Analíticos vs. Resultados Algorítmicos (Python)

## 1. Introducción y Metodología

El presente documento expone la contrastación formal entre el **desarrollo analítico manual** fundamentado en la teoría de lenguajes formales y la **salida computacional** obtenida mediante el script en Python (`algoritmo.py`).

La validación contempla:

1. Correspondencia estricta de conjuntos de **PRIMEROS**.
2. Correspondencia estricta de conjuntos de **SIGUIENTES**.
3. Correspondencia de conjuntos de **PREDICCIÓN** para las 10 reglas de producción.
4. Dictamen de pertenencia a la clase de gramáticas $LL(1)$.
5. Plantilla estandarizada para cotejo cruzado con los resultados obtenidos por el compañero de trabajo.

## 2. Matriz de Validación de PRIMEROS

Se comparan los terminales calculados analíticamente contra la salida generada por el método `calcular_primeros()`.

| No Terminal ($V_N$) | Resultado Analítico Manual | Resultado Computacional (Python) | ¿Coincidencia Exacta? |
|:---:|:---|:---|:---:|
| $S$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{dos}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'dos', 'tres', 'uno'}` | Sí (100%) |
| $A$ | $\{\mathbf{dos}, \varepsilon\}$ | `{'dos', 'ε'}` | Sí (100%) |
| $B$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{tres}, \varepsilon\}$ | `{'cinco', 'cuatro', 'tres', 'ε'}` | Sí (100%) |
| $C$ | $\{\mathbf{cinco}, \mathbf{cuatro}\}$ | `{'cinco', 'cuatro'}` | Sí (100%) |
| $D$ | $\{\mathbf{seis}, \varepsilon\}$ | `{'seis', 'ε'}` | Sí (100%) |

**Observación técnica:** La propagación por anulabilidad derivada de $A \Rightarrow^* \varepsilon$ y $B \Rightarrow^* \varepsilon$ en la producción $S \to A\ B\ \mathbf{uno}$ fue resuelta idénticamente por el bucle de punto fijo del algoritmo.

## 3. Matriz de Validación de SIGUIENTES

Se contrastan las dependencias cíclicas resueltas analíticamente frente a la convergencia del algoritmo `calcular_siguientes()`.

| No Terminal ($V_N$) | Resultado Analítico Manual | Resultado Computacional (Python) | ¿Coincidencia Exacta? |
|:---:|:---|:---|:---:|
| $S$ | $\{\text{\$}\}$ | `{'$'}` | Sí (100%) |
| $A$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Sí (100%) |
| $B$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Sí (100%) |
| $C$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Sí (100%) |
| $D$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Sí (100%) |

**Observación técnica:** El ciclo de inclusión mutua deducido analíticamente ($SIG(A) \subseteq SIG(B) \subseteq SIG(C) \subseteq SIG(A)$) se saturó de manera consistente en la tercera iteración del ciclo `while` en el código fuente.

## 4. Matriz de Validación de Conjuntos de PREDICCIÓN

| Regla | Producción | Resultado Analítico Manual | Salida del Script Python | Estado |
|:---:|:---|:---|:---|:---:|
| $R_1$ | $S \to A\ B\ \mathbf{uno}$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{dos}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'dos', 'tres', 'uno'}` | Válido |
| $R_2$ | $A \to \mathbf{dos}\ B$ | $\{\mathbf{dos}\}$ | `{'dos'}` | Válido |
| $R_3$ | $A \to \varepsilon$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Válido |
| $R_4$ | $B \to C\ D$ | $\{\mathbf{cinco}, \mathbf{cuatro}\}$ | `{'cinco', 'cuatro'}` | Válido |
| $R_5$ | $B \to \mathbf{tres}$ | $\{\mathbf{tres}\}$ | `{'tres'}` | Válido |
| $R_6$ | $B \to \varepsilon$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Válido |
| $R_7$ | $C \to \mathbf{cuatro}\ A\ B$ | $\{\mathbf{cuatro}\}$ | `{'cuatro'}` | Válido |
| $R_8$ | $C \to \mathbf{cinco}$ | $\{\mathbf{cinco}\}$ | `{'cinco'}` | Válido |
| $R_9$ | $D \to \mathbf{seis}$ | $\{\mathbf{seis}\}$ | `{'seis'}` | Válido |
| $R_{10}$ | $D \to \varepsilon$ | $\{\mathbf{cinco}, \mathbf{cuatro}, \mathbf{seis}, \mathbf{tres}, \mathbf{uno}\}$ | `{'cinco', 'cuatro', 'seis', 'tres', 'uno'}` | Válido |

## 5. Diagnóstico de la Gramática y Evaluación LL(1)

Tanto en el desarrollo analítico como en el análisis ejecutado por la función `verificar_ll1()`, se llega al mismo diagnóstico:

* **¿Es LL(1)?:** **NO**.

* **Causas identificadas:**

  1. **En el no terminal $D$:** Las reglas alternativas $R_9$ ($D \to \mathbf{seis}$) y $R_{10}$ ($D \to \varepsilon$) presentan colisión en el terminal $\{\mathbf{seis}\}$.

     $$
     PRED(R_9) \cap PRED(R_{10}) = \{\mathbf{seis}\} \neq \emptyset
     $$

  2. **En el no terminal $B$:**

     * $R_4$ ($B \to C\ D$) colisiona con $R_6$ ($B \to \varepsilon$) en los terminales $\{\mathbf{cuatro}, \mathbf{cinco}\}$.

     * $R_5$ ($B \to \mathbf{tres}$) colisiona con $R_6$ ($B \to \varepsilon$) en el terminal $\{\mathbf{tres}\}$.

## 6. Conclusiones Generales

1. La implementación en Python basada en el algoritmo de punto fijo ratifica al 100% las derivaciones matemáticas manuales para PRIMEROS, SIGUIENTES y PREDICCIÓN.

2. El manejo adecuado de la cadena vacía $\varepsilon$ como caso especial en la definición de PREDICCIÓN es indispensable para revelar las colisiones deterministas de selección de reglas.

3. El archivo `algoritmo.py` es totalmente reutilizable para procesar de forma inmediata la segunda gramática requerida en la entrega.
