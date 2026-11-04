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

def otimizar_para_hardware(circuito: QuantumCircuit, conectividade: CouplingMap, layout_inicial=None, nivel_otimizacao:int=0):
    """
    Adapta um circuito às conexões físicas
    de um hardware quântico.

    Se nenhum layout inicial for informado,
    utiliza o algoritmo SABRE.
    """
    if nivel_otimizacao not in (0, 1, 2, 3):
        raise ValueError("Nível de otimização deve ser 0, 1, 2 ou 3.")

    otimizado = transpile(
        circuito,
        coupling_map=conectividade,
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
