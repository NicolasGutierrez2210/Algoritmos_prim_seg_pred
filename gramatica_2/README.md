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

## 2. Gramática del taller

Trabajamos sobre la siguiente gramática formal:

- **Símbolos No Terminales (VN):** {S, A, B, C, D}
- **Símbolos Terminales (VT):** {uno, dos, tres, cuatro, cinco, seis}
- **Símbolo Inicial:** S
- **Fin de entrada (EOF):** $
- **Cadena vacía:** ε

### Reglas de producción numeradas:
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

## 3. Primer paso: Identificación de símbolos anulables (Nullability)

Un no terminal se considera **anulable** si tiene la capacidad de evaporarse por completo, es decir, de derivar en la cadena vacía ε (X =>* ε). 

Saber quién es anulable es el primer paso obligatorio, porque cuando una variable en una secuencia puede desaparecer, el token inicial ya no lo dictará ella, sino la variable que esté parada inmediatamente a su derecha.

Analizando las reglas:
- **D:** Tiene la regla directa `D -> ε`. Por tanto, **D es anulable**.
- **C:** Tiene la regla directa `C -> ε`. Por tanto, **C es anulable**.
- **B:** Tiene la regla directa `B -> ε`. Por tanto, **B es anulable**.
- **A:** Tiene la regla directa `A -> ε`. Además, la regla `A -> B C D` está compuesta por tres variables donde todas son anulables (B, C, D =>* ε). Por tanto, **A es anulable**.
- **S:** La regla 1 (`S -> A uno B C`) tiene en medio al terminal obligatorio `uno`, el cual nunca puede borrarse. La regla 2 (`S -> S dos`) tiene al terminal `dos`. Por ende, ninguna combinación permite que S se transforme en vacío. **S NO es anulable**.

### Resumen de anulabilidad:
```text
Anulables    = {A, B, C, D}
No Anulables = {S}
```

---

## 4. Segundo paso: Cálculo analítico de PRIMEROS

La regla lógica para calcular `PRIMEROS(X)` sigue el principio de propagación en cadena (efecto dominó):
- Si el cuerpo arranca con un terminal, ese terminal entra directo.
- Si arranca con un no terminal Y, hereda todos los terminales de `PRIMEROS(Y)`.
- Si ese Y es anulable, no nos podemos detener ahí: la puerta queda abierta y tenemos que mirar también a los `PRIMEROS` del siguiente símbolo en la lista, y así sucesivamente hasta toparnos con alguien que no sea anulable.
- Si toda la fila de símbolos es anulable, ε se agrega al conjunto de `PRIMEROS`.

Deducción variable por variable:

### Para D:
- Regla 10: `D -> seis` => aporta el terminal `seis`.
- Regla 11: `D -> ε` => aporta `ε`.
```text
PRIMEROS(D) = {seis, ε}
```

### Para C:
- Regla 8: `C -> cinco D B` => arranca con el terminal `cinco`, así que aporta `cinco`.
- Regla 9: `C -> ε` => aporta `ε`.
```text
PRIMEROS(C) = {cinco, ε}
```

### Para B:
- Regla 6: `B -> D cuatro C tres`.
  - El primer elemento es D, por lo que heredamos los terminales de D: `seis`.
  - Como D es anulable, el flujo continúa hacia el siguiente símbolo: el terminal `cuatro`. Se incluye `cuatro`.
  - Como `cuatro` es un terminal rígido (no se anula), la propagación se frena aquí.
- Regla 7: `B -> ε` => aporta `ε`.
```text
PRIMEROS(B) = {cuatro, seis, ε}
```

### Para A:
- Regla 3: `A -> B C D`.
  - Empieza con B: aporta `PRIMEROS(B) - {ε} = {cuatro, seis}`.
  - Como B es anulable, pasa a C: aporta `PRIMEROS(C) - {ε} = {cinco}`.
  - Como C es anulable, pasa a D: aporta `PRIMEROS(D) - {ε} = {seis}` (ya presente).
  - Como todos (B, C, D) son anulables a la vez, toda la producción puede desaparecer: aporta `ε`.
- Regla 4: `A -> A tres`.
  - Como sabemos que A puede derivar en vacío (A =>* ε), podemos hacer la sustitución mental: A => A tres => ε tres = `tres`. Esto significa que una cadena derivada de A puede comenzar legítimamente por el terminal `tres`. Por tanto, se añade `tres`.
- Regla 5: `A -> ε` => aporta `ε`.
```text
PRIMEROS(A) = {cinco, cuatro, seis, tres, ε}
```

