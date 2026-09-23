 Informe Académico: Cálculo Analítico de Conjuntos de PRIMEROS, SIGUIENTES y PREDICCIÓN

## 1. Definición Formal de la Gramática

Se define la gramática libre de contexto mediante la 4-tupla formal $G = (V_N, V_T, P, S)$, constituida por los siguientes elementos:

* **Conjunto de Símbolos No Terminales ($V_N$):** $\{S, A, B, C, D\}$
* **Conjunto de Símbolos Terminales ($V_T$):** $\{\mathrm{uno}, \mathrm{dos}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$
* **Axioma o Símbolo Inicial:** $S$
* **Delimitador de Fin de Cadena:** $\$$
* **Cadena Vacía:** $\varepsilon$
* **Conjunto de Reglas de Producción ($P$):**
  1. $R_1: S \to A B \mathrm{uno}$
  2. $R_2: A \to \mathrm{dos}\ B$
  3. $R_3: A \to \varepsilon$
  4. $R_4: B \to C\ D$
  5. $R_5: B \to \mathrm{tres}$
  6. $R_6: B \to \varepsilon$
  7. $R_7: C \to \mathrm{cuatro}\ A\ B$
  8. $R_8: C \to \mathrm{cinco}$
  9. $R_9: D \to \mathrm{seis}$
  10. $R_{10}: D \to \varepsilon$

---

## 2. Fundamentación y Deducción Analítica de Conjuntos de PRIMEROS

### 2.1 Criterio Teórico
Para cualquier forma sentencial o símbolo $\alpha \in (V_N \cup V_T)^*$, el conjunto $PRIM(\alpha)$ reúne la totalidad de símbolos terminales con los que puede iniciar una cadena derivada a partir de $\alpha$. Asimismo, si $\alpha$ puede anularse completamente mediante derivaciones sucesivas ($\alpha \Rightarrow^* \varepsilon$), el símbolo de cadena vacía $\varepsilon$ se incorpora al conjunto.

Formalmente se define:
$$PRIM(\alpha) = \{a \in V_T \mid \alpha \Rightarrow^* a\beta\} \cup \{\varepsilon \mid \alpha \Rightarrow^* \varepsilon\}$$

Las reglas sistemáticas aplicadas en la deducción son las siguientes:
1. Si $X$ es un símbolo terminal, su inicio es invariable: $PRIM(X) = \{X\}$.
2. Si existe una producción $X \to \varepsilon$, el elemento $\varepsilon$ se incluye directamente en $PRIM(X)$.
3. Si existe una producción $X \to Y_1 Y_2 \dots Y_k$, se incorporan todos los terminales pertenecientes a $PRIM(Y_1) \setminus \{\varepsilon\}$. Si $Y_1$ es anulable ($\varepsilon \in PRIM(Y_1)$), el análisis avanza hacia $Y_2$, añadiendo $PRIM(Y_2) \setminus \{\varepsilon\}$, y así sucesivamente.
4. Solo en el caso en que todos los componentes $Y_1, \dots, Y_k$ sean simultáneamente anulables, se concluye que $\varepsilon \in PRIM(X)$.

### 2.2 Deducción Analítica Paso a Paso
El cómputo se realiza de manera ascendente, analizando inicialmente los no terminales cuyas reglas presentan menor dependencia indirecta:

#### Análisis para el No Terminal $D$
* **Regla 9 ($D \to \mathrm{seis}$):** La producción inicia directamente con el símbolo terminal $\mathrm{seis}$. Por consiguiente, se añade $\mathrm{seis}$ a $PRIM(D)$.
* **Regla 10 ($D \to \varepsilon$):** La producción genera de forma explícita la cadena vacía, por lo que se incorpora $\varepsilon$ a $PRIM(D)$.
* **Resultado:**
  $$PRIM(D) = \{\mathrm{seis}, \varepsilon\}$$

#### Análisis para el No Terminal $C$
* **Regla 7 ($C \to \mathrm{cuatro}\ A\ B$):** La derivación comienza de forma determinista con el símbolo terminal $\mathrm{cuatro}$. Se incorpora $\mathrm{cuatro}$ a $PRIM(C)$.
* **Regla 8 ($C \to \mathrm{cinco}$):** La regla inicia con el terminal $\mathrm{cinco}$. Se incorpora $\mathrm{cinco}$ a $PRIM(C)$.
* Dado que ninguna de las producciones asociadas a $C$ deriva en la cadena vacía, se verifica que $C$ no es anulable ($C \not\Rightarrow^* \varepsilon$).
* **Resultado:**
  $$PRIM(C) = \{\mathrm{cuatro}, \mathrm{cinco}\}$$

#### Análisis para el No Terminal $B$
* **Regla 5 ($B \to \mathrm{tres}$):** Comienza con el terminal $\mathrm{tres}$, aportando este elemento al conjunto.
* **Regla 6 ($B \to \varepsilon$):** Produce directamente la cadena vacía, incorporando $\varepsilon$ a $PRIM(B)$.
* **Regla 4 ($B \to C\ D$):** Se examina la secuencia $C\ D$. El primer símbolo es el no terminal $C$, cuyos primeros son $\{\mathrm{cuatro}, \mathrm{cinco}\}$. Dado que se demostró previamente que $\varepsilon \notin PRIM(C)$, la propagación se detiene de forma estricta en $C$, sin necesidad de inspeccionar el no terminal $D$.
* **Resultado:**
  $$PRIM(B) = \{\mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \varepsilon\}$$

#### Análisis para el No Terminal $A$
* **Regla 2 ($A \to \mathrm{dos}\ B$):** La producción inicia con el símbolo terminal $\mathrm{dos}$, incluyéndose de forma directa.
* **Regla 3 ($A \to \varepsilon$):** Genera la cadena vacía de forma directa, aportando $\varepsilon$ al conjunto.
* **Resultado:**
  $$PRIM(A) = \{\mathrm{dos}, \varepsilon\}$$

#### Análisis para el Símbolo Inicial $S$
* **Regla 1 ($S \to A B \mathrm{uno}$):**
  1. Se evalúa el primer elemento de la secuencia, correspondiente al no terminal $A$. Se incorporan todos los terminales de $PRIM(A)$, lo cual añade $\{\mathrm{dos}\}$.
  2. Debido a que $A$ es anulable ($\varepsilon \in PRIM(A)$), la producción puede prescindir de $A$ e iniciar con el siguiente símbolo, $B$. Se incorporan los elementos terminales de $PRIM(B)$, aportando $\{\mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$.
  3. Puesto que $B$ también es anulable ($\varepsilon \in PRIM(B)$), existe la posibilidad de que tanto $A$ como $B$ deriven simultáneamente en $\varepsilon$. Por ende, la búsqueda avanza hacia el tercer símbolo de la secuencia, $\mathrm{uno}$. Al tratarse de un terminal, se agrega $\{\mathrm{uno}\}$ y la exploración finaliza.
  4. Dado que la producción concluye con un elemento no anulable, se constata que $\varepsilon \notin PRIM(S)$.
* **Resultado:**
  $$PRIM(S) = \{\mathrm{dos}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{uno}\}$$

### 2.3 Resumen Consolidado de PRIMEROS

| Símbolo No Terminal | Conjunto de PRIMEROS |
| :---: | :--- |
| $S$ | $\{\mathrm{uno}, \mathrm{dos}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$ |
| $A$ | $\{\mathrm{dos}, \varepsilon\}$ |
| $B$ | $\{\mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \varepsilon\}$ |
| $C$ | $\{\mathrm{cuatro}, \mathrm{cinco}\}$ |
| $D$ | $\{\mathrm{seis}, \varepsilon\}$ |

---

## 3. Fundamentación y Deducción Analítica de Conjuntos de SIGUIENTES

### 3.1 Criterio Teórico
Para un símbolo no terminal $X \in V_N$, el conjunto $SIG(X)$ agrupa todos los símbolos terminales que pueden aparecer situados inmediatamente a la derecha de $X$ en alguna forma sentencial derivable a partir del símbolo inicial $S$.

Formalmente se define:
$$SIG(X) = \{a \in V_T \mid S \Rightarrow^* \alpha X a \beta\} \cup \{\$ \mid S \Rightarrow^* \alpha X\}$$

Las reglas sistemáticas aplicadas en la deducción son:
1. **Condición de frontera:** El marcador de fin de cadena pertenece obligatoriamente al símbolo inicial: $\$ \in SIG(S)$.
2. **Propagación por adyacencia derecha:** Si existe una producción de la forma $A \to \alpha B \beta$, todos los terminales pertenecientes a $PRIM(\beta) \setminus \{\varepsilon\}$ forman parte de $SIG(B)$.
3. **Propagación por posición final o anulabilidad:** Si existe una producción $A \to \alpha B$, o bien $A \to \alpha B \beta$ donde el sufijo es anulable ($\beta \Rightarrow^* \varepsilon$), la totalidad de elementos contenidos en $SIG(A)$ debe heredarse en $SIG(B)$ (es decir, $SIG(A) \subseteq SIG(B)$).
4. **Propiedad de exclusión:** La cadena vacía $\varepsilon$ nunca forma parte de un conjunto de SIGUIENTES.

### 3.2 Deducción Analítica Paso a Paso
Se efectúa un rastreo exhaustivo de cada aparición de los no terminales en los cuerpos de producción (lados derechos de las reglas):

#### Análisis para el Símbolo Inicial $S$
* Por definición formal, se incorpora el fin de entrada: $\$ \in SIG(S)$.
* Al revisar el cuerpo de las diez reglas de producción, se observa que $S$ no interviene en el lado derecho de ninguna producción.
* **Resultado:**
  $$SIG(S) = \{\$\}$$

#### Análisis para el No Terminal $A$
* En la producción $R_1: S \to A B \mathrm{uno}$, a la derecha de $A$ se encuentra la subcadena $B\ \mathrm{uno}$.
  * Se calcula $PRIM(B\ \mathrm{uno}) = (PRIM(B) \setminus \{\varepsilon\}) \cup \{\mathrm{uno}\} = \{\mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{uno}\}$.
  * Por consiguiente, se transfieren dichos elementos: $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\} \subseteq SIG(A)$.
* En la producción $R_7: C \to \mathrm{cuatro}\ A\ B$, a la derecha de $A$ se localiza el no terminal $B$.
  * Se añaden los elementos terminales de $PRIM(B)$, es decir, $\{\mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$.
  * Debido a que $B \Rightarrow^* \varepsilon$, el símbolo $A$ puede pasar a ocupar de facto la posición terminal del cuerpo, originando la inclusión:
    $$SIG(C) \subseteq SIG(A)$$

#### Análisis para el No Terminal $B$
* En la producción $R_1: S \to A B \mathrm{uno}$, a la derecha de $B$ se encuentra el terminal $\mathrm{uno}$. Se incorpora $\{\mathrm{uno}\} \subseteq SIG(B)$.
* En la producción $R_2: A \to \mathrm{dos}\ B$, el símbolo $B$ se sitúa en el extremo final de la regla. Se genera la relación de herencia:
  $$SIG(A) \subseteq SIG(B)$$
* En la producción $R_7: C \to \mathrm{cuatro}\ A\ B$, el símbolo $B$ ocupa igualmente la posición final del cuerpo, estableciendo:
  $$SIG(C) \subseteq SIG(B)$$

#### Análisis para el No Terminal $C$
* En la producción $R_4: B \to C\ D$, a la derecha de $C$ se ubica el símbolo $D$.
  * Se incorporan los terminales de $PRIM(D)$, aportando $\{\mathrm{seis}\} \subseteq SIG(C)$.
  * Debido a que $D$ es anulable ($D \Rightarrow^* \varepsilon$), la regla puede culminar en $C$, transfiriendo los siguientes de la cabecera:
    $$SIG(B) \subseteq SIG(C)$$

#### Análisis para el No Terminal $D$
* En la producción $R_4: B \to C\ D$, el no terminal $D$ se sitúa en la posición final absoluta de la regla, originando:
  $$SIG(B) \subseteq SIG(D)$$

### 3.3 Resolución del Sistema de Ecuaciones de Inclusión
Al reunir las relaciones deducidas para los no terminales $A$, $B$ y $C$, se identifica una dependencia cíclica cerrada:
$$SIG(A) \subseteq SIG(B) \subseteq SIG(C) \subseteq SIG(A)$$

De acuerdo con la teoría de relaciones y análisis de puntos fijos, la reciprocidad de inclusiones demuestra la igualdad matemática estricta entre los tres conjuntos:
$$SIG(A) = SIG(B) = SIG(C)$$

Se efectúa la consolidación de todos los terminales aportados de forma directa:
* Aportes directos hacia $A$: $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$
* Aporte directo hacia $B$: $\{\mathrm{uno}\}$
* Aporte directo hacia $C$: $\{\mathrm{seis}\}$

La unión exhaustiva de estos componentes determina:
$$SIG(A) = SIG(B) = SIG(C) = \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$$

Finalmente, al evaluar la relación correspondiente a $D$:
$$SIG(D) = SIG(B) = \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$$

### 3.4 Resumen Consolidado de SIGUIENTES

| Símbolo No Terminal | Conjunto de SIGUIENTES |
| :---: | :--- |
| $S$ | $\{\text{\$}\}$ |
| $A$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |
| $B$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |
| $C$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |
| $D$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |

---

## 4. Fundamentación y Deducción Analítica de Conjuntos de PREDICCIÓN

### 4.1 Criterio Teórico
El conjunto de predicción se asocia de forma unívoca a cada regla de producción individual $R_i: X \to \alpha$. Dicho conjunto establece los símbolos de la cadena de entrada mediante los cuales un analizador sintáctico predictivo descendente determina la aplicación de dicha regla sin incurrir en ambigüedad.

La formulación canónica establece:
$$PRED(X \to \alpha) = \begin{cases} 
PRIM(\alpha), & \text{si } \varepsilon \notin PRIM(\alpha) \\ 
(PRIM(\alpha) \setminus \{\varepsilon\}) \cup SIG(X), & \text{si } \varepsilon \in PRIM(\alpha) 
\end{cases}$$

### 4.2 Deducción Analítica por Regla de Producción

* **Regla 1: $S \to A B \mathrm{uno}$**
  * Se evalúa la anulabilidad del cuerpo: la presencia del terminal $\mathrm{uno}$ al final de la secuencia impide que el cuerpo derive en la cadena vacía ($\varepsilon \notin PRIM(A B \mathrm{uno})$).
  * En consecuencia, se aplica el caso directo: $PRED(R_1) = PRIM(A B \mathrm{uno})$.
  * **$PRED(R_1) = \{\mathrm{uno}, \mathrm{dos}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$**

* **Regla 2: $A \to \mathrm{dos}\ B$**
  * El cuerpo inicia con el terminal $\mathrm{dos}$, por lo cual $\varepsilon \notin PRIM(\mathrm{dos}\ B)$.
  * Por consiguiente: $PRED(R_2) = PRIM(\mathrm{dos}\ B) = \{\mathrm{dos}\}$.
  * **$PRED(R_2) = \{\mathrm{dos}\}$**

* **Regla 3: $A \to \varepsilon$**
  * El cuerpo es nulo de forma trivial ($\varepsilon \in PRIM(\varepsilon)$).
  * Por formulación de regla anulable: $PRED(R_3) = SIG(A)$.
  * **$PRED(R_3) = \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$**

* **Regla 4: $B \to C\ D$**
  * El cuerpo inicia con el no terminal $C$, el cual no es anulable ($PRIM(C) = \{\mathrm{cuatro}, \mathrm{cinco}\}$). Por tanto, $\varepsilon \notin PRIM(C\ D)$.
  * Por consiguiente: $PRED(R_4) = PRIM(C) = \{\mathrm{cuatro}, \mathrm{cinco}\}$.
  * **$PRED(R_4) = \{\mathrm{cuatro}, \mathrm{cinco}\}$**

* **Regla 5: $B \to \mathrm{tres}$**
  * El cuerpo inicia con el terminal $\mathrm{tres}$, impidiendo la anulación.
  * Por consiguiente: $PRED(R_5) = \{\mathrm{tres}\}$.
  * **$PRED(R_5) = \{\mathrm{tres}\}$**

* **Regla 6: $B \to \varepsilon$**
  * La producción deriva directamente en la cadena vacía ($\varepsilon \in PRIM(\varepsilon)$).
  * En consecuencia: $PRED(R_6) = SIG(B)$.
  * **$PRED(R_6) = \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$**

* **Regla 7: $C \to \mathrm{cuatro}\ A\ B$**
  * Inicia con el símbolo terminal $\mathrm{cuatro}$, por lo cual $\varepsilon \notin PRIM(\mathrm{cuatro}\ A\ B)$.
  * Por consiguiente: $PRED(R_7) = \{\mathrm{cuatro}\}$.
  * **$PRED(R_7) = \{\mathrm{cuatro}\}$**

* **Regla 8: $C \to \mathrm{cinco}$**
  * Inicia con el símbolo terminal $\mathrm{cinco}$, por lo cual $\varepsilon \notin PRIM(\mathrm{cinco})$.
  * Por consiguiente: $PRED(R_8) = \{\mathrm{cinco}\}$.
  * **$PRED(R_8) = \{\mathrm{cinco}\}$**

* **Regla 9: $D \to \mathrm{seis}$**
  * Inicia con el terminal $\mathrm{seis}$, por lo cual $\varepsilon \notin PRIM(\mathrm{seis})$.
  * Por consiguiente: $PRED(R_9) = \{\mathrm{seis}\}$.
  * **$PRED(R_9) = \{\mathrm{seis}\}$**

* **Regla 10: $D \to \varepsilon$**
  * La producción es nula ($\varepsilon \in PRIM(\varepsilon)$).
  * En consecuencia: $PRED(R_{10}) = SIG(D)$.
  * **$PRED(R_{10}) = \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$**

### 4.3 Tabla Consolidada de Conjuntos de PREDICCIÓN

| ID | Regla de Producción | Condición de Anulabilidad | Conjunto de PREDICCIÓN |
| :---: | :--- | :---: | :--- |
| $R_1$ | $S \to A B \mathrm{uno}$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{uno}, \mathrm{dos}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}\}$ |
| $R_2$ | $A \to \mathrm{dos}\ B$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{dos}\}$ |
| $R_3$ | $A \to \varepsilon$ | $\varepsilon \in PRIM(\mathrm{cuerpo})$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |
| $R_4$ | $B \to C\ D$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{cuatro}, \mathrm{cinco}\}$ |
| $R_5$ | $B \to \mathrm{tres}$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{tres}\}$ |
| $R_6$ | $B \to \varepsilon$ | $\varepsilon \in PRIM(\mathrm{cuerpo})$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |
| $R_7$ | $C \to \mathrm{cuatro}\ A\ B$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{cuatro}\}$ |
| $R_8$ | $C \to \mathrm{cinco}$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{cinco}\}$ |
| $R_9$ | $D \to \mathrm{seis}$ | $\varepsilon \notin PRIM(\mathrm{cuerpo})$ | $\{\mathrm{seis}\}$ |
| $R_{10}$ | $D \to \varepsilon$ | $\varepsilon \in PRIM(\mathrm{cuerpo})$ | $\{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\}$ |

