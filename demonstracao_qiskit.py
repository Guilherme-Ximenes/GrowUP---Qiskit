import json

from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap

from qiskit_service import (obter_metricas, otimizar_circuito, verificar_equivalencia, comparar_niveis, otimizar_para_hardware, analisar_adaptacao_hardware, avaliar_proposta_ia)


def mostrar_resultado(dados):
    """
    Exibe um dicionário em formato JSON.
    """
    print(json.dumps(dados, indent=4, ensure_ascii=False))


def main():

    print("=" * 55)
    print("GROWUP - DEMONSTRAÇÃO DO MÓDULO QISKIT")
    print("=" * 55)

    # === 1. OTIMIZAÇÃO BÁSICA ===

    print("\n=== 1. OTIMIZAÇÃO BÁSICA ===")

    original = QuantumCircuit(2)

    # Operações redundantes
    original.x(0)
    original.x(0)

    original.h(0)
    original.h(0)

    original.h(0)

    original.cx(0, 1)
    original.cx(0, 1)
    original.cx(0, 1)

    # Otimização genérica
    otimizado = otimizar_circuito(original)

    print("\nCircuito original:")
    print(original.draw())

    print("\nCircuito otimizado:")
    print(otimizado.draw())

    print("\nMétricas originais:")
    mostrar_resultado(obter_metricas(original))

    print("\nMétricas otimizadas:")
    mostrar_resultado(obter_metricas(otimizado))

    print("\nEquivalência:")
    print(verificar_equivalencia(original, otimizado))

    # Comparação dos níveis de otimização
    print("\nComparação dos níveis 0 a 3:")

    resultados_niveis = comparar_niveis(original)

    for nivel, dados in resultados_niveis.items():
        metricas = dados["metricas"]

        print(
            f"Nível {nivel}: "
            f"{metricas['total_operacoes']} operações | "
            f"Profundidade {metricas['profundidade']} | "
            f"Equivalente: {dados['equivalente']}"
        )

    # === 2. OTIMIZAÇÃO PARA HARDWARE ===

    print("\n=== 2. ADAPTAÇÃO AO HARDWARE ===")

    circuito_hardware = QuantumCircuit(3)

    circuito_hardware.h(0)
    circuito_hardware.cx(0, 2)
    circuito_hardware.cx(0, 1)

    # Hardware hipotético com 3 qubits em linha
    conectividade = CouplingMap.from_line(3)

    # Portas permitidas
    portas_nativas = ["rz", "sx", "x", "cx"]

    # Adaptar o circuito
    adaptado = otimizar_para_hardware(circuito_hardware,conectividade,portas_nativas=portas_nativas)

    print("\nCircuito original:")
    print(circuito_hardware.draw())

    print("\nCircuito adaptado:")
    print(adaptado.draw())

    # Análise da adaptação
    analise_hardware = analisar_adaptacao_hardware(circuito_hardware,adaptado,portas_nativas)

    print("\nAnálise do hardware:")
    mostrar_resultado(analise_hardware)

    print("\nSWAPs inseridas:")
    print(adaptado.count_ops().get("swap", 0))

    print("\nMapeamento inicial:")
    print(adaptado.layout.initial_index_layout())

    # === 3. AVALIAÇÃO DE PROPOSTAS DA IA ===

    print("\n=== 3. AVALIAÇÃO DE PROPOSTAS DA IA ===")

    # Simulação de proposta correta:
    # circuito obtido pelo próprio transpilador
    proposta_correta = otimizado

    # Simulação de proposta incorreta:
    # remove a CNOT necessária
    proposta_incorreta = QuantumCircuit(2)
    proposta_incorreta.h(0)

    print("\nProposta correta:")
    resultado_correto = avaliar_proposta_ia(original,proposta_correta)
    mostrar_resultado(resultado_correto)

    print("\nProposta incorreta:")
    resultado_incorreto = avaliar_proposta_ia(original,proposta_incorreta)

    mostrar_resultado(resultado_incorreto)

    # === FINALIZAÇÃO ===
    
    print("\n" + "=" * 55)
    print("DEMONSTRAÇÃO FINALIZADA")
    print("=" * 55)

if __name__ == "__main__":
    main()