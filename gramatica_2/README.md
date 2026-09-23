# Taller: Análisis sintáctico descendente y conjuntos de predicción


## 1. Por qué calculamos esto?

En compiladores y procesamiento de lenguajes, un analizador sintáctico descendente predictivo (como un parser LL(1)) tiene un objetivo muy puntual: **leer el código fuente token por token y decidir qué regla gramatical aplicar sin titubear y sin tener que devolverse (sin backtracking)**.

Podemos pensar en el parser como un clasificador determinista en tiempo real:
- Ve un símbolo no terminal en su pila (por ejemplo, $A$).
- Observa el siguiente token de entrada (llamado *lookahead*).
- Con solo esa información, debe escoger con total certeza cuál de las reglas de $A$ debe dispararse.

Para construir la tabla de decisiones de este clasificador, necesitamos tres herramientas matemáticas fundamentales:
1. **PRIMEROS:** Responde a la pregunta: *si expando esta variable o regla, ¿con qué tokens reales puede arrancar el texto?*
2. **SIGUIENTES:** Responde a la pregunta: *si esta variable se reduce, termina su trabajo o simplemente se borra (deriva en vacía), ¿qué tokens pueden aparecer inmediatamente a su derecha en el código?*
3. **PREDICCIÓN:** Es la combinación de las dos anteriores. Determina el conjunto exacto de tokens que deben hacer que el parser elija una producción específica.

Si para un mismo no terminal dos reglas distintas reaccionan al mismo token (sus conjuntos de predicción se cruzan), el parser sufrirá un conflicto de ambigüedad y no podrá ser LL(1).

---

## 2. La gramática del taller

Trabajamos sobre la siguiente gramática formal:

- **Símbolos No Terminales:** $V_N = \{S, A, B, C, D\}$
- **Símbolos Terminales:** $V_T = \{\text{uno}, \text{dos}, \text{tres}, \text{cuatro}, \text{cinco}, \text{seis}\}$
- **Símbolo Inicial:** $S$
- **Fin de entrada:** $\$$
- **Cadena vacía:** $\varepsilon$

### Reglas de producción numeradas:
1. $S \to A \text{ uno } B C$
2. $S \to S \text{ dos}$
3. $A \to B C D$
4. $A \to A \text{ tres}$
5. $A \to \varepsilon$
6. $B \to D \text{ cuatro } C \text{ tres}$
7. $B \to \varepsilon$
8. $C \to \text{cinco } D B$
9. $C \to \varepsilon$
10. $D \to \text{seis}$
11. $D \to \varepsilon$

---

## 3. Primer paso: Identificación de símbolos anulables (Nullability)

Un no terminal se considera **anulable** si tiene la capacidad de evaporarse por completo, es decir, de derivar en la cadena vacía $\varepsilon$ ($X \Rightarrow^* \varepsilon$). 

Saber quién es anulable es el primer paso obligatorio, porque cuando una variable en una secuencia puede desaparecer, el token inicial ya no lo dictará ella, sino la variable que esté parada inmediatamente a su derecha.

Analizando las reglas:
- **$D$:** Tiene la regla directa $D \to \varepsilon$. Por tanto, **$D$ es anulable**.
- **$C$:** Tiene la regla directa $C \to \varepsilon$. Por tanto, **$C$ es anulable**.
- **$B$:** Tiene la regla directa $B \to \varepsilon$. Por tanto, **$B$ es anulable**.
- **$A$:** Tiene la regla directa $A \to \varepsilon$. Además, la regla $A \to B C D$ está compuesta por tres variables donde todas son anulables ($B, C, D \Rightarrow^* \varepsilon$). Por tanto, **$A$ es anulable**.
- **$S$:** La regla 1 ($S \to A \text{ uno } B C$) tiene en medio al terminal obligatorio `uno`, el cual nunca puede borrarse. La regla 2 ($S \to S \text{ dos}$) tiene al terminal `dos`. Por ende, ninguna combinación permite que $S$ se transforme en vacío. **$S$ NO es anulable**.

**Resumen:**
$$\text{Anulables} = \{A, B, C, D\}$$
$$\text{No Anulables} = \{S\}$$

---

## 4. Segundo paso: Cálculo analítico de PRIMEROS

La regla lógica para calcular $\text{PRIMEROS}(X)$ sigue el principio de propagación en cadena (efecto dominó):
- Si el cuerpo arranca con un terminal, ese terminal entra directo.
- Si arranca con un no terminal $Y$, hereda todos los terminales de $\text{PRIMEROS}(Y)$.
- Si ese $Y$ es anulable, no nos podemos detener ahí: la puerta queda abierta y tenemos que mirar también a los $\text{PRIMEROS}$ del siguiente símbolo en la lista, y así sucesivamente hasta toparnos con alguien que no sea anulable.
- Si toda la fila de símbolos es anulable, $\varepsilon$ se agrega al conjunto de $\text{PRIMEROS}$.

