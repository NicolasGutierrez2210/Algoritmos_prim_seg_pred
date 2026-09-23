#!/usr/bin/env python3
import sys

# Configurar salida estándar en UTF-8 para caracteres especiales como ε
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Gramatica:
    def __init__(self, no_terminales, terminales, simbolo_inicial, producciones):
        self.VN = set(no_terminales)
        self.VT = set(terminales)
        self.S = simbolo_inicial
        # Lista de tuplas: (indice, cabeza, [cuerpo])
        self.producciones = producciones
        self.EPSILON = "ε"
        self.FIN_CADENA = "$"

    def es_terminal(self, simbolo):
        return simbolo in self.VT

    def es_no_terminal(self, simbolo):
        return simbolo in self.VN

    def es_epsilon(self, simbolo):
        return simbolo == self.EPSILON or simbolo == "epsilon"

    def calcular_anulables(self):
        """
        Calcula qué no terminales pueden derivar en la cadena vacía ε (punto fijo).
        """
        anulables = set()
        cambio = True
        while cambio:
            cambio = False
            for idx, cabeza, cuerpo in self.producciones:
                if cabeza not in anulables:
                    # Si la producción es epsilon directa
                    if len(cuerpo) == 1 and self.es_epsilon(cuerpo[0]):
                        anulables.add(cabeza)
                        cambio = True
                    # O si todos los símbolos del cuerpo son anulables
                    elif len(cuerpo) > 0 and all(s in anulables for s in cuerpo):
                        anulables.add(cabeza)
                        cambio = True
        return anulables

    def primeros_de_secuencia(self, secuencia, primeros_nt, anulables):
        """
        Calcula PRIMEROS para una secuencia arbitraria X_1 X_2 ... X_k.
        Reglas de la diapositiva 11 (05_LP_2026_2.pdf):
        1. Si X1 es terminal, agrega X1 y termina.
        2. Si X1 es no terminal, agrega PRIMEROS(X1) - {ε}.
        3. Si ε in PRIMEROS(X1), continúa con X2 y así sucesivamente.
        4. Si todos los Xi son anulables, agrega ε.
        """
        resultado = set()
        if not secuencia or (len(secuencia) == 1 and self.es_epsilon(secuencia[0])):
            resultado.add(self.EPSILON)
            return resultado

        todos_anulables = True
        for simbolo in secuencia:
            if self.es_terminal(simbolo):
                resultado.add(simbolo)
                todos_anulables = False
                break
            elif self.es_no_terminal(simbolo):
                prim_simb = primeros_nt[simbolo]
                resultado.update(prim_simb - {self.EPSILON})
                if simbolo not in anulables and self.EPSILON not in prim_simb:
                    todos_anulables = False
                    break
            elif self.es_epsilon(simbolo):
                continue
            else:
                # Símbolo desconocido, tratar como terminal
                resultado.add(simbolo)
                todos_anulables = False
                break

        if todos_anulables:
            resultado.add(self.EPSILON)

        return resultado

    def calcular_primeros(self):
        """
        Algoritmo de punto fijo para PRIMEROS (diapositivas 13 y 14).
        """
        anulables = self.calcular_anulables()
        primeros = {nt: set() for nt in self.VN}

        cambio = True
        iteracion = 0
        while cambio:
            cambio = False
            iteracion += 1
            for idx, cabeza, cuerpo in self.producciones:
                antes = len(primeros[cabeza])
                if len(cuerpo) == 1 and self.es_epsilon(cuerpo[0]):
                    primeros[cabeza].add(self.EPSILON)
                else:
                    prim_cuerpo = self.primeros_de_secuencia(cuerpo, primeros, anulables)
                    primeros[cabeza].update(prim_cuerpo)

                if len(primeros[cabeza]) > antes:
                    cambio = True

        return primeros, anulables

    def calcular_siguientes(self, primeros, anulables):
        """
        Algoritmo de punto fijo para SIGUIENTES (diapositivas 15 y 16).
        Reglas:
        1. $ in SIGUIENTES(S)
        2. Para cada regla A -> α B β:
           - Agregar PRIMEROS(β) - {ε} a SIGUIENTES(B).
           - Si β =>* ε o β está vacía, agregar SIGUIENTES(A) a SIGUIENTES(B).
        3. ε NUNCA pertenece a SIGUIENTES.
        """
        siguientes = {nt: set() for nt in self.VN}
        siguientes[self.S].add(self.FIN_CADENA)

        cambio = True
        iteracion = 0
        while cambio:
            cambio = False
            iteracion += 1
            for idx, A, cuerpo in self.producciones:
                # Si el cuerpo es epsilon, no hay no terminales que sigan a nadie
                if len(cuerpo) == 1 and self.es_epsilon(cuerpo[0]):
                    continue

                for i, B in enumerate(cuerpo):
                    if self.es_no_terminal(B):
                        beta = cuerpo[i + 1:]
                        antes = len(siguientes[B])

                        if beta:
                            prim_beta = self.primeros_de_secuencia(beta, primeros, anulables)
                            siguientes[B].update(prim_beta - {self.EPSILON})
                            # Si beta deriva en epsilon, SIGUIENTES(A) pasa a SIGUIENTES(B)
                            if self.EPSILON in prim_beta or all(s in anulables for s in beta):
                                siguientes[B].update(siguientes[A])
                        else:
                            # beta está vacía: B está al final de la producción
                            siguientes[B].update(siguientes[A])

                        if len(siguientes[B]) > antes:
                            cambio = True

        # Asegurar que ε jamás esté en ningún conjunto de siguientes
        for nt in siguientes:
            siguientes[nt].discard(self.EPSILON)

        return siguientes

    def calcular_prediccion(self, primeros, siguientes, anulables):
        """
        Calcula el conjunto de predicción para cada producción A -> α (diapositiva 17 y 18):
        PRED(A -> α) =
            PRIMEROS(α)                           si ε ∉ PRIMEROS(α)
            (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A)   si ε ∈ PRIMEROS(α)
        """
        predicciones = {}
        for idx, A, cuerpo in self.producciones:
            prim_alfa = self.primeros_de_secuencia(cuerpo, primeros, anulables)
            if self.EPSILON in prim_alfa:
                pred = (prim_alfa - {self.EPSILON}) | siguientes[A]
            else:
                pred = set(prim_alfa)
            predicciones[idx] = {
                "cabeza": A,
                "cuerpo": cuerpo,
                "primeros_alfa": prim_alfa,
                "prediccion": pred
            }
        return predicciones

    def verificar_ll1(self, predicciones):
        """
        Verifica el criterio LL(1) (diapositiva 9 y 24):
        Para cada no terminal A, las alternativas deben tener conjuntos de predicción disjuntos.
        """
        conflictos = {}
        es_ll1 = True

        por_no_terminal = {nt: [] for nt in self.VN}
        for idx, info in predicciones.items():
            por_no_terminal[info["cabeza"]].append((idx, info["cuerpo"], info["prediccion"]))

        for nt, reglas in por_no_terminal.items():
            conflictos[nt] = []
            for i in range(len(reglas)):
                for j in range(i + 1, len(reglas)):
                    r1_idx, r1_cuerpo, p1 = reglas[i]
                    r2_idx, r2_cuerpo, p2 = reglas[j]
                    interseccion = p1 & p2
                    if interseccion:
                        es_ll1 = False
                        conflictos[nt].append({
                            "regla1": (r1_idx, r1_cuerpo, p1),
                            "regla2": (r2_idx, r2_cuerpo, p2),
                            "interseccion": interseccion
                        })

        return es_ll1, conflictos


