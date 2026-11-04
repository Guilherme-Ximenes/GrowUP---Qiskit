from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
from qiskit.transpiler import CouplingMap

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
    Verifica se dois circuitos realizam
    transformações quânticas equivalentes 
    até uma fase global.
    """
    if original.num_qubits != otimizado.num_qubits:
        return False
    
    return bool(Operator.from_circuit(original).equiv(Operator.from_circuit(otimizado)))

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
    Compara as métricas de um circuito original
    com sua versão adaptada ao hardware.

    Considera circuitos unitários sem medições.
    """
    metricas_originais = obter_metricas(original)
    metricas_adaptadas = obter_metricas(adaptado)

    diferenca_portas = (
        metricas_adaptadas["total_operacoes"]
        - metricas_originais["total_operacoes"]
    )
    
    diferenca_profundidade = (
        metricas_adaptadas["profundidade"]
        - metricas_originais["profundidade"]
    )

    equivalencia = verificar_equivalencia(original, adaptado)

    compativel_portas = None

    if portas_nativas is not None:
        compativel_portas = set(adaptado.count_ops()).issubset(set(portas_nativas))

    resultados = {
        "original": metricas_originais,
        "adaptado": metricas_adaptadas,
        "diferenca_portas": diferenca_portas,
        "diferenca_profundidade": diferenca_profundidade,
        "equivalente": equivalencia,
        "somente_portas_permitidas": compativel_portas
    }

    return resultados

def avaliar_proposta_ia(original: QuantumCircuit, proposta: QuantumCircuit):
    """
    Avalia uma proposta de otimização de um circuito
    feita por uma IA, comparando com o circuito original,
    verificando equivalência e métricas.

    Destinada a circuitos unitários pequenos,
    sem medições ou operações não unitárias.
    """
    metricas_original = obter_metricas(original)
    metricas_proposta = obter_metricas(proposta)

    equivalencia = verificar_equivalencia(original, proposta)

    diferenca_portas = (
        metricas_proposta["total_operacoes"]
        - metricas_original["total_operacoes"]
    )
    
    diferenca_profundidade = (
        metricas_proposta["profundidade"]
        - metricas_original["profundidade"]
    )

    reduziu_operacoes = (equivalencia and diferenca_portas < 0)

    reduziu_profundidade = (equivalencia and diferenca_profundidade < 0)

    resultados = {
        "original": metricas_original,
        "proposta": metricas_proposta,
        "equivalente": equivalencia,
        "diferenca_portas": diferenca_portas,
        "diferenca_profundidade": diferenca_profundidade,
        "reduziu_operacoes": reduziu_operacoes,
        "reduziu_profundidade": reduziu_profundidade
    }

    return resultados