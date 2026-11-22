
"""
EX08 - Equivalência e validação de circuitos quânticos.

Compara circuitos com estruturas diferentes para verificar
se representam a mesma operação quântica.
Também testa uma proposta não equivalente.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import (
    obter_metricas,
    verificar_equivalencia,
    avaliar_proposta_ia
)


def construir_circuito_original():
    """Constrói o circuito original usando uma porta CX."""

    circuito = QuantumCircuit(2)

    circuito.h(0)
    circuito.cx(0, 1)

    return circuito


def construir_circuito_equivalente():
    """
    Reconstrói a operação CX utilizando H, CZ e H.

    A identidade utilizada é:
    CX = H no alvo + CZ + H no alvo.
    """

    circuito = QuantumCircuit(2)

    circuito.h(0)
    circuito.h(1)
    circuito.cz(0, 1)
    circuito.h(1)

    return circuito


def construir_circuito_nao_equivalente():
    """Constrói uma proposta incorreta, sem o último H."""

    circuito = QuantumCircuit(2)

    circuito.h(0)
    circuito.h(1)
    circuito.cz(0, 1)

    return circuito


def exibir_metricas(titulo, circuito):
    """Exibe as métricas e a representação do circuito."""

    metricas = obter_metricas(circuito)

    print(f"\n{titulo}")
    print(f"Qubits: {metricas['qubits']}")
    print(f"Operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")
    print(f"Tipos de operações: {metricas['tipos_operacoes']}")

    print(circuito.draw(output="text"))


def exibir_avaliacao(titulo, resultado):
    """Exibe os resultados da avaliação de uma proposta."""

    print(f"\n{titulo}")

    print(f"Equivalente: {resultado['equivalente']}")
    print(f"Status: {resultado['status_verificacao']}")

    print(
        f"Diferença de operações: "
        f"{resultado['diferenca_operacoes']}"
    )

    print(
        f"Diferença de profundidade: "
        f"{resultado['diferenca_profundidade']}"
    )

    print(
        f"Reduziu operações: "
        f"{resultado['reduziu_operacoes']}"
    )

    print(
        f"Reduziu profundidade: "
        f"{resultado['reduziu_profundidade']}"
    )

    if resultado["motivo"]:
        print(f"Motivo: {resultado['motivo']}")


def main():
    original = construir_circuito_original()
    proposta_equivalente = construir_circuito_equivalente()
    proposta_incorreta = construir_circuito_nao_equivalente()

    exibir_metricas("CIRCUITO ORIGINAL", original)

    exibir_metricas(
        "PROPOSTA EQUIVALENTE",
        proposta_equivalente
    )

    exibir_metricas(
        "PROPOSTA NÃO EQUIVALENTE",
        proposta_incorreta
    )

    equivalencia = verificar_equivalencia(
        original,
        proposta_equivalente
    )

    print("\nVERIFICAÇÃO DIRETA")
    print(
        "Original e proposta equivalente:",
        equivalencia
    )

    resultado_equivalente = avaliar_proposta_ia(
        original,
        proposta_equivalente
    )

    exibir_avaliacao(
        "AVALIAÇÃO DA PROPOSTA EQUIVALENTE",
        resultado_equivalente
    )

    resultado_incorreto = avaliar_proposta_ia(
        original,
        proposta_incorreta
    )

    exibir_avaliacao(
        "AVALIAÇÃO DA PROPOSTA NÃO EQUIVALENTE",
        resultado_incorreto
    )


if __name__ == "__main__":
    main()