---

## 5. Evaluación de la Condición LL(1)

Una gramática es determinista y clasificable como $LL(1)$ si y solo si, para cada par de producciones que compartan el mismo no terminal en su parte izquierda ($X \to \alpha$ y $X \to \beta$, con $\alpha \neq \beta$), sus respectivos conjuntos de predicción resultan disyuntos:

$$PRED(X \to \alpha) \cap PRED(X \to \beta) = \emptyset$$

Se realiza la verificación para cada variable del conjunto $V_N$:

1. **No Terminal $A$:**
   $$PRED(R_2) \cap PRED(R_3) = \{\mathrm{dos}\} \cap \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\} = \emptyset$$
   *(Condición satisfecha).*

2. **No Terminal $C$:**
   $$PRED(R_7) \cap PRED(R_8) = \{\mathrm{cuatro}\} \cap \{\mathrm{cinco}\} = \emptyset$$
   *(Condición satisfecha).*

3. **No Terminal $D$:**
   $$PRED(R_9) \cap PRED(R_{10}) = \{\mathrm{seis}\} \cap \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\} = \{\mathrm{seis}\} \neq \emptyset$$
   *(Se presenta conflicto de selección sobre el símbolo $\mathrm{seis}$).*

4. **No Terminal $B$:**
   $$PRED(R_4) \cap PRED(R_5) = \{\mathrm{cuatro}, \mathrm{cinco}\} \cap \{\mathrm{tres}\} = \emptyset$$
   $$PRED(R_4) \cap PRED(R_6) = \{\mathrm{cuatro}, \mathrm{cinco}\} \cap \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\} = \{\mathrm{cuatro}, \mathrm{cinco}\} \neq \emptyset$$
   $$PRED(R_5) \cap PRED(R_6) = \{\mathrm{tres}\} \cap \{\mathrm{uno}, \mathrm{tres}, \mathrm{cuatro}, \mathrm{cinco}, \mathrm{seis}\} = \{\mathrm{tres}\} \neq \emptyset$$
   *(Se presentan colisiones deterministas sobre los símbolos $\mathrm{tres}$, $\mathrm{cuatro}$ y $\mathrm{cinco}$).*

### Conclusión Formal
Dado que existen intersecciones no vacías en los conjuntos de predicción asociados a los no terminales $B$ y $D$, se dictamina formalmente que la gramática examinada **no es de tipo $LL(1)$**.
