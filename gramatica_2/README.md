# Taller: Análisis Sintáctico Descendente y Conjuntos de Predicción

**Curso:** Lenguajes de Programación y Traducción  
**Tema:** Cálculo de Anulabilidad, Primeros, Siguientes y Conjuntos de Predicción  
**Programa:** Ciencias de la Computación e Inteligencia Artificial (5to Semestre)  
**Institución:** Universidad Sergio Arboleda  

---

## 1. Justificación y Propósito: ¿Por qué calculamos estos conjuntos?

En compiladores y procesamiento de lenguajes, un analizador sintáctico descendente predictivo (como un parser LL(1)) tiene un objetivo muy puntual: **leer el código fuente token por token y decidir qué regla gramatical aplicar de forma determinista, sin titubear y sin tener que devolverse (sin backtracking)**.

Podemos pensar en el parser como un clasificador determinista en tiempo real:
- Ve un símbolo no terminal en su pila (por ejemplo, `A`).
- Observa el siguiente token de entrada (llamado *lookahead*).
- Con solo esa información, debe escoger con total certeza cuál de las reglas de `A` debe dispararse.

Para construir la tabla de decisiones de este clasificador, necesitamos tres herramientas matemáticas fundamentales:
1. **PRIMEROS:** Responde a la pregunta: *si expando esta variable o regla, ¿con qué tokens reales puede arrancar el texto?*
2. **SIGUIENTES:** Responde a la pregunta: *si esta variable se reduce, termina su trabajo o simplemente se borra (deriva en vacía), ¿qué tokens pueden aparecer inmediatamente a su derecha en el código?*
3. **PREDICCIÓN:** Es la combinación de las dos anteriores. Determina el conjunto exacto de tokens que deben hacer que el parser elija una producción específica.

Si para un mismo no terminal dos reglas distintas reaccionan al mismo token (sus conjuntos de predicción se cruzan), el parser sufrirá un conflicto de ambigüedad y no podrá ser LL(1).

---

## 2. La Gramática del Taller

Trabajamos sobre la siguiente gramática formal:

- **Símbolos No Terminales:** $V_N = \{S, A, B, C, D\}$
- **Símbolos Terminales:** $V_T = \{\text{uno}, \text{dos}, \text{tres}, \text{cuatro}, \text{cinco}, \text{seis}\}$
- **Símbolo Inicial:** $S$
- **Fin de entrada:** `$` *(marcador de fin de archivo / EOF)*
- **Cadena vacía:** $\varepsilon$

### Reglas de Producción Numeradas:
1. `S -> A uno B C`
2. `S -> S dos`
3. `A -> B C D`
4. `A -> A tres`
5. `A -> ε`
6. `B -> D cuatro C tres`
7. `B -> ε`
8. `C -> cinco D B`
9. `C -> ε`
10. `D -> seis`
11. `D -> ε`

---

## 3. Primer Paso: Identificación de Símbolos Anulables (Nullability)

Un no terminal se considera **anulable** si tiene la capacidad de evaporarse por completo, es decir, de derivar en la cadena vacía $\varepsilon$ ($X \Rightarrow^* \varepsilon$). 

Saber quién es anulable es el primer paso obligatorio, porque cuando una variable en una secuencia puede desaparecer, el token inicial ya no lo dictará ella, sino la variable que esté parada inmediatamente a su derecha.

Analizando las reglas:
- **$D$:** Tiene la regla directa `D -> ε`. Por tanto, **$D$ es anulable**.
- **$C$:** Tiene la regla directa `C -> ε`. Por tanto, **$C$ es anulable**.
- **$B$:** Tiene la regla directa `B -> ε`. Por tanto, **$B$ es anulable**.
- **$A$:** Tiene la regla directa `A -> ε`. Además, la regla `A -> B C D` está compuesta por tres variables donde todas son anulables ($B, C, D \Rightarrow^* \varepsilon$). Por tanto, **$A$ es anulable**.
- **$S$:** La regla 1 (`S -> A uno B C`) tiene en medio al terminal obligatorio `uno`, el cual nunca puede borrarse. La regla 2 (`S -> S dos`) tiene al terminal `dos`. Por ende, ninguna combinación permite que $S$ se transforme en vacío. **$S$ NO es anulable**.

