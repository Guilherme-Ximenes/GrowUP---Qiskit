
"""
EX02 - Circuito de Três Qubits

Objetivos:
1. Construir um circuito de três qubits.
2. Utilizar qiskit_service para obter métricas.
3. Interpretar o papel de cada qubit.
4. Analisar o estado quântico final.
5. Calcular as probabilidades teóricas.
6. Simular medições com StatevectorSampler.
7. Validar os resultados.

Circuito:
- q0 recebe uma porta X.
- q1 recebe uma porta H.
- q1 controla uma porta CX aplicada em q2.

Dependências:
- qiskit
- qiskit_service.py
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

# Localiza a raiz do projeto para importar qiskit_service.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import obter_metricas

SHOTS = 1024
SEED = 42


def construir_circuito():
    """
    Constrói um circuito de três qubits.

    q0:
        Recebe X e passa de |0> para |1>.

    q1:
        Recebe H e entra em superposição.

    q2:
        Recebe CX controlada por q1.
    """

    circuito = QuantumCircuit(3)

    circuito.x(0)
    circuito.h(1)
    circuito.cx(1, 2)

    return circuito

def analisar_metricas(circuito):
    """
    Utiliza obter_metricas do qiskit_service
    para analisar a estrutura do circuito.
    """

    metricas = obter_metricas(circuito)

    print("\n========== MÉTRICAS DO CIRCUITO ==========")

    print(f"Quantidade de qubits: {metricas['qubits']}")
    print(f"Total de operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")

    print("\nOperações por tipo:")

    for operacao, quantidade in metricas["tipos_operacoes"].items():
        print(f"{operacao}: {quantidade}")

    return metricas

def interpretar_circuito():
    """
    Explica o papel de cada qubit e operação.
    """

    print("\n========== INTERPRETAÇÃO DO CIRCUITO ==========")

    print("q0: recebe X e passa de |0> para |1>.")
    print("q1: recebe H e entra em superposição.")
    print("q2: recebe CX controlada por q1.")

    print("\nComportamento esperado:")
    print("- q0 permanece em |1>.")
    print("- q1 pode apresentar resultado 0 ou 1.")
    print("- q2 acompanha o valor de q1.")
    print("- q1 e q2 apresentam resultados correlacionados.")

def analisar_estado(circuito):
    """
    Calcula o estado quântico antes das medições.
    """

    estado = Statevector.from_instruction(circuito)

    probabilidades = estado.probabilities_dict()

    print("\n========== ESTADO QUÂNTICO ==========")
    print(estado.draw(output="text"))

    print("\n========== PROBABILIDADES TEÓRICAS ==========")

    for resultado, probabilidade in sorted(probabilidades.items()):

        print(
            f"{resultado}: {probabilidade:.4f} "
            f"({probabilidade * 100:.2f}%)"
        )

    return estado, probabilidades

def interpretar_resultados(probabilidades):
    """
    Interpreta os resultados considerando a ordem dos bits
    utilizada pelo Qiskit: q2 q1 q0.

    O bit mais à direita representa q0.
    O bit central representa q1.
    O bit mais à esquerda representa q2.
    """

    print("\n========== INTERPRETAÇÃO DOS QUBITS ==========")

    for resultado, probabilidade in sorted(probabilidades.items()):

        q2 = resultado[0]
        q1 = resultado[1]
        q0 = resultado[2]

        print(
            f"Estado {resultado}: "
            f"q0={q0}, q1={q1}, q2={q2} "
            f"| Probabilidade={probabilidade * 100:.2f}%"
        )

    print("\nConclusões:")

    print("- q0 permanece em |1> em todos os resultados.")
    print("- q1 pode resultar em 0 ou 1.")
    print("- q2 apresenta o mesmo valor de q1.")
    print("- Os únicos resultados possíveis são 001 e 111.")

def executar_medicoes(circuito):
    """
    Executa medições utilizando StatevectorSampler.

    O circuito original é preservado sem medições.
    """

    circuito_medicao = circuito.copy()

    circuito_medicao.measure_all()

    sampler = StatevectorSampler(
        default_shots=SHOTS,
        seed=SEED
    )

    resultado = sampler.run(
        [circuito_medicao],
        shots=SHOTS
    ).result()

    contagens = resultado[0].data.meas.get_counts()

    print("\n========== RESULTADOS DAS MEDIÇÕES ==========")
    print(f"Total de shots: {SHOTS}")

    for estado, quantidade in sorted(contagens.items()):

        percentual = quantidade / SHOTS * 100

        print(
            f"{estado}: {quantidade} ocorrências "
            f"({percentual:.2f}%)"
        )

    return contagens

def validar_resultados(metricas, probabilidades, contagens):
    """
    Valida as métricas, os estados teóricos
    e os resultados das medições.
    """

    print("\n========== VALIDAÇÃO ==========")

    # Métricas do qiskit_service
    assert metricas["qubits"] == 3
    assert metricas["total_operacoes"] == 3
    assert metricas["profundidade"] == 2

    print("[OK] Métricas obtidas pelo qiskit_service.")

    # Estados teóricos esperados
    assert len(probabilidades) == 2

    assert abs(probabilidades.get("001", 0) - 0.5) < 1e-10
    assert abs(probabilidades.get("111", 0) - 0.5) < 1e-10

    print("[OK] Os estados teóricos são 001 e 111, com 50% cada.")

    # q0 deve permanecer em 1
    assert all(
        resultado[-1] == "1"
        for resultado in probabilidades
    )

    print("[OK] q0 permanece em |1>.")

    # q1 e q2 devem apresentar valores iguais
    assert all(
        resultado[0] == resultado[1]
        for resultado in probabilidades
    )

    print("[OK] q1 e q2 apresentam resultados correlacionados.")

    # Validação das medições
    assert sum(contagens.values()) == SHOTS

    assert all(
        resultado in ("001", "111")
        for resultado in contagens
    )

    print("[OK] Todas as medições produziram estados esperados.")

def main():

    print("==============================================")
    print("      EX02 - CIRCUITO DE TRÊS QUBITS")
    print("==============================================")

    circuito = construir_circuito()

    print("\n========== CIRCUITO ==========")
    print(circuito.draw(output="text"))

    metricas = analisar_metricas(circuito)

    interpretar_circuito()

    estado, probabilidades = analisar_estado(circuito)

    interpretar_resultados(probabilidades)

    contagens = executar_medicoes(circuito)

    validar_resultados(
        metricas,
        probabilidades,
        contagens
    )

    print("\n==============================================")
    print("           EXEMPLO CONCLUÍDO")
    print("==============================================")


if __name__ == "__main__":
    main()