### Para S:
- Regla 1: `S -> A uno B C`.
  - Arranca con A: aporta todos los terminales de A, es decir: `{cinco, cuatro, seis, tres}`.
  - Como A es anulable, pasamos al siguiente símbolo: el terminal `uno`. Se añade `uno`.
  - `uno` no se anula, por lo que aquí termina la propagación. Como la producción contiene a `uno`, no deriva en ε.
- Regla 2: `S -> S dos`.
  - Contiene a `PRIMEROS(S)`, sin añadir nuevos símbolos.
```text
PRIMEROS(S) = {cinco, cuatro, seis, tres, uno}
```

---

## 5. Tercer paso: Cálculo analítico de SIGUIENTES

El conjunto `SIGUIENTES(X)` no describe lo que X produce por dentro, sino **quién puede aparecer pegado a su derecha en cualquier parte de una derivación válida**.

Reglas clave para deducirlo:
1. El símbolo inicial siempre lleva el fin de archivo: `$` pertenece a `SIGUIENTES(S)`.
2. En cualquier lado derecho donde aparezca X, miramos al vecino que tiene a su derecha (llamémoslo β):
   - Todo lo que pueda comenzar β (`PRIMEROS(β) - {ε}`) formará parte de `SIGUIENTES(X)`.
   - Si ese vecino β no existe (porque X está al puro final de la regla), o si β es anulable (puede desvanecerse), entonces **X hereda todo el conjunto SIGUIENTES de la cabeza de la regla**.
3. El vacío ε **nunca** pertenece a un conjunto de siguientes.

Rastreo exhaustivo en los cuerpos de las producciones:

### Para S:
- Regla 1: S es el símbolo inicial => `$` pertenece a `SIGUIENTES(S)`.
- Regla 2: En `S -> S dos`, a la derecha de S está el terminal `dos` => `dos` entra a `SIGUIENTES(S)`.
```text
SIGUIENTES(S) = {dos, $}
```

### Para A:
- Regla 1: En `S -> A uno B C`, a la derecha de A está directamente el terminal `uno` => `uno` entra a `SIGUIENTES(A)`.
- Regla 4: En `A -> A tres`, a la derecha de A está directamente el terminal `tres` => `tres` entra a `SIGUIENTES(A)`.
```text
SIGUIENTES(A) = {tres, uno}
```

### Para C:
- Regla 1: En `S -> A uno B C`, la variable C está al final de la producción. Por lo tanto, hereda todo `SIGUIENTES(S) = {dos, $}`.
- Regla 3: En `A -> B C D`, a la derecha de C está D.
  - Se agrega `PRIMEROS(D) - {ε} = {seis}`.
  - Pero D es anulable, lo que significa que D puede borrarse y dejar a C expuesto al final. Por ende, C también hereda `SIGUIENTES(A) = {tres, uno}`.
- Regla 6: En `B -> D cuatro C tres`, a la derecha de C está el terminal `tres` (ya incluido).
```text
SIGUIENTES(C) = {dos, seis, tres, uno, $}
```

### Para B:
- Regla 1: En `S -> A uno B C`, a la derecha de B está C.
  - Se añade `PRIMEROS(C) - {ε} = {cinco}`.
  - Pero C es anulable. Si C se borra, B queda al final y hereda `SIGUIENTES(S) = {dos, $}`.
- Regla 3: En `A -> B C D`, a la derecha de B está la secuencia C D.
  - Añade `PRIMEROS(C) - {ε} = {cinco}`.
  - Como C es anulable, añade `PRIMEROS(D) - {ε} = {seis}`.
  - Como C y D se pueden anular a la vez (C D =>* ε), B hereda `SIGUIENTES(A) = {tres, uno}`.
- Regla 8: En `C -> cinco D B`, B está al final de la regla, por lo que hereda todo `SIGUIENTES(C) = {dos, seis, tres, uno, $}`.
Uniendo todo:
```text
SIGUIENTES(B) = {cinco, dos, seis, tres, uno, $}
```

### Para D:
- Regla 3: En `A -> B C D`, D está al final, así que hereda `SIGUIENTES(A) = {tres, uno}`.
- Regla 6: En `B -> D cuatro C tres`, a la derecha de D está el terminal `cuatro` => `cuatro` entra a `SIGUIENTES(D)`.
- Regla 8: En `C -> cinco D B`, a la derecha de D está B.
  - Añade `PRIMEROS(B) - {ε} = {cuatro, seis}`.
  - Como B es anulable, D queda al final y hereda `SIGUIENTES(C) = {dos, seis, tres, uno, $}`.
Uniendo todas las fuentes:
```text
SIGUIENTES(D) = {cuatro, dos, seis, tres, uno, $}
```

---

## 6. Cuarto paso: Conjuntos de prediccion de las reglas

