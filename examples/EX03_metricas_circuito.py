
"""
EX03 - Métricas de Circuitos Quânticos

Objetivos:
1. Construir circuitos com diferentes estruturas.
2. Utilizar qiskit_service para obter métricas.
3. Comparar quantidade de operações e profundidade.
4. Contabilizar portas de um e dois qubits.
5. Interpretar as diferenças entre as métricas.
6. Validar os resultados obtidos.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import obter_metricas


def construir_circuito_sequencial():
    """
    Constrói um circuito com quatro operações sequenciais
    aplicadas ao mesmo qubit.
    """

    circuito = QuantumCircuit(4)

    circuito.h(0)
    circuito.x(0)
    circuito.z(0)
    circuito.h(0)

    return circuito


def construir_circuito_paralelo():
    """
    Constrói um circuito com quatro operações independentes,
    cada uma aplicada a um qubit diferente.
    """

    circuito = QuantumCircuit(4)

    circuito.h(0)
    circuito.x(1)
    circuito.z(2)
    circuito.h(3)

    return circuito


def construir_circuito_misto():
    """
    Constrói um circuito com operações paralelas
    e operações de dois qubits.
    """

    circuito = QuantumCircuit(4)

    circuito.h(0)
    circuito.h(1)

    circuito.cx(0, 2)
    circuito.cx(1, 3)

    circuito.x(2)
    circuito.x(3)

    return circuito


def analisar_circuito(nome, circuito):
    """
    Utiliza obter_metricas do qiskit_service e complementa
    a análise com a contagem de portas por quantidade de qubits.
    """

    metricas = obter_metricas(circuito)

    portas_um_qubit = sum(
        instrucao.operation.num_qubits == 1
        for instrucao in circuito.data
    )

    portas_dois_qubits = sum(
        instrucao.operation.num_qubits == 2
        for instrucao in circuito.data
    )

    print(f"\n========== {nome} ==========")

    print("\nCircuito:")
    print(circuito.draw(output="text"))

    print("\nMétricas:")

    print(f"Quantidade de qubits: {metricas['qubits']}")
    print(f"Total de operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")
    print(f"Portas de um qubit: {portas_um_qubit}")
    print(f"Portas de dois qubits: {portas_dois_qubits}")

    print("\nOperações por tipo:")

    for operacao, quantidade in metricas["tipos_operacoes"].items():
        print(f"{operacao}: {quantidade}")

    return {
        "metricas": metricas,
        "portas_um_qubit": portas_um_qubit,
        "portas_dois_qubits": portas_dois_qubits
    }


def comparar_circuitos(metricas_sequencial, metricas_paralelo):
    """
    Compara dois circuitos com a mesma quantidade
    de operações, mas diferentes profundidades.
    """

    sequencial = metricas_sequencial["metricas"]
    paralelo = metricas_paralelo["metricas"]

    print("\n========== COMPARAÇÃO DOS CIRCUITOS ==========")

    print(
        f"Operações no circuito sequencial: "
        f"{sequencial['total_operacoes']}"
    )

    print(
        f"Operações no circuito paralelo: "
        f"{paralelo['total_operacoes']}"
    )

    print(
        f"Profundidade do circuito sequencial: "
        f"{sequencial['profundidade']}"
    )

    print(
        f"Profundidade do circuito paralelo: "
        f"{paralelo['profundidade']}"
    )

    print("\nInterpretação:")

    print("Os dois circuitos possuem a mesma quantidade de operações.")

    print("O circuito sequencial apresenta maior profundidade.")

    print(
        "Isso acontece porque suas operações dependem "
        "da execução das operações anteriores."
    )

    print(
        "No circuito paralelo, as portas atuam em qubits diferentes "
        "e podem ser executadas na mesma camada."
    )


def validar_resultados(sequencial, paralelo, misto):
    """
    Verifica se as métricas obtidas correspondem
    aos resultados esperados para cada circuito.
    """

    print("\n========== VALIDAÇÃO ==========")

    metricas_sequencial = sequencial["metricas"]
    metricas_paralelo = paralelo["metricas"]
    metricas_misto = misto["metricas"]

    assert metricas_sequencial["qubits"] == 4
    assert metricas_sequencial["total_operacoes"] == 4
    assert metricas_sequencial["profundidade"] == 4

    print("[OK] Métricas do circuito sequencial.")

    assert metricas_paralelo["qubits"] == 4
    assert metricas_paralelo["total_operacoes"] == 4
    assert metricas_paralelo["profundidade"] == 1

    print("[OK] Métricas do circuito paralelo.")

    assert metricas_misto["qubits"] == 4
    assert metricas_misto["total_operacoes"] == 6
    assert metricas_misto["profundidade"] == 3

    print("[OK] Métricas do circuito misto.")

    assert sequencial["portas_um_qubit"] == 4
    assert sequencial["portas_dois_qubits"] == 0

    assert paralelo["portas_um_qubit"] == 4
    assert paralelo["portas_dois_qubits"] == 0

    print("[OK] Contagem de portas dos circuitos sequencial e paralelo.")

    assert misto["portas_um_qubit"] == 4
    assert misto["portas_dois_qubits"] == 2

    print("[OK] Contagem de portas do circuito misto.")

    assert (
        metricas_sequencial["total_operacoes"]
        == metricas_paralelo["total_operacoes"]
    )

    assert (
        metricas_sequencial["profundidade"]
        > metricas_paralelo["profundidade"]
    )

    print("[OK] Diferença entre quantidade de operações e profundidade.")


def main():

    print("==============================================")
    print("       EX03 - MÉTRICAS DE CIRCUITOS")
    print("==============================================")

    sequencial = construir_circuito_sequencial()
    paralelo = construir_circuito_paralelo()
    misto = construir_circuito_misto()

    metricas_sequencial = analisar_circuito(
        "CIRCUITO SEQUENCIAL",
        sequencial
    )

    metricas_paralelo = analisar_circuito(
        "CIRCUITO PARALELO",
        paralelo
    )

    metricas_misto = analisar_circuito(
        "CIRCUITO MISTO",
        misto
    )

    comparar_circuitos(
        metricas_sequencial,
        metricas_paralelo
    )

    validar_resultados(
        metricas_sequencial,
        metricas_paralelo,
        metricas_misto
    )

    print("\n==============================================")
    print("           EXEMPLO CONCLUÍDO")
    print("==============================================")


if __name__ == "__main__":
    main()
