
"""
EX06 - Adaptação de circuitos à conectividade de hardware.

Demonstra como o Qiskit adapta operações entre qubits
que não possuem conexão física direta.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import (
    obter_metricas,
    otimizar_para_hardware,
    analisar_adaptacao_hardware
)


def construir_circuito():
    """Constrói um circuito com interação entre qubits distantes."""

    circuito = QuantumCircuit(4)

    circuito.h(0)
    circuito.h(3)

    circuito.cx(0, 3)

    circuito.cx(1, 2)
    circuito.cx(0, 2)

    circuito.h(1)

    return circuito


def exibir_metricas(titulo, metricas):
    """Exibe as métricas do circuito."""

    print(f"\n{titulo}")
    print(f"Qubits: {metricas['qubits']}")
    print(f"Operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")
    print(f"Tipos de operações: {metricas['tipos_operacoes']}")


def main():
    circuito_original = construir_circuito()

    conectividade = CouplingMap(
        couplinglist=[
            (0, 1),
            (1, 2),
            (2, 3)
        ]
    )

    portas_nativas = ["rz", "sx", "x", "cx"]

    print("ARQUITETURA DE HARDWARE")
    print("Conectividade linear: 0 -- 1 -- 2 -- 3")

    print("\nConexões disponíveis:")
    print(conectividade.get_edges())

    metricas_originais = obter_metricas(circuito_original)

    exibir_metricas(
        "CIRCUITO ORIGINAL",
        metricas_originais
    )

    print("\nAdaptando circuito ao hardware...")

    circuito_adaptado = otimizar_para_hardware(
        circuito=circuito_original,
        conectividade=conectividade,
        layout_inicial=[0, 1, 2, 3],
        nivel_otimizacao=0,
        portas_nativas=portas_nativas
    )

    resultado = analisar_adaptacao_hardware(
        original=circuito_original,
        adaptado=circuito_adaptado,
        portas_nativas=portas_nativas
    )

    exibir_metricas(
        "CIRCUITO ADAPTADO",
        resultado["adaptado"]
    )

    print("\nANÁLISE DA ADAPTAÇÃO")
    print(
        f"Diferença de operações: "
        f"{resultado['diferenca_operacoes']}"
    )
    print(
        f"Diferença de profundidade: "
        f"{resultado['diferenca_profundidade']}"
    )
    print(f"Equivalente: {resultado['equivalente']}")
    print(f"Status: {resultado['status_verificacao']}")
    print(
        f"Somente portas permitidas: "
        f"{resultado['somente_portas_permitidas']}"
    )

    if resultado["motivo"]:
        print(f"Motivo: {resultado['motivo']}")

    print("\nCIRCUITO ORIGINAL:")
    print(circuito_original.draw(output="text"))

    print("\nCIRCUITO ADAPTADO:")
    print(circuito_adaptado.draw(output="text"))

    print("\nOPERAÇÕES SWAP INSERIDAS:")
    print(circuito_adaptado.count_ops().get("swap", 0))


if __name__ == "__main__":
    main()