El conjunto de predicción de una regla `A -> α` le dice al compilador: *"Si tienes a A en la cima de la pila y en la entrada estás viendo cualquiera de estos tokens, aplica esta regla"*.

La regla de cálculo es directa:
- **Si el cuerpo α no deriva en vacío:**  
  `PRED(A -> α) = PRIMEROS(α)`
- **Si el cuerpo α sí puede derivar en vacío:**  
  `PRED(A -> α) = (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A)`  
  *(Porque si la regla decide evaporarse vía ε, el token que se leerá será alguno de los que válidamente pueden seguir a A)*.

### Tabla detallada de predicción por regla:

| ID | Regla | ¿Es anulable? | Fórmula de cálculo | Conjunto de prediccion |
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

## 7. Por qué esta gramática falla para un parser predictivo?

Para que una gramática sea determinista **LL(1)**, se exige que las alternativas de un mismo no terminal tengan conjuntos de predicción **totalmente disjuntos** (su intersección debe ser vacía). 

Al analizar los resultados, observamos que **esta gramática NO es LL(1)** debido a colisiones en casi todos sus no terminales:

1. **Colisión en S:**
   ```text
   PRED(S -> A uno B C) ∩ PRED(S -> S dos) = {cinco, cuatro, seis, tres, uno}
   ```
   Las dos reglas reaccionan exactamente a los mismos 5 tokens. Si el parser ve cualquiera de ellos, no tiene forma de saber cuál producción escoger. Además, `S -> S dos` tiene recursión izquierda directa, lo cual cuelga a un analizador predictivo en un bucle infinito.

2. **Colisión en A:**
   - La regla 3 y la regla 4 colisionan en: `{cinco, cuatro, seis, tres}`.
   - La regla 3 y la regla 5 colisionan en: `{tres, uno}`.
   - La regla 4 y la regla 5 colisionan en: `{tres}`.
   Posee recursión izquierda en `A -> A tres` y conflicto de anulación con la regla 5.

3. **Colisión en B:**
   ```text
   PRED(B -> D cuatro C tres) ∩ PRED(B -> ε) = {seis}
   ```
   Si el token entrante es `seis`, el parser no puede decidir si debe construir la estructura de B o considerarlo vacío (ε).

4. **Colisión en D:**
   ```text
   PRED(D -> seis) ∩ PRED(D -> ε) = {seis}
   ```
   Existe colisión idéntica sobre el token `seis`.

**Caso excepcional:**
El no terminal C es el único bien comportado en toda la gramática:
```text
PRED(C -> cinco D B) ∩ PRED(C -> ε) = {cinco} ∩ {dos, seis, tres, uno, $} = ∅
```
Para C sí existe decisión determinista con un solo token de anticipación.

---

## 8. Verificación con el código en Python (analitico vs. algoritmico)

El script `algoritmos_sintacticos.py` codifica los algoritmos de punto fijo formales para gramáticas arbitrarias. Al correrlo, efectúa una comprobación estricta de aserción (`assert`) comparando la solución manual contra la solución generada por la máquina.

### Tabla comparativa:

| No terminal | PRIMEROS (Analítico) | PRIMEROS (Python) | SIGUIENTES (Analítico) | SIGUIENTES (Python) |
| :---: | :--- | :--- | :--- | :--- |
| **S** | `{cinco, cuatro, seis, tres, uno}` | `{cinco, cuatro, seis, tres, uno}` | `{dos, $}` | `{dos, $}` |
| **A** | `{cinco, cuatro, seis, tres, ε}` | `{cinco, cuatro, seis, tres, ε}` | `{tres, uno}` | `{tres, uno}` |
| **B** | `{cuatro, seis, ε}` | `{cuatro, seis, ε}` | `{cinco, dos, seis, tres, uno, $}` | `{cinco, dos, seis, tres, uno, $}` |
| **C** | `{cinco, ε}` | `{cinco, ε}` | `{dos, seis, tres, uno, $}` | `{dos, seis, tres, uno, $}` |
| **D** | `{seis, ε}` | `{seis, ε}` | `{cuatro, dos, seis, tres, uno, $}` | `{cuatro, dos, seis, tres, uno, $}` |

### Resumen de coincidencia:
- **Conjuntos PRIMEROS:** 100% Coincide (sin diferencias).
- **Conjuntos SIGUIENTES:** 100% Coincide (sin diferencias).
- **Conjuntos PREDICCIÓN:** 100% Coincide (sin diferencias).

---

## 9. Guía de ejecución en Linux y WSL

La tarea fue desarrollada utilizando las librerías nativas de Python 3, por lo que no requiere instalación de otros paquetes.

### Paso 1: Abrir la terminal y ubicarse en la carpeta
```bash
cd gramatica_2
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