**Resumen de Anulabilidad:**
$$
\text{Anulables} = \{A, B, C, D\}
$$
$$
\text{No Anulables} = \{S\}
$$

---

## 4. Segundo Paso: Cálculo Analítico de PRIMEROS

La regla lógica para calcular $\text{PRIMEROS}(X)$ sigue el principio de propagación en cadena (efecto dominó):
- Si el cuerpo arranca con un terminal, ese terminal entra directo.
- Si arranca con un no terminal $Y$, hereda todos los terminales de $\text{PRIMEROS}(Y)$.
- Si ese $Y$ es anulable, no nos podemos detener ahí: la puerta queda abierta y tenemos que mirar también a los $\text{PRIMEROS}$ del siguiente símbolo en la lista, y así sucesivamente hasta toparnos con alguien que no sea anulable.
- Si toda la fila de símbolos es anulable, $\varepsilon$ se agrega al conjunto de $\text{PRIMEROS}$.

Deducción variable por variable:

### Para $D$:
- Regla 10: `D -> seis` $\implies$ aporta el terminal `seis`.
- Regla 11: `D -> ε` $\implies$ aporta $\varepsilon$.
$$
\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}
$$

### Para $C$:
- Regla 8: `C -> cinco D B` $\implies$ arranca con el terminal `cinco`, así que aporta `cinco`.
- Regla 9: `C -> ε` $\implies$ aporta $\varepsilon$.
$$
\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}
$$

### Para $B$:
- Regla 6: `B -> D cuatro C tres`.
  - El primer elemento es $D$, por lo que heredamos los terminales de $D$: `seis`.
  - Como $D$ es anulable, el flujo continúa hacia el siguiente símbolo: el terminal `cuatro`. Se incluye `cuatro`.
  - Como `cuatro` es un terminal rígido (no se anula), la propagación se frena aquí.
- Regla 7: `B -> ε` $\implies$ aporta $\varepsilon$.
$$
\text{PRIMEROS}(B) = \{\text{cuatro}, \text{seis}, \varepsilon\}
$$

### Para $A$:
- Regla 3: `A -> B C D`.
  - Empieza con $B$: aporta $\text{PRIMEROS}(B) - \{\varepsilon\} = \{\text{cuatro}, \text{seis}\}$.
  - Como $B$ es anulable, pasa a $C$: aporta $\text{PRIMEROS}(C) - \{\varepsilon\} = \{\text{cinco}\}$.
  - Como $C$ es anulable, pasa a $D$: aporta $\text{PRIMEROS}(D) - \{\varepsilon\} = \{\text{seis}\}$ (ya presente).
  - Como todos ($B, C, D$) son anulables a la vez, toda la producción puede desaparecer: aporta $\varepsilon$.
- Regla 4: `A -> A tres`.
  - Como sabemos que $A$ puede derivar en vacío ($A \Rightarrow^* \varepsilon$), podemos hacer la sustitución mental: $A \Rightarrow A \text{ tres} \Rightarrow \varepsilon \text{ tres} = \text{tres}$. Esto significa que una cadena derivada de $A$ puede comenzar legítimamente por el terminal `tres`. Por tanto, se añade `tres`.
- Regla 5: `A -> ε` $\implies$ aporta $\varepsilon$.
$$
\text{PRIMEROS}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}
$$

### Para $S$:
- Regla 1: `S -> A uno B C`.
  - Arranca con $A$: aporta todos los terminales de $A$, es decir: $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$.
  - Como $A$ es anulable, pasamos al siguiente símbolo: el terminal `uno`. Se añade `uno`.
  - `uno` no se anula, por lo que aquí termina la propagación. Como la producción contiene a `uno`, no deriva en $\varepsilon$.
