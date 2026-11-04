"""Prototipo inicial de analise e otimizacao de circuitos quanticos do GrowUp.

Este exemplo usa apenas o Qiskit SDK: nao executa circuitos em simuladores
ou hardware real e nao inclui integracao com o agente RAG.
"""

import json

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator


def main():
    # Criar circuito de dois qubits com operacoes redundantes.
    circuito = QuantumCircuit(2)

    circuito.x(0)
    circuito.x(0)  # Redundancia: X seguida de X

    circuito.h(0)
    circuito.h(0)  # Redundancia: H seguida de H

    circuito.h(0)
    circuito.cx(0, 1)
    circuito.cx(0, 1)  # Redundancia: duas CNOT consecutivas
    circuito.cx(0, 1)

    # Solicitar otimizacao ao transpilador do Qiskit.
    otimizado = transpile(
        circuito,
        optimization_level=3,
        seed_transpiler=42,
    )

    # Representacoes textuais para inspecao visual.
    print("CIRCUITO ORIGINAL:")
    print(circuito.draw())

    print("\nCIRCUITO OTIMIZADO:")
    print(otimizado.draw())

    # Metricas de comparacao.
    print("\nCOMPARACAO:")
    print("Operacoes originais:", circuito.size())
    print("Operacoes otimizadas:", otimizado.size())
    print("Profundidade original:", circuito.depth())
    print("Profundidade otimizada:", otimizado.depth())

    # Equivalencia unitaria, admitindo diferenca de fase global.
    equivalente = bool(
        Operator(circuito).equiv(Operator(otimizado))
    )
    print("Circuitos equivalentes:", equivalente)

    print("\n--- ANALISE DETALHADA ---")
    print("Operacoes originais:")
    print(dict(circuito.count_ops()))
    print("\nOperacoes otimizadas:")
    print(dict(otimizado.count_ops()))

    quantidade_original = circuito.size()
    reducao = (
        (quantidade_original - otimizado.size())
        / quantidade_original
        * 100
        if quantidade_original > 0
        else 0.0
    )

    print(f"\nReducao de operacoes: {reducao:.1f}%")
    print("Equivalencia preservada:", equivalente)

    # Estrutura reutilizavel no futuro pela API do GrowUp.
    analise = {
        "qubits": circuito.num_qubits,
        "portas_antes": circuito.size(),
        "portas_depois": otimizado.size(),
        "profundidade_antes": circuito.depth(),
        "profundidade_depois": otimizado.depth(),
        "reducao_percentual": round(reducao, 2),
        "equivalente": equivalente,
    }

    print("\nRESULTADO JSON:")
    print(json.dumps(analise, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