Deducción variable por variable:

### Para $D$:
- Regla 10: $D \to \text{seis} \implies$ aporta el terminal `seis`.
- Regla 11: $D \to \varepsilon \implies$ aporta $\varepsilon$.
$$\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$$

### Para $C$:
- Regla 8: $C \to \text{cinco } D B \implies$ arranca con el terminal `cinco`, así que aporta `cinco`.
- Regla 9: $C \to \varepsilon \implies$ aporta $\varepsilon$.
$$\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}$$

### Para $B$:
- Regla 6: $B \to D \text{ cuatro } C \text{ tres}$.
  - El primer elemento es $D$, por lo que heredamos los terminales de $D$: `seis`.
  - Como $D$ es anulable, el flujo continúa hacia el siguiente símbolo: el terminal `cuatro`. Se incluye `cuatro`.
  - Como `cuatro` es un terminal rígido (no se anula), la propagación se frena aquí.
- Regla 7: $B \to \varepsilon \implies$ aporta $\varepsilon$.
$$\text{PRIMEROS}(B) = \{\text{cuatro}, \text{seis}, \varepsilon\}$$

### Para $A$:
- Regla 3: $A \to B C D$.
  - Empieza con $B$: aporta $\text{PRIMEROS}(B) \setminus \{\varepsilon\} = \{\text{cuatro}, \text{seis}\}$.
  - Como $B$ es anulable, pasa a $C$: aporta $\text{PRIMEROS}(C) \setminus \{\varepsilon\} = \{\text{cinco}\}$.
  - Como $C$ es anulable, pasa a $D$: aporta $\text{PRIMEROS}(D) \setminus \{\varepsilon\} = \{\text{seis}\}$ (ya presente).
  - Como todos ($B, C, D$) son anulables a la vez, toda la producción puede desaparecer: aporta $\varepsilon$.
- Regla 4: $A \to A \text{ tres}$.
  - Como sabemos que $A$ puede derivar en vacío ($A \Rightarrow^* \varepsilon$), podemos hacer la sustitución mental: $A \Rightarrow A \text{ tres} \Rightarrow \varepsilon \text{ tres} = \text{tres}$. Esto significa que una cadena derivada de $A$ puede comenzar legítimamente por el terminal `tres`. Por tanto, se añade `tres`.
- Regla 5: $A \to \varepsilon \implies$ aporta $\varepsilon$.
$$\text{PRIMEROS}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$$

### Para $S$:
- Regla 1: $S \to A \text{ uno } B C$.
  - Arranca con $A$: aporta todos los terminales de $A$, es decir: $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$.
  - Como $A$ es anulable, pasamos al siguiente símbolo: el terminal `uno`. Se añade `uno`.
  - `uno` no se anula, por lo que aquí termina la propagación. Como la producción contiene a `uno`, no deriva en $\varepsilon$.
- Regla 2: $S \to S \text{ dos}$.
  - Contiene a $\text{PRIMEROS}(S)$, sin añadir nuevos símbolos.
$$\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$$

---

## 5. Paso 2: Cálculo analítico de SIGUIENTES

El conjunto $\text{SIGUIENTES}(X)$ no describe lo que $X$ produce por dentro, sino **quién puede aparecer pegado a su derecha en cualquier parte de una derivación válida**.

Reglas clave para deducirlo:
1. El símbolo inicial siempre lleva el fin de archivo: $\$ \in \text{SIGUIENTES}(S)$.
2. En cualquier lado derecho donde aparezca $X$, miramos al vecino que tiene a su derecha ($\beta$):
   - Todo lo que pueda comenzar $\beta$ ($\text{PRIMEROS}(\beta) \setminus \{\varepsilon\}$) formará parte de $\text{SIGUIENTES}(X)$.
   - Si ese vecino $\beta$ no existe (porque $X$ está al puro final de la regla), o si $\beta$ es anulable (puede desvanecerse), entonces **$X$ hereda todo el conjunto $\text{SIGUIENTES}$ de la cabeza de la regla**.
3. El vacío $\varepsilon$ **nunca** pertenece a un conjunto de siguientes.

Rastreo exhaustivo en los cuerpos de las producciones:

### Para $S$:
- Regla 1: $S$ es el símbolo inicial $\implies \$ \in \text{SIGUIENTES}(S)$.
- Regla 2: En $S \to S \text{ dos}$, a la derecha de $S$ está el terminal `dos` $\implies \text{dos} \in \text{SIGUIENTES}(S)$.
$$\text{SIGUIENTES}(S) = \{\$, \text{dos}\}$$