- Regla 2: `S -> S dos`.
  - Contiene a $\text{PRIMEROS}(S)$, sin añadir nuevos símbolos.
$$
\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}
$$

---

## 5. Tercer Paso: Cálculo Analítico de SIGUIENTES

El conjunto $\text{SIGUIENTES}(X)$ no describe lo que $X$ produce por dentro, sino **quién puede aparecer pegado a su derecha en cualquier parte de una derivación válida**.

Reglas clave para deducirlo:
1. El símbolo inicial siempre lleva el fin de archivo: `$` $\in \text{SIGUIENTES}(S)$.
2. En cualquier lado derecho donde aparezca $X$, miramos al vecino que tiene a su derecha ($\beta$):
   - Todo lo que pueda comenzar $\beta$ ($\text{PRIMEROS}(\beta) - \{\varepsilon\}$) formará parte de $\text{SIGUIENTES}(X)$.
   - Si ese vecino $\beta$ no existe (porque $X$ está al puro final de la regla), o si $\beta$ es anulable (puede desvanecerse), entonces **$X$ hereda todo el conjunto $\text{SIGUIENTES}$ de la cabeza de la regla**.
3. El vacío $\varepsilon$ **nunca** pertenece a un conjunto de siguientes.

Rastreo exhaustivo en los cuerpos de las producciones:

### Para $S$:
- Regla 1: $S$ es el símbolo inicial $\implies$ `$` $\in \text{SIGUIENTES}(S)$.
- Regla 2: En `S -> S dos`, a la derecha de $S$ está el terminal `dos` $\implies \text{dos} \in \text{SIGUIENTES}(S)$.
$$
\text{SIGUIENTES}(S) = \{\text{dos}, \$\}
$$

### Para $A$:
- Regla 1: En `S -> A uno B C`, a la derecha de $A$ está directamente el terminal `uno` $\implies \text{uno} \in \text{SIGUIENTES}(A)$.
- Regla 4: En `A -> A tres`, a la derecha de $A$ está directamente el terminal `tres` $\implies \text{tres} \in \text{SIGUIENTES}(A)$.
$$
\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}
$$

### Para $C$:
- Regla 1: En `S -> A uno B C`, la variable $C$ está al final de la producción. Por lo tanto, hereda todo $\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$.
- Regla 3: En `A -> B C D`, a la derecha de $C$ está $D$.
  - Se agrega $\text{PRIMEROS}(D) - \{\varepsilon\} = \{\text{seis}\}$.
  - Pero $D$ es anulable, lo que significa que $D$ puede borrarse y dejar a $C$ expuesto al final. Por ende, $C$ también hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 6: En `B -> D cuatro C tres`, a la derecha de $C$ está el terminal `tres` (ya incluido).
$$
\text{SIGUIENTES}(C) = \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}
$$

### Para $B$:
- Regla 1: En `S -> A uno B C`, a la derecha de $B$ está $C$.
  - Se añade $\text{PRIMEROS}(C) - \{\varepsilon\} = \{\text{cinco}\}$.
  - Pero $C$ es anulable. Si $C$ se borra, $B$ queda al final y hereda $\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$.
- Regla 3: En `A -> B C D`, a la derecha de $B$ está la secuencia $C D$.
  - Añade $\text{PRIMEROS}(C) - \{\varepsilon\} = \{\text{cinco}\}$.
  - Como $C$ es anulable, añade $\text{PRIMEROS}(D) - \{\varepsilon\} = \{\text{seis}\}$.
  - Como $C$ y $D$ se pueden anular a la vez ($CD \Rightarrow^* \varepsilon$), $B$ hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 8: En `C -> cinco D B`, $B$ está al final de la regla, por lo que hereda todo $\text{SIGUIENTES}(C) = \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$.
Uniendo todo:
$$
\text{SIGUIENTES}(B) = \{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}
$$

