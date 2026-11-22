
"""
EX04 - Identificação e Eliminação de Portas Redundantes

Objetivos:
1. Construir um circuito com operações redundantes.
2. Analisar as métricas do circuito original.
3. Comparar os quatro níveis de otimização.
4. Avaliar a proposta otimizada.
5. Verificar se a otimização preservou a equivalência.
6. Identificar possíveis reduções de operações e profundidade.
"""

import sys
from pathlib import Path

from qiskit import QuantumCircuit

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from qiskit_service import (
    obter_metricas,
    comparar_niveis,
    otimizar_circuito,
    avaliar_proposta_ia
)


def construir_circuito():
    """
    Constrói um circuito com pares de operações redundantes.

    H seguido de H retorna o qubit ao estado original.
    X seguido de X também retorna o qubit ao estado original.
    Duas portas CX consecutivas com os mesmos qubits
    anulam seus efeitos.
    """

    circuito = QuantumCircuit(2)

    circuito.h(0)
    circuito.h(0)

    circuito.x(1)
    circuito.x(1)

    circuito.cx(0, 1)
    circuito.cx(0, 1)

    return circuito


def analisar_circuito_original(circuito):
    """
    Obtém as métricas do circuito original utilizando
    a função centralizada do qiskit_service.
    """

    metricas = obter_metricas(circuito)

    print("\n========== CIRCUITO ORIGINAL ==========")
    print(circuito.draw(output="text"))

    print("\nMétricas originais:")
    print(f"Qubits: {metricas['qubits']}")
    print(f"Operações: {metricas['total_operacoes']}")
    print(f"Profundidade: {metricas['profundidade']}")

    print("\nOperações por tipo:")

    for operacao, quantidade in metricas["tipos_operacoes"].items():
        print(f"{operacao}: {quantidade}")

    return metricas


def comparar_otimizacoes(circuito):
    """
    Utiliza comparar_niveis para avaliar o circuito
    nos níveis de otimização de 0 a 3.
    """

    resultados = comparar_niveis(circuito)

    print("\n========== COMPARAÇÃO DOS NÍVEIS ==========")

    for nivel, resultado in resultados.items():

        metricas = resultado["metricas"]

        print(f"\nNível de otimização: {nivel}")
        print(f"Operações: {metricas['total_operacoes']}")
        print(f"Profundidade: {metricas['profundidade']}")
        print(f"Equivalência: {resultado['status_verificacao']}")

        if resultado["motivo"] is not None:
            print(f"Motivo: {resultado['motivo']}")

    return resultados


def avaliar_otimizacao(original):
    """
    Executa a otimização no nível 3 e utiliza
    avaliar_proposta_ia para verificar a proposta.
    """

    otimizado = otimizar_circuito(
        original,
        nivel_otimizacao=3
    )

    avaliacao = avaliar_proposta_ia(
        original,
        otimizado
    )

    print("\n========== CIRCUITO OTIMIZADO ==========")
    print(otimizado.draw(output="text"))

    print("\n========== AVALIAÇÃO DA PROPOSTA ==========")

    print(
        f"Operações originais: "
        f"{avaliacao['original']['total_operacoes']}"
    )

    print(
        f"Operações propostas: "
        f"{avaliacao['proposta']['total_operacoes']}"
    )

    print(
        f"Profundidade original: "
        f"{avaliacao['original']['profundidade']}"
    )

    print(
        f"Profundidade proposta: "
        f"{avaliacao['proposta']['profundidade']}"
    )

    print(f"Equivalência: {avaliacao['status_verificacao']}")

    print(
        f"Diferença de operações: "
        f"{avaliacao['diferenca_operacoes']}"
    )

    print(
        f"Diferença de profundidade: "
        f"{avaliacao['diferenca_profundidade']}"
    )

    print(
        f"Reduziu operações: "
        f"{avaliacao['reduziu_operacoes']}"
    )

    print(
        f"Reduziu profundidade: "
        f"{avaliacao['reduziu_profundidade']}"
    )

    if avaliacao["motivo"] is not None:
        print(f"Motivo da verificação: {avaliacao['motivo']}")

    return otimizado, avaliacao


def validar_resultados(resultados, avaliacao):
    """
    Verifica se os níveis de otimização preservaram
    a equivalência e se a proposta final foi validada.
    """

    print("\n========== VALIDAÇÃO ==========")

    assert len(resultados) == 4

    print("[OK] Foram avaliados os quatro níveis de otimização.")

    for nivel, resultado in resultados.items():
        assert resultado["equivalente"] is True, (
            f"O nível {nivel} não confirmou a equivalência."
        )

    print("[OK] Todos os níveis preservaram a equivalência.")

    assert avaliacao["equivalente"] is True

    print("[OK] A proposta final é equivalente ao circuito original.")

    assert avaliacao["reduziu_operacoes"] is not None
    assert avaliacao["reduziu_profundidade"] is not None

    print("[OK] As reduções foram avaliadas após a verificação de equivalência.")


def main():

    print("==============================================")
    print("       EX04 - PORTAS REDUNDANTES")
    print("==============================================")

    circuito = construir_circuito()

    analisar_circuito_original(circuito)

    resultados = comparar_otimizacoes(circuito)

    otimizado, avaliacao = avaliar_otimizacao(circuito)

    validar_resultados(
        resultados,
        avaliacao
    )

    print("\n==============================================")
    print("           EXEMPLO CONCLUÍDO")
    print("==============================================")


if __name__ == "__main__":
    main()