def construir_gramatica_taller():
    """
    Construye la gramática del ejercicio:
    S -> A uno B C
    S -> S dos
    A -> B C D
    A -> A tres
    A -> ε
    B -> D cuatro C tres
    B -> ε
    C -> cinco D B
    C -> ε
    D -> seis
    D -> ε
    """
    no_terminales = ["S", "A", "B", "C", "D"]
    terminales = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
    simbolo_inicial = "S"

    producciones = [
        (1, "S", ["A", "uno", "B", "C"]),
        (2, "S", ["S", "dos"]),
        (3, "A", ["B", "C", "D"]),
        (4, "A", ["A", "tres"]),
        (5, "A", ["ε"]),
        (6, "B", ["D", "cuatro", "C", "tres"]),
        (7, "B", ["ε"]),
        (8, "C", ["cinco", "D", "B"]),
        (9, "C", ["ε"]),
        (10, "D", ["seis"]),
        (11, "D", ["ε"])
    ]

    return Gramatica(no_terminales, terminales, simbolo_inicial, producciones)


def imprimir_tabla(titulo, encabezados, filas, anchos=None):
    print(f"\n{'=' * 80}")
    print(f" {titulo.upper()}")
    print(f"{'=' * 80}")
    if not anchos:
        anchos = [max(len(str(fila[i])) for fila in [encabezados] + filas) + 2 for i in range(len(encabezados))]

    formato_enc = " | ".join(f"{{:<{w}}}" for w in anchos)
    separador = "-+-".join("-" * w for w in anchos)

    print(formato_enc.format(*encabezados))
    print(separador)
    for fila in filas:
        print(formato_enc.format(*[str(x) for x in fila]))
    print(f"{'=' * 80}\n")