### Para $D$:
- Regla 3: En `A -> B C D`, $D$ está al final, así que hereda $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
- Regla 6: En `B -> D cuatro C tres`, a la derecha de $D$ está el terminal `cuatro` $\implies \text{cuatro} \in \text{SIGUIENTES}(D)$.
- Regla 8: En `C -> cinco D B`, a la derecha de $D$ está $B$.
  - Añade $\text{PRIMEROS}(B) - \{\varepsilon\} = \{\text{cuatro}, \text{seis}\}$.
  - Como $B$ es anulable, $D$ queda al final y hereda $\text{SIGUIENTES}(C) = \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$.
Uniendo todas las fuentes:
$$
\text{SIGUIENTES}(D) = \{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}
$$

---

## 6. Cuarto Paso: Conjuntos de PREDICCIÓN de las Reglas

El conjunto de predicción de una regla $A \to \alpha$ le dice al compilador: *"Si tienes a $A$ en la cima de la pila y en la entrada estás viendo cualquiera de estos tokens, aplica esta regla"*.

La regla de cálculo es directa:
- **Si el cuerpo $\alpha$ no deriva en vacío:**  
  $\text{PRED}(A \to \alpha) = \text{PRIMEROS}(\alpha)$.
- **Si el cuerpo $\alpha$ sí puede derivar en vacío:**  
  $\text{PRED}(A \to \alpha) = (\text{PRIMEROS}(\alpha) - \{\varepsilon\}) \cup \text{SIGUIENTES}(A)$.  
  *(Porque si la regla decide evaporarse vía $\varepsilon$, el token que se leerá será alguno de los que válidamente pueden seguir a $A$)*.

### Tabla Detallada de Predicción por Regla:

| ID | Regla | ¿Es Anulable? | Fórmula de Cálculo | Conjunto de PREDICCIÓN |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `S -> A uno B C` | No | `PRIMEROS(A uno B C)` | `{cinco, cuatro, seis, tres, uno}` |
| **2** | `S -> S dos` | No | `PRIMEROS(S dos)` | `{cinco, cuatro, seis, tres, uno}` |
| **3** | `A -> B C D` | Sí | `(PRIM(BCD) - {ε}) ∪ SIG(A)` | `{cinco, cuatro, seis, tres, uno}` |
| **4** | `A -> A tres` | No | `PRIMEROS(A tres)` | `{cinco, cuatro, seis, tres}` |
| **5** | `A -> ε` | Sí | `SIGUIENTES(A)` | `{tres, uno}` |
| **6** | `B -> D cuatro C tres` | No | `PRIMEROS(D cuatro C tres)` | `{cuatro, seis}` |
| **7** | `B -> ε` | Sí | `SIGUIENTES(B)` | `{cinco, dos, seis, tres, uno, $}` |
| **8** | `C -> cinco D B` | No | `PRIMEROS(cinco D B)` | `{cinco}` |
| **9** | `C -> ε` | Sí | `SIGUIENTES(C)` | `{dos, seis, tres, uno, $}` |
| **10** | `D -> seis` | No | `PRIMEROS(seis)` | `{seis}` |
| **11** | `D -> ε` | Sí | `SIGUIENTES(D)` | `{cuatro, dos, seis, tres, uno, $}` |

---

## 7. Evaluación del Criterio LL(1): ¿Por qué esta gramática falla para un parser predictivo?

Para que una gramática sea determinista **LL(1)**, se exige que las alternativas de un mismo no terminal tengan conjuntos de predicción **totalmente disjuntos** (su intersección debe ser vacía). 

Al analizar los resultados, observamos que **esta gramática NO es LL(1)** debido a colisiones en casi todos sus no terminales:

1. **Colisión en $S$:**
   $$
   \text{PRED}(S \to A \text{ uno } B C) \cap \text{PRED}(S \to S \text{ dos}) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}
   $$
   Las dos reglas reaccionan exactamente a los mismos 5 tokens. Si el parser ve cualquiera de ellos, no tiene forma de saber cuál producción escoger. Además, `S -> S dos` tiene recursión izquierda directa, lo cual cuelga a un analizador predictivo en un bucle infinito.