### Para $A$:
- Regla 1: En $S \to A \text{ uno } B C$, a la derecha de $A$ está directamente el terminal `uno` $\implies \text{uno} \in \text{SIGUIENTES}(A)$.
- Regla 4: En $A \to A \text{ tres}$, a la derecha de $A$ está directamente el terminal `tres` $\implies \text{tres} \in \text{SIGUIENTES}(A)$.
$$\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$$

### Para $C$:
- Regla 1: En $S \to A \text{ uno } B C$, la variable $C$ está al final de la producción. Por lo tanto, hereda todo $\text{SIGUIENTES}(S) = \{\$, \text{dos}\}$.
- Regla 3: En $A \to B C D$, a la derecha de $C$ está $D$.
  - Se agrega $\text{PRIMEROS}(D) \setminus \{\varepsilon\} = \{\text{seis}\}$.
  - Pero $D$ es anulable, lo que significa que $D$ puede borrarse y dejar a $C$ expuesto al final. Por ende, $C$ también hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 6: En $B \to D \text{ cuatro } C \text{ tres}$, a la derecha de $C$ está el terminal `tres` (ya incluido).
$$\text{SIGUIENTES}(C) = \{\$, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$$

### Para $B$:
- Regla 1: En $S \to A \text{ uno } B C$, a la derecha de $B$ está $C$.
  - Se añade $\text{PRIMEROS}(C) \setminus \{\varepsilon\} = \{\text{cinco}\}$.
  - Pero $C$ es anulable. Si $C$ se borra, $B$ queda al final y hereda $\text{SIGUIENTES}(S) = \{\$, \text{dos}\}$.
- Regla 3: En $A \to B C D$, a la derecha de $B$ está la secuencia $C D$.
  - Añade $\text{PRIMEROS}(C) \setminus \{\varepsilon\} = \{\text{cinco}\}$.
  - Como $C$ es anulable, añade $\text{PRIMEROS}(D) \setminus \{\varepsilon\} = \{\text{seis}\}$.
  - Como $C$ y $D$ se pueden anular a la vez ($CD \Rightarrow^* \varepsilon$), $B$ hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 8: En $C \to \text{cinco } D B$, $B$ está al final de la regla, por lo que hereda todo $\text{SIGUIENTES}(C) = \{\$, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$.
Uniendo todo:
$$\text{SIGUIENTES}(B) = \{\$, \text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$$

### Para $D$:
- Regla 3: En $A \to B C D$, $D$ está al final, así que hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 6: En $B \to D \text{ cuatro } C \text{ tres}$, a la derecha de $D$ está el terminal `cuatro` $\implies \text{cuatro} \in \text{SIGUIENTES}(D)$.
- Regla 8: En $C \to \text{cinco } D B$, a la derecha de $D$ está $B$.
  - Añade $\text{PRIMEROS}(B) \setminus \{\varepsilon\} = \{\text{cuatro}, \text{seis}\}$.
  - Como $B$ es anulable, $D$ queda al final y hereda $\text{SIGUIENTES}(C) = \{\$, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$.
Uniendo todas las fuentes:
$$\text{SIGUIENTES}(D) = \{\$, \text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$$

---

## 6. Paso 3: Conjuntos de prediccion de las reglas

El conjunto de predicción de una regla $A \to \alpha$ le dice al compilador: *"Si tienes a $A$ en la cima de la pila y en la entrada estás viendo cualquiera de estos tokens, aplica esta regla"*.

La fórmula matemática estándar es:
- **Si el cuerpo $\alpha$ no deriva en vacío:** $\text{PRED}(A \to \alpha) = \text{PRIMEROS}(\alpha)$.
- **Si el cuerpo $\alpha$ sí puede derivar en vacío:** $\text{PRED}(A \to \alpha) = (\text{PRIMEROS}(\alpha) \setminus \{\varepsilon\}) \cup \text{SIGUIENTES}(A)$. *(Porque si la regla decide anularse, el token entrante será alguno de los que pueden venir después de $A$)*.

Evaluando cada una de las 11 reglas:

| ID | Regla | ¿Es Anulable? | Cálculo Detallado | Conjunto de PREDICCIÓN |
| :---: | :--- | :---: | :--- | :--- |
| **1** | $S \to A \text{ uno } B C$ | No | $\text{PRIMEROS}(A \text{ uno } B C)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **2** | $S \to S \text{ dos}$ | No | $\text{PRIMEROS}(S \text{ dos}) = \text{PRIMEROS}(S)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **3** | $A \to B C D$ | Sí | $(\text{PRIM}(BCD) \setminus \{\varepsilon\}) \cup \text{SIG}(A)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **4** | $A \to A \text{ tres}$ | No | $\text{PRIMEROS}(A \text{ tres})$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$ |
| **5** | $A \to \varepsilon$ | Sí | $\text{SIGUIENTES}(A)$ | $\{\text{tres}, \text{uno}\}$ |
| **6** | $B \to D \text{ cuatro } C \text{ tres}$ | No | $\text{PRIMEROS}(D \text{ cuatro } C \text{ tres})$ | $\{\text{cuatro}, \text{seis}\}$ |
| **7** | $B \to \varepsilon$ | Sí | $\text{SIGUIENTES}(B)$ | $\{\$, \text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **8** | $C \to \text{cinco } D B$ | No | $\text{PRIMEROS}(\text{cinco } D B)$ | $\{\text{cinco}\}$ |
| **9** | $C \to \varepsilon$ | Sí | $\text{SIGUIENTES}(C)$ | $\{\$, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **10** | $D \to \text{seis}$ | No | $\text{PRIMEROS}(\text{seis})$ | $\{\text{seis}\}$ |
| **11** | $D \to \varepsilon$ | Sí | $\text{SIGUIENTES}(D)$ | $\{\$, \text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}\}$ |

---

## 7. Por qué esta gramática falla para un parser predictivo?

Para que una gramática sea determinista **LL(1)**, se exige que las alternativas de un mismo no terminal tengan conjuntos de predicción **totalmente disjuntos** (intersección vacía). 

Al analizar los resultados, observamos que **esta gramática NO es LL(1)** debido a colisiones masivas en casi todos sus no terminales:

1. **Colisión en $S$:**
   $$\text{PRED}(S \to A \text{ uno } B C) \cap \text{PRED}(S \to S \text{ dos}) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$$
   Las dos reglas reaccionan a los mismos 5 tokens. Si el parser ve cualquiera de ellos, no tiene forma de saber cuál producción escoger. Además, $S \to S \text{ dos}$ tiene recursión izquierda directa, lo cual cuelga a un analizador predictivo en un bucle infinito.

2. **Colisión en $A$:**
   - La regla 3 y la regla 4 colisionan en: $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$.
   - La regla 3 y la regla 5 colisionan en: $\{\text{tres}, \text{uno}\}$.
   - La regla 4 y la regla 5 colisionan en: $\{\text{tres}\}$.
   Posee recursión izquierda en $A \to A \text{ tres}$ y conflicto de anulación con la regla 5.

3. **Colisión en $B$:**
   $$\text{PRED}(B \to D \text{ cuatro } C \text{ tres}) \cap \text{PRED}(B \to \varepsilon) = \{\text{seis}\}$$
   Si el token entrante es `seis`, el parser no puede decidir si debe construir la estructura de $B$ o considerarlo vacío ($\varepsilon$).

4. **Colisión en $D$:**
   $$\text{PRED}(D \to \text{seis}) \cap \text{PRED}(D \to \varepsilon) = \{\text{seis}\}$$
   Existe colisión idéntica sobre el token `seis`.

**Caso excepcional:**
El no terminal $C$ es el único bien comportado en toda la gramática:
$$\text{PRED}(C \to \text{cinco } D B) \cap \text{PRED}(C \to \varepsilon) = \{\text{cinco}\} \cap \{\$, \text{dos}, \text{seis}, \text{tres}, \text{uno}\} = \emptyset$$
Para $C$ sí existe decisión determinista con un solo token de anticipación.

---

## 8. Verificación con el código en Python (analítico vs algorítmico)

El script `algoritmos_sintacticos.py` codifica los algoritmos de punto fijo formales para gramáticas arbitrarias. Al correrlo, efectúa una comprobación estricta de aserción (`assert`) comparando la solución manual contra la solución generada por la máquina.

### Resumen de Coincidencia:

| Conjunto | Estado de Validación |
| :--- | :---: |
| **Conjuntos PRIMEROS** | **100% Coincide** (sin diferencias) |
| **Conjuntos SIGUIENTES** | **100% Coincide** (sin diferencias) |
| **Conjuntos PREDICCIÓN** | **100% Coincide** (sin diferencias) |

---

## 9. Guía de Ejecución en Linux y WSL

El proyecto fue desarrollado utilizando las librerías nativas de Python 3, por lo que no requiere instalación de paquetes de terceros.

### Paso 1: Abrir la terminal y ubicarse en la carpeta
```bash
cd tareaalgoritmosprimeros
```

### Paso 2: (Opcional) Activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Ejecutar el algoritmo
```bash
python3 algoritmos_sintacticos.py
```