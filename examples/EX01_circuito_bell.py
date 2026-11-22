
"""
EX01 - Circuito de Bell

Objetivos:
1. Construir um circuito de Bell.
2. Utilizar qiskit_service para obter métricas.
3. Analisar o estado quântico antes das medições.
4. Calcular as probabilidades teóricas.
5. Analisar o emaranhamento.
6. Simular medições com StatevectorSampler.
7. Validar os resultados obtidos.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.primitives import StatevectorSampler

SHOTS = 1024
SEED = 42

# Adiciona a raiz do projeto ao caminho de importação.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import obter_metricas

def construir_circuito_bell():
    """
    Constrói o estado de Bell |Φ+>.

    q0 recebe uma porta Hadamard.
    q0 controla uma porta CX aplicada em q1.
    """

    circuito = QuantumCircuit(2)

    circuito.h(0)
    circuito.cx(0, 1)

    return circuito

def analisar_metricas(circuito):
    """
    Utiliza a função obter_metricas do qiskit_service
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

def analisar_estado(circuito):
    """
    Calcula o estado final utilizando Statevector.

    A análise é realizada antes das medições.
    """

    estado = Statevector.from_instruction(circuito)

    probabilidades = estado.probabilities_dict()

    print("\n========== ESTADO QUÂNTICO ==========")
    print(estado.draw(output="text"))

    print("\n========== PROBABILIDADES TEÓRICAS ==========")

    for resultado, probabilidade in probabilidades.items():

        print(
            f"{resultado}: {probabilidade:.4f} "
            f"({probabilidade * 100:.2f}%)"
        )

    return estado, probabilidades

def analisar_emaranhamento(estado):
    """
    Calcula a pureza do estado reduzido de um dos qubits.

    Para o estado de Bell, a pureza reduzida esperada é 0.5,
    indicando emaranhamento máximo.
    """

    estado_reduzido = partial_trace(estado, [1])

    pureza = estado_reduzido.purity()

    print("\n========== ANÁLISE DO EMARANHAMENTO ==========")
    print(f"Pureza do estado reduzido: {pureza:.4f}")

    if abs(pureza - 0.5) < 1e-10:
        print("Resultado: estado com emaranhamento máximo.")
    else:
        print("Resultado: pureza diferente da esperada.")

    return pureza

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

def validar_resultados(metricas, probabilidades, pureza, contagens):
    """
    Verifica se as métricas, probabilidades e medições
    correspondem ao comportamento esperado.
    """

    print("\n========== VALIDAÇÃO ==========")

    # Métricas obtidas pelo serviço
    assert metricas["qubits"] == 2
    assert metricas["total_operacoes"] == 2
    assert metricas["profundidade"] == 2

    print("[OK] Métricas obtidas pelo qiskit_service.")

    # Probabilidades teóricas
    assert abs(probabilidades.get("00", 0) - 0.5) < 1e-10
    assert abs(probabilidades.get("11", 0) - 0.5) < 1e-10

    assert len(probabilidades) == 2

    print("[OK] Probabilidades teóricas de 00 e 11 são de 50%.")

    # Emaranhamento
    assert abs(pureza - 0.5) < 1e-10

    print("[OK] Pureza reduzida igual a 0.5.")

    # Resultados das medições
    assert sum(contagens.values()) == SHOTS

    assert all(
        estado in ("00", "11")
        for estado in contagens
    )

    print("[OK] Todas as medições produziram 00 ou 11.")

def main():

    print("========================================")
    print("       EX01 - CIRCUITO DE BELL")
    print("========================================")

    circuito = construir_circuito_bell()

    print("\n========== CIRCUITO ==========")
    print(circuito.draw(output="text"))

    metricas = analisar_metricas(circuito)

    estado, probabilidades = analisar_estado(circuito)

    pureza = analisar_emaranhamento(estado)

    contagens = executar_medicoes(circuito)

    validar_resultados(
        metricas,
        probabilidades,
        pureza,
        contagens
    )

    print("\n========================================")
    print("          EXEMPLO CONCLUÍDO")
    print("========================================")


if __name__ == "__main__":
    main()