2. **Colisión en $A$:**
   - La regla 3 y la regla 4 colisionan en: `cinco`, `cuatro`, `seis`, `tres`.
   - La regla 3 y la regla 5 colisionan en: `tres`, `uno`.
   - La regla 4 y la regla 5 colisionan en: `tres`.
   Posee recursión izquierda en `A -> A tres` y conflicto de anulación con la regla 5.

3. **Colisión en $B$:**
   $$
   \text{PRED}(B \to D \text{ cuatro } C \text{ tres}) \cap \text{PRED}(B \to \varepsilon) = \{\text{seis}\}
   $$
   Si el token entrante es `seis`, el parser no puede decidir si debe construir la estructura de $B$ o considerarlo vacío ($\varepsilon$).

4. **Colisión en $D$:**
   $$
   \text{PRED}(D \to \text{seis}) \cap \text{PRED}(D \to \varepsilon) = \{\text{seis}\}
   $$
   Existe colisión idéntica sobre el token `seis`.

**Caso excepcional:**
El no terminal $C$ es el único bien comportado en toda la gramática:
$$
\text{PRED}(C \to \text{cinco } D B) \cap \text{PRED}(C \to \varepsilon) = \{\text{cinco}\} \cap \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\} = \emptyset
$$
Para $C$ sí existe decisión determinista con un solo token de anticipación.

---

## 8. Verificación con el Código en Python (Analítico vs. Algorítmico)

El script `algoritmos_sintacticos.py` codifica los algoritmos de punto fijo formales para gramáticas arbitrarias. Al correrlo, efectúa una comprobación estricta de aserción (`assert`) comparando la solución manual contra la solución generada por la máquina.

### Tabla Comparativa de Conjuntos:

| No Terminal | PRIMEROS (Analítico) | PRIMEROS (Python) | SIGUIENTES (Analítico) | SIGUIENTES (Python) |
| :---: | :--- | :--- | :--- | :--- |
| **S** | `{cinco, cuatro, seis, tres, uno}` | `{cinco, cuatro, seis, tres, uno}` | `{dos, $}` | `{dos, $}` |
| **A** | `{cinco, cuatro, seis, tres, ε}` | `{cinco, cuatro, seis, tres, ε}` | `{tres, uno}` | `{tres, uno}` |
| **B** | `{cuatro, seis, ε}` | `{cuatro, seis, ε}` | `{cinco, dos, seis, tres, uno, $}` | `{cinco, dos, seis, tres, uno, $}` |
| **C** | `{cinco, ε}` | `{cinco, ε}` | `{dos, seis, tres, uno, $}` | `{dos, seis, tres, uno, $}` |
| **D** | `{seis, ε}` | `{seis, ε}` | `{cuatro, dos, seis, tres, uno, $}` | `{cuatro, dos, seis, tres, uno, $}` |

### Resumen de Coincidencia:
- **Conjuntos PRIMEROS:** 100% Coincide (sin diferencias).
- **Conjuntos SIGUIENTES:** 100% Coincide (sin diferencias).
- **Conjuntos PREDICCIÓN:** 100% Coincide (sin diferencias).

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

### Paso 3: Ejecutar el script
```bash
python3 algoritmos_sintacticos.py
```

### Salida esperada en consola:
El script desplegará:
1. Tabla de anulabilidad de las variables.
2. Tablas con los conjuntos calculados de PRIMEROS y SIGUIENTES.
3. Desglose de los conjuntos de PREDICCIÓN para las 11 producciones.
4. Reporte detallado de conflictos LL(1) especificando qué reglas chocan y con qué tokens.
5. Validación formal de aserción confirmando el 100% de coincidencia analítica.

---

## 10. Estructura de Archivos

```text
tareaalgoritmosprimeros/
├── README.md                      # Esta guía conceptual y analítica detallada
├── algoritmos_sintacticos.py      # Implementación algorítmica en Python 3
├── Captura de pantalla...png      # Enunciado original de la tarea
└── .gitignore                     # Archivo de exclusiones para Git
```