from typing import Dict, List, Set, Tuple

# Constantes de control sintáctico
EPSILON = "ε"
FIN_CADENA = "$"


class GramaticaLL1:
    """
    Representa una Gramática Libre de Contexto G = (V_N, V_T, P, S)
    y provee métodos para el cómputo de sus conjuntos directores.
    """

    def __init__(
        self,
        no_terminales: List[str],
        terminales: List[str],
        simbolo_inicial: str,
        producciones: List[Tuple[int, str, List[str]]],
    ):
        """
        Inicializa la gramática formal.

        :param no_terminales: Lista de símbolos no terminales (V_N).
        :param terminales: Lista de símbolos terminales (V_T).
        :param simbolo_inicial: Axioma de inicio (S).
        :param producciones: Lista de tuplas (id_regla, no_terminal_izq, [simbolos_der]).
        """
        self.no_terminales: Set[str] = set(no_terminales)
        self.terminales: Set[str] = set(terminales)
        self.simbolo_inicial: str = simbolo_inicial
        self.producciones: List[Tuple[int, str, List[str]]] = producciones

    def primeros_de_cadena(
        self, secuencia: List[str], primeros_nt: Dict[str, Set[str]]
    ) -> Set[str]:
        """
        Calcula el conjunto PRIMEROS de una secuencia arbitraria de símbolos:
        PRIM(X1 X2 ... Xn).

        :param secuencia: Lista de símbolos de la forma sentencial.
        :param primeros_nt: Diccionario actual de conjuntos PRIMEROS de no terminales.
        :return: Conjunto de terminales resultantes (incluyendo ε si la cadena es anulable).
        """
        resultado: Set[str] = set()

        # Caso base: cadena vacía o explícitamente ε
        if not secuencia or secuencia == [EPSILON]:
            resultado.add(EPSILON)
            return resultado

        anulable_completamente = True

        for simbolo in secuencia:
            if simbolo in self.terminales:
                resultado.add(simbolo)
                anulable_completamente = False
                break
            elif simbolo in self.no_terminales:
                prim_simbolo = primeros_nt[simbolo]
                resultado.update(prim_simbolo - {EPSILON})
                # Si el símbolo actual no deriva en ε, se detiene la propagación a la derecha
                if EPSILON not in prim_simbolo:
                    anulable_completamente = False
                    break
            elif simbolo == EPSILON:
                continue
            else:
                raise ValueError(f"Símbolo no reconocido en la gramática: '{simbolo}'")

        if anulable_completamente:
            resultado.add(EPSILON)

        return resultado

    def calcular_primeros(self) -> Dict[str, Set[str]]:
        """
        Calcula de forma iterativa (punto fijo) los conjuntos de PRIMEROS
        para cada símbolo no terminal de la gramática.
        """
        primeros: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}

        cambio = True
        iteracion = 0
        while cambio:
            cambio = False
            iteracion += 1
            for _, cabeza, cuerpo in self.producciones:
                cuerpo_prim = self.primeros_de_cadena(cuerpo, primeros)
                tamano_previo = len(primeros[cabeza])
                primeros[cabeza].update(cuerpo_prim)
                if len(primeros[cabeza]) > tamano_previo:
                    cambio = True

        return primeros

    def calcular_siguientes(
        self, primeros: Dict[str, Set[str]]
    ) -> Dict[str, Set[str]]:
        """
        Calcula de forma iterativa (punto fijo) los conjuntos de SIGUIENTES
        para cada símbolo no terminal de la gramática.
        """
        siguientes: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}
        # Regla de frontera: el símbolo de fin de cadena entra al axioma inicial
        siguientes[self.simbolo_inicial].add(FIN_CADENA)

        cambio = True
        while cambio:
            cambio = False
            for _, cabeza, cuerpo in self.producciones:
                for i, simbolo in enumerate(cuerpo):
                    if simbolo in self.no_terminales:
                        sufijo = cuerpo[i + 1 :]
                        primeros_sufijo = self.primeros_de_cadena(sufijo, primeros)

                        tamano_previo = len(siguientes[simbolo])

                        # Regla 1: Todo PRIM(sufijo) \ {ε} va a SIGUIENTES(simbolo)
                        siguientes[simbolo].update(primeros_sufijo - {EPSILON})

                        # Regla 2: Si el sufijo es anulable o no existe, hereda SIGUIENTES(cabeza)
                        if EPSILON in primeros_sufijo:
                            siguientes[simbolo].update(siguientes[cabeza])

                        if len(siguientes[simbolo]) > tamano_previo:
                            cambio = True

        return siguientes

    def calcular_prediccion(
        self, primeros: Dict[str, Set[str]], siguientes: Dict[str, Set[str]]
    ) -> Dict[int, Tuple[str, List[str], Set[str]]]:
        """
        Calcula los conjuntos de PREDICCIÓN para cada regla de producción:
        PRED(A -> α) = PRIM(α) si ε ∉ PRIM(α)
        PRED(A -> α) = (PRIM(α) \ {ε}) ∪ SIG(A) si ε ∈ PRIM(α)
        """
        prediccion: Dict[int, Tuple[str, List[str], Set[str]]] = {}

        for num_regla, cabeza, cuerpo in self.producciones:
            primeros_cuerpo = self.primeros_de_cadena(cuerpo, primeros)

            if EPSILON in primeros_cuerpo:
                conjunto_pred = (primeros_cuerpo - {EPSILON}) | siguientes[cabeza]
            else:
                conjunto_pred = set(primeros_cuerpo)

            prediccion[num_regla] = (cabeza, cuerpo, conjunto_pred)

        return prediccion

    def verificar_ll1(
        self, prediccion: Dict[int, Tuple[str, List[str], Set[str]]]
    ) -> Tuple[bool, List[str]]:
        """
        Determina si la gramática es LL(1) verificando que para todo no terminal,
        las reglas alternativas tengan conjuntos de predicción mutuamente disyuntos.
        """
        es_ll1 = True
        conflictos: List[str] = []

        # Agrupar reglas por no terminal
        reglas_por_nt: Dict[str, List[int]] = {nt: [] for nt in self.no_terminales}
        for num_regla, (cabeza, _, _) in prediccion.items():
            reglas_por_nt[cabeza].append(num_regla)

        for nt, lista_reglas in reglas_por_nt.items():
            n = len(lista_reglas)
            for i in range(n):
                for j in range(i + 1, n):
                    r1 = lista_reglas[i]
                    r2 = lista_reglas[j]
                    pred1 = prediccion[r1][2]
                    pred2 = prediccion[r2][2]
                    interseccion = pred1 & pred2
                    if interseccion:
                        es_ll1 = False
                        conflictos.append(
                            f"Conflicto en '{nt}': Regla {r1} y Regla {r2} "
                            f"comparten los terminales: {sorted(list(interseccion))}"
                        )

        return es_ll1, conflictos


