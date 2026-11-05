from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
from qiskit.transpiler import CouplingMap
from qiskit.exceptions import QiskitError

def obter_metricas(circuito: QuantumCircuit):
    """
    Analisa um circuito quântico e retorna
    suas principais métricas.
    """
    metricas = {
        "qubits": circuito.num_qubits,
        "total_operacoes": circuito.size(),
        "profundidade": circuito.depth(),
        "tipos_operacoes": dict(circuito.count_ops())  
    }
    return metricas

def otimizar_circuito(circuito:QuantumCircuit, nivel_otimizacao:int=3):
    '''
    Recebe um circuito quântico junto com nível
    de otimização, sendo o padrão 3, e faz o processo
    com transpile.
    '''
    if nivel_otimizacao not in (0, 1, 2, 3):
        raise ValueError("Nível de otimização deve ser 0, 1, 2 ou 3.")

    circuito_otimizado = transpile(
    circuito, 
    optimization_level=nivel_otimizacao, 
    seed_transpiler=42
    )
    return circuito_otimizado

def otimizar_para_hardware(circuito: QuantumCircuit, conectividade: CouplingMap, layout_inicial=None, nivel_otimizacao:int=0, portas_nativas: list[str] | None = None):
    """
    Adapta um circuito quântico às restrições
    de conectividade e portas nativas do hardware.
    """
    if nivel_otimizacao not in (0, 1, 2, 3):
        raise ValueError("Nível de otimização deve ser 0, 1, 2 ou 3.")

    otimizado = transpile(
        circuito,
        coupling_map=conectividade,
        basis_gates=portas_nativas,
        initial_layout=layout_inicial,
        layout_method = "sabre" if layout_inicial is None else None,
        routing_method= "basic",
        optimization_level=nivel_otimizacao,
        seed_transpiler=42
    )
    return otimizado

def verificar_equivalencia(original: QuantumCircuit, otimizado: QuantumCircuit):
    """
    Verifica equivalência de circuitos unitários,
    considerando os metadados de layout.

    Gera ValueError caso a comparação não
    possa ser realizada.
    """
    if original.num_qubits != otimizado.num_qubits:
        return False
    
    try:
        operador_original = Operator.from_circuit(original)
        operador_otimizado = Operator.from_circuit(otimizado)

        return bool(
            operador_original.equiv(operador_otimizado)
        )

    except QiskitError as erro:
        raise ValueError(
            "Não foi possível verificar equivalência pelo método de operadores unitários."
        ) from erro

def comparar_niveis(circuito: QuantumCircuit):
    """
    Compara o circuito original com suas versões
    otimizadas em diferentes níveis de otimização.
    """
    resultados = {}
    nivel = 0

    while nivel <= 3:
        otimizado = otimizar_circuito(circuito, nivel)

        resultados[nivel] = {
            "metricas": obter_metricas(otimizado),
            "equivalente": verificar_equivalencia(circuito, otimizado)
        }
        nivel += 1
        
    return resultados   

def analisar_adaptacao_hardware(original: QuantumCircuit, adaptado: QuantumCircuit, portas_nativas: list[str] | None = None):
    """
    Compara um circuito original com sua versão
    adaptada ao hardware.
    """

    # Obter métricas
    metricas_originais = obter_metricas(original)
    metricas_adaptadas = obter_metricas(adaptado)

    # Calcular diferenças
    diferenca_operacoes = (
        metricas_adaptadas["total_operacoes"]
        - metricas_originais["total_operacoes"]
    )

    diferenca_profundidade = (
        metricas_adaptadas["profundidade"]
        - metricas_originais["profundidade"]
    )

    # Verificar equivalência
    motivo = None

    try:
        equivalente = verificar_equivalencia(
            original, adaptado
        )

        if equivalente:
            status = "equivalente"
        else:
            status = "nao_equivalente"

    except ValueError as erro:
        equivalente = None
        status = "nao_verificado"
        motivo = str(erro)

    # Verificar portas nativas
    compativel_portas = None

    if portas_nativas is not None:
        compativel_portas = set(adaptado.count_ops()).issubset(set(portas_nativas))

    resultados = {
        "original": metricas_originais,
        "adaptado": metricas_adaptadas,
        "diferenca_operacoes": diferenca_operacoes,
        "diferenca_profundidade": diferenca_profundidade,
        "equivalente": equivalente,
        "status_verificacao": status,
        "motivo": motivo,
        "somente_portas_permitidas": compativel_portas
    }

    return resultados

def avaliar_proposta_ia(original: QuantumCircuit, proposta: QuantumCircuit):
    """
    Avalia uma proposta de otimização quântica,
    considerando métricas e equivalência.
    """

    metricas_original = obter_metricas(original)
    metricas_proposta = obter_metricas(proposta)

    diferenca_operacoes = (
        metricas_proposta["total_operacoes"]
        - metricas_original["total_operacoes"]
    )

    diferenca_profundidade = (
        metricas_proposta["profundidade"]
        - metricas_original["profundidade"]
    )

    # Tentar verificar equivalência
    motivo = None

    try:
        equivalente = verificar_equivalencia(
            original, proposta
        )

        if equivalente:
            status = "equivalente"
        else:
            status = "nao_equivalente"

    except ValueError as erro:
        equivalente = None
        status = "nao_verificado"
        motivo = str(erro)

    # Avaliar reduções apenas se houve verificação
    if equivalente is None:
        reduziu_operacoes = None
        reduziu_profundidade = None
    else:
        reduziu_operacoes = (
            equivalente and diferenca_operacoes < 0
        )

        reduziu_profundidade = (
            equivalente and diferenca_profundidade < 0
        )

    resultados = {
        "original": metricas_original,
        "proposta": metricas_proposta,
        "equivalente": equivalente,
        "status_verificacao": status,
        "motivo": motivo,
        "diferenca_operacoes": diferenca_operacoes,
        "diferenca_profundidade": diferenca_profundidade,
        "reduziu_operacoes": reduziu_operacoes,
        "reduziu_profundidade": reduziu_profundidade
    }

    return resultados