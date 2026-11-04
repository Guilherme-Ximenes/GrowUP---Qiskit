from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

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

def verificar_equivalencia(original: QuantumCircuit, otimizado: QuantumCircuit):
    """
    Verifica se dois circuitos realizam
    transformações quânticas equivalentes 
    até uma fase global.
    """
    if original.num_qubits != otimizado.num_qubits:
        return False
    
    return bool(Operator(original).equiv(Operator(otimizado)))