def formatear_conjunto(conjunto: Set[str]) -> str:
    """Retorna una representación legible y ordenada de un conjunto."""
    elementos = sorted(list(conjunto))
    return "{" + ", ".join(elementos) + "}"


def main():
   
    print(" EJECUCIÓN DEL ANALIZADOR SINTÁCTICO - CÁLCULO DE CONJUNTOS")
    

    # Definición de la Gramática del Ejercicio 2
    no_terminales = ["S", "A", "B", "C", "D"]
    terminales = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
    axioma = "S"

    producciones = [
        (1, "S", ["A", "B", "uno"]),
        (2, "A", ["dos", "B"]),
        (3, "A", [EPSILON]),
        (4, "B", ["C", "D"]),
        (5, "B", ["tres"]),
        (6, "B", [EPSILON]),
        (7, "C", ["cuatro", "A", "B"]),
        (8, "C", ["cinco"]),
        (9, "D", ["seis"]),
        (10, "D", [EPSILON]),
    ]

    gramatica = GramaticaLL1(no_terminales, terminales, axioma, producciones)

    # 1. Cómputo de PRIMEROS
    primeros = gramatica.calcular_primeros()
    print("\n[+] CONJUNTOS DE PRIMEROS:")
    for nt in sorted(gramatica.no_terminales):
        print(f"    PRIM({nt}) = {formatear_conjunto(primeros[nt])}")

    # 2. Cómputo de SIGUIENTES
    siguientes = gramatica.calcular_siguientes(primeros)
    print("\n[+] CONJUNTOS DE SIGUIENTES:")
    for nt in sorted(gramatica.no_terminales):
        print(f"    SIG({nt}) = {formatear_conjunto(siguientes[nt])}")

    # 3. Cómputo de PREDICCIÓN
    predicciones = gramatica.calcular_prediccion(primeros, siguientes)
    print("\n[+] CONJUNTOS DE PREDICCIÓN:")
    for num_regla in sorted(predicciones.keys()):
        cabeza, cuerpo, p_set = predicciones[num_regla]
        cuerpo_str = " ".join(cuerpo)
        print(f"    R{num_regla:02d}: {cabeza} -> {cuerpo_str:<15} => PRED = {formatear_conjunto(p_set)}")

    # 4. Evaluación Determinista LL(1)
    es_ll1, conflictos = gramatica.verificar_ll1(predicciones)
    
    print(" EVALUACIÓN DE LA PROPIEDAD LL(1):")
    
    if es_ll1:
        print(" -> La gramática es estrictamente LL(1).")
    else:
        print(" -> La gramática NO es LL(1). Se encontraron las siguientes colisiones:")
        for c in conflictos:
            print(f"    * {c}")
    print("=" * 70)


if __name__ == "__main__":
    main()
