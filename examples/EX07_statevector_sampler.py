
"""
EX07 - Simulação e amostragem de estados quânticos.

Compara as probabilidades teóricas de um circuito com
os resultados obtidos por medições usando StatevectorSampler.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import obter_metricas


def construir_circuito():
    """Constrói um circuito com quatro resultados possíveis."""

    circuito = QuantumCircuit(3)

    circuito.h(0)
    circuito.cx(0, 1)
    circuito.h(2)

    return circuito


def exibir_probabilidades(probabilidades):
    """Exibe as probabilidades teóricas de cada estado."""

    print("\nPROBABILIDADES TEÓRICAS")

    for estado, probabilidade in sorted(probabilidades.items()):
        print(f"|{estado}>: {probabilidade * 100:.2f}%")


def exibir_contagens(contagens, total_shots):
    """Exibe as contagens e frequências das medições."""

    print("\nRESULTADOS DAS MEDIÇÕES")

    for estado, quantidade in sorted(contagens.items()):
        frequencia = quantidade / total_shots

        print(
            f"|{estado}>: {quantidade} ocorrências "
            f"({frequencia * 100:.2f}%)"
        )


def main():
    circuito = construir_circuito()

    metricas = obter_metricas(circuito)

    print("MÉTRICAS DO CIRCUITO")
    print(f"Qubits: {metricas['qubits']}")
    print(f"Operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")

    estado = Statevector.from_instruction(circuito)

    probabilidades = estado.probabilities_dict()

    exibir_probabilidades(probabilidades)

    circuito_medicao = circuito.copy()
    circuito_medicao.measure_all()

    total_shots = 1024

    sampler = StatevectorSampler(
        default_shots=total_shots,
        seed=42
    )

    resultado = sampler.run(
        [circuito_medicao]
    ).result()

    contagens = resultado[0].data.meas.get_counts()

    exibir_contagens(contagens, total_shots)

    print("\nCOMPARAÇÃO DOS RESULTADOS")

    for estado, probabilidade in sorted(probabilidades.items()):
        frequencia = contagens.get(estado, 0) / total_shots

        diferenca = abs(probabilidade - frequencia)

        print(
            f"|{estado}> | "
            f"Teórico: {probabilidade * 100:.2f}% | "
            f"Simulado: {frequencia * 100:.2f}% | "
            f"Diferença: {diferenca * 100:.2f} pontos percentuais"
        )

    print("\nCIRCUITO:")
    print(circuito.draw(output="text"))


if __name__ == "__main__":
    main()
