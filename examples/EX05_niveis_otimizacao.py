
"""
EX05 - Comparação dos níveis de otimização do Qiskit.

Compara os níveis 0, 1, 2 e 3 usando as funções
disponíveis em qiskit_service.py.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import obter_metricas, comparar_niveis


def construir_circuito():
    """Constrói um circuito de três qubits para comparação."""

    circuito = QuantumCircuit(3)

    circuito.h(0)
    circuito.ry(0.7, 1)
    circuito.rz(1.2, 2)

    circuito.cx(0, 1)
    circuito.cx(1, 2)

    circuito.h(2)
    circuito.cz(0, 2)

    circuito.ry(0.4, 0)
    circuito.rz(0.9, 1)

    return circuito


def exibir_metricas(titulo, metricas):
    """Exibe as métricas de um circuito."""

    print(f"\n{titulo}")
    print(f"Qubits: {metricas['qubits']}")
    print(f"Operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")
    print(f"Tipos de operações: {metricas['tipos_operacoes']}")


def main():
    circuito_original = construir_circuito()

    metricas_originais = obter_metricas(circuito_original)

    print("CIRCUITO ORIGINAL")
    exibir_metricas("Métricas originais:", metricas_originais)

    resultados = comparar_niveis(circuito_original)

    print("\nCOMPARAÇÃO DOS NÍVEIS DE OTIMIZAÇÃO")

    for nivel, resultado in resultados.items():
        metricas = resultado["metricas"]

        print(f"\nNível de otimização {nivel}")
        print(f"Operações: {metricas['total_operacoes']}")
        print(f"Profundidade: {metricas['profundidade']}")
        print(f"Tipos de operações: {metricas['tipos_operacoes']}")
        print(f"Status de equivalência: {resultado['status_verificacao']}")
        print(f"Equivalente: {resultado['equivalente']}")

        if resultado["motivo"]:
            print(f"Motivo: {resultado['motivo']}")

        if resultado["equivalente"] is True:
            print("Validação: circuito equivalente ao original.")
        elif resultado["equivalente"] is False:
            print("Validação: circuito não equivalente ao original.")
        else:
            print("Validação: não foi possível verificar a equivalência.")

    print("\nCIRCUITO ORIGINAL:")
    print(circuito_original.draw(output="text"))


if __name__ == "__main__":
    main()