def main():
    gram = construir_gramatica_taller()

    # 1. Ejecutar algoritmos de cálculo
    primeros, anulables = gram.calcular_primeros()
    siguientes = gram.calcular_siguientes(primeros, anulables)
    predicciones = gram.calcular_prediccion(primeros, siguientes, anulables)
    es_ll1, conflictos = gram.verificar_ll1(predicciones)

    # 2. Mostrar Anulabilidad
    filas_anulables = [[nt, "Sí (deriva en ε)" if nt in anulables else "No"] for nt in sorted(gram.VN)]
    imprimir_tabla("Símbolos Anulables (Nullability)", ["No Terminal", "¿Es Anulable?"], filas_anulables, [15, 30])

    # 3. Mostrar Conjuntos PRIMEROS
    filas_primeros = []
    for nt in ["S", "A", "B", "C", "D"]:
        elem = sorted(list(primeros[nt]), key=lambda x: (x == "ε", x))
        filas_primeros.append([nt, "{" + ", ".join(elem) + "}"])
    imprimir_tabla("Conjuntos PRIMEROS", ["No Terminal", "PRIMEROS(X)"], filas_primeros, [15, 55])

    # 4. Mostrar Conjuntos SIGUIENTES
    filas_siguientes = []
    for nt in ["S", "A", "B", "C", "D"]:
        elem = sorted(list(siguientes[nt]), key=lambda x: (x == "$", x))
        filas_siguientes.append([nt, "{" + ", ".join(elem) + "}"])
    imprimir_tabla("Conjuntos SIGUIENTES", ["No Terminal", "SIGUIENTES(X)"], filas_siguientes, [15, 55])

    # 5. Mostrar Conjuntos de PREDICCIÓN
    filas_pred = []
    for idx in range(1, 12):
        info = predicciones[idx]
        cuerpo_str = " ".join(info["cuerpo"])
        regla_str = f"{info['cabeza']} -> {cuerpo_str}"
        elem_pred = sorted(list(info["prediccion"]), key=lambda x: (x == "$", x))
        filas_pred.append([f"Regla {idx}", regla_str, "{" + ", ".join(elem_pred) + "}"])
    imprimir_tabla("Conjuntos de PREDICCIÓN de las Reglas", ["ID Regla", "Producción", "PRED(A -> α)"], filas_pred, [12, 30, 45])

    # 6. Diagnóstico de Gramática LL(1)
    print("=" * 80)
    print(" EVALUACIÓN DE CRITERIO LL(1)")
    print("=" * 80)
    print(f"¿La gramática es LL(1)?: {'SÍ' if es_ll1 else 'NO'}")
    if not es_ll1:
        print("\nConflictos detectados (conjuntos de predicción con intersección no vacía):")
        for nt, lista_conf in conflictos.items():
            if lista_conf:
                print(f"\n[!] En No Terminal '{nt}':")
                for conf in lista_conf:
                    r1 = f"Regla {conf['regla1'][0]} ({nt} -> {' '.join(conf['regla1'][1])})"
                    r2 = f"Regla {conf['regla2'][0]} ({nt} -> {' '.join(conf['regla2'][1])})"
                    inter = "{" + ", ".join(sorted(list(conf['interseccion']))) + "}"
                    print(f"    - Conflicto entre:")
                    print(f"        {r1} con PRED = {{{', '.join(sorted(list(conf['regla1'][2])))}}}")
                    print(f"        {r2} con PRED = {{{', '.join(sorted(list(conf['regla2'][2])))}}}")
                    print(f"      -> Tokens de conflicto común: {inter}")
    print("=" * 80)

    # 7. Comparación formal Analítico vs Programático
    # Definimos la solución analítica obtenida paso a paso
    analitico_primeros = {
        "S": {"uno", "tres", "cuatro", "cinco", "seis"},
        "A": {"tres", "cuatro", "cinco", "seis", "ε"},
        "B": {"cuatro", "seis", "ε"},
        "C": {"cinco", "ε"},
        "D": {"seis", "ε"}
    }

    analitico_siguientes = {
        "S": {"$", "dos"},
        "A": {"uno", "tres"},
        "B": {"$", "dos", "tres", "uno", "cinco", "seis"},
        "C": {"$", "dos", "tres", "uno", "seis"},
        "D": {"$", "dos", "tres", "cuatro", "seis", "uno"}
    }

    analitico_predicciones = {
        1: {"uno", "tres", "cuatro", "cinco", "seis"},
        2: {"uno", "tres", "cuatro", "cinco", "seis"},
        3: {"uno", "tres", "cuatro", "cinco", "seis"},
        4: {"tres", "cuatro", "cinco", "seis"},
        5: {"uno", "tres"},
        6: {"cuatro", "seis"},
        7: {"$", "dos", "tres", "uno", "cinco", "seis"},
        8: {"cinco"},
        9: {"$", "dos", "tres", "uno", "seis"},
        10: {"seis"},
        11: {"$", "dos", "tres", "cuatro", "seis", "uno"}
    }

    coinciden_primeros = all(primeros[k] == analitico_primeros[k] for k in primeros)
    coinciden_siguientes = all(siguientes[k] == analitico_siguientes[k] for k in siguientes)
    coinciden_predicciones = all(predicciones[k]["prediccion"] == analitico_predicciones[k] for k in predicciones)

    print("\n" + "=" * 80)
    print(" COMPARACIÓN FORMAL: RESOLUCIÓN ANALÍTICA VS. IMPLEMENTACIÓN EN PYTHON")
    print("=" * 80)
    print(f" • Coincidencia en conjuntos PRIMEROS:    {'100% COINCIDE' if coinciden_primeros else 'DISCREPANCIA'}")
    print(f" • Coincidencia en conjuntos SIGUIENTES:  {'100% COINCIDE' if coinciden_siguientes else 'DISCREPANCIA'}")
    print(f" • Coincidencia en conjuntos PREDICCIÓN:  {'100% COINCIDE' if coinciden_predicciones else 'DISCREPANCIA'}")
    print("=" * 80)

    assert coinciden_primeros and coinciden_siguientes and coinciden_predicciones, "Error: Discrepancia entre cálculo analítico y algorítmico."


if __name__ == "__main__":
    main()
