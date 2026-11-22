# DOC06 — Equivalência e Validação de Circuitos Quânticos

## 1. Objetivo

Este documento apresenta os conceitos e os recursos do Qiskit utilizados para verificar se dois circuitos quânticos implementam o mesmo comportamento, mesmo quando possuem estruturas e quantidades de operações diferentes.

O objetivo é estabelecer critérios para validar transformações realizadas durante a otimização de circuitos, evitando que reduções de portas ou profundidade sejam consideradas corretas sem uma verificação de equivalência.

O conteúdo aborda:

- Diferença entre igualdade estrutural e equivalência funcional.
- Equivalência de operadores unitários.
- Utilização de `Operator` e `Operator.equiv()`.
- Equivalência de estados quânticos com `Statevector`.
- Cancelamento de operações redundantes.
- Validação de circuitos antes e depois da otimização.
- Cuidados com medições, fase global e layouts.
- Validação de circuitos transpilados.
- Registro de evidências e limitações da validação.

Este documento é especialmente importante para sistemas de otimização automática, nos quais o agente precisa justificar as transformações realizadas e demonstrar que o circuito otimizado preserva o comportamento esperado.

---

## 2. Igualdade estrutural e equivalência funcional

### 2.1. Igualdade estrutural

Dois circuitos são estruturalmente iguais quando suas estruturas, operações e propriedades relevantes correspondem segundo os critérios de comparação utilizados.

Por exemplo:

```python
from qiskit import QuantumCircuit

circuito_a = QuantumCircuit(1)
circuito_a.h(0)
circuito_a.x(0)

circuito_b = QuantumCircuit(1)
circuito_b.h(0)
circuito_b.x(0)

print(circuito_a == circuito_b)
```

Nesse caso, os circuitos possuem a mesma estrutura e operações.

Entretanto, a igualdade estrutural não é suficiente para determinar se dois circuitos executam a mesma transformação quântica.

### 2.2. Equivalência funcional

Dois circuitos podem possuir estruturas completamente diferentes e, ainda assim, produzir a mesma transformação quântica.

Considere:

```python
from qiskit import QuantumCircuit

circuito_a = QuantumCircuit(1)
circuito_a.h(0)
circuito_a.h(0)

circuito_b = QuantumCircuit(1)

print(circuito_a == circuito_b)
```

A comparação estrutural retorna `False`, pois um circuito possui duas portas Hadamard e o outro não possui operações.

Entretanto, a identidade:

\[
H \cdot H = I
\]

demonstra que duas aplicações consecutivas da porta Hadamard equivalem à operação identidade.

Portanto, os dois circuitos implementam a mesma transformação unitária.

Essa distinção é fundamental para a otimização quântica: uma transformação pode alterar completamente a estrutura do circuito sem modificar seu comportamento matemático.

---

## 3. Equivalência de operadores unitários

### 3.1. O que é um operador unitário?

As operações quânticas reversíveis podem ser representadas por matrizes unitárias.

Uma matriz \(U\) é unitária quando:

\[
U^\dagger U = I
\]

Onde:

- \(U^\dagger\): matriz adjunta de \(U\).
- \(I\): matriz identidade.

Um circuito composto exclusivamente por operações unitárias pode ser representado por um operador que descreve sua transformação sobre todos os possíveis estados de entrada.

Para verificar se dois circuitos unitários implementam a mesma transformação, podemos comparar seus operadores.

### 3.2. Utilizando Operator

A classe `Operator`, disponível em `qiskit.quantum_info`, permite representar operações quânticas por matrizes.

Exemplo:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

circuito_a = QuantumCircuit(1)
circuito_a.h(0)
circuito_a.h(0)

circuito_b = QuantumCircuit(1)

operador_a = Operator(circuito_a)
operador_b = Operator(circuito_b)

print(operador_a.equiv(operador_b))
```

Resultado esperado:

```text
True
```

Nesse exemplo, o Qiskit converte os circuitos em operadores e verifica se eles são equivalentes.

### 3.3. Utilizando Operator.equiv()

O método `equiv()` verifica se dois operadores são equivalentes, considerando também a possibilidade de uma diferença de fase global.

Exemplo:

```python
equivalentes = operador_a.equiv(operador_b)

if equivalentes:
    print("Os circuitos são equivalentes.")
else:
    print("Os circuitos não são equivalentes.")
```

O retorno é booleano:

- `True`: os operadores são equivalentes dentro das tolerâncias utilizadas.
- `False`: os operadores não foram considerados equivalentes.

O método aceita os parâmetros `rtol` e `atol`, utilizados para controlar as tolerâncias numéricas da comparação.

Exemplo:

```python
equivalentes = operador_a.equiv(
    operador_b,
    rtol=1e-5,
    atol=1e-8
)
```

A tolerância é importante porque operações envolvendo números complexos e cálculos de ponto flutuante podem produzir pequenas diferenças numéricas.

### 3.4. Equivalência considerando fase global

Dois operadores podem diferir por um fator de fase global e ainda representar a mesma transformação física quando considerados isoladamente.

Matematicamente:

\[
U = e^{i\phi}V
\]

Onde:

- \(U\) e \(V\) são operadores unitários.
- \(\phi\) representa uma fase real.
- \(e^{i\phi}\) é o fator de fase global.

O método `Operator.equiv()` considera essa equivalência.

É importante distinguir fase global de fase relativa. Uma fase relativa entre componentes de um estado pode alterar os resultados de interferência e, portanto, não deve ser ignorada.

**Atenção:** uma fase global aparentemente irrelevante para um circuito isolado pode se tornar relevante quando o circuito é incorporado como uma operação controlada. Portanto, a validação deve considerar o contexto em que o circuito será utilizado.

---

## 4. Equivalência de estados quânticos com Statevector

### 4.1. Diferença entre equivalência de estados e equivalência de circuitos

A equivalência de estados verifica se dois vetores de estado representam o mesmo estado quântico, considerando a fase global.

Entretanto, isso não significa necessariamente que os circuitos que produziram esses estados implementam a mesma transformação para todas as entradas possíveis.

Considere dois circuitos que produzem o mesmo estado quando recebem a entrada \(|0\rangle\), mas que se comportam de maneira diferente quando recebem \(|1\rangle\).

A comparação dos estados de saída para \(|0\rangle\) não seria suficiente para identificar essa diferença.

Portanto:

- `Statevector.equiv()`: compara estados quânticos.
- `Operator.equiv()`: compara transformações unitárias completas.

### 4.2. Comparando estados com Statevector

Exemplo:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

circuito_a = QuantumCircuit(1)
circuito_a.h(0)
circuito_a.h(0)

circuito_b = QuantumCircuit(1)

estado_a = Statevector.from_instruction(circuito_a)
estado_b = Statevector.from_instruction(circuito_b)

print(estado_a.equiv(estado_b))
```

Resultado esperado:

```text
True
```

Nesse caso, os dois circuitos produzem o mesmo estado final quando iniciados em \(|0\rangle\).

### 4.3. Quando utilizar cada método?

| Objetivo                                    | Recurso recomendado                              |
| ------------------------------------------- | ------------------------------------------------ |
| Comparar a estrutura dos circuitos          | `QuantumCircuit.__eq__`                          |
| Comparar transformações unitárias completas | `Operator.equiv()`                               |
| Comparar estados finais específicos         | `Statevector.equiv()`                            |
| Comparar resultados de medição              | Comparação de distribuições de resultados        |
| Validar circuito transpilado com layout     | `Operator.from_circuit()` e tratamento do layout |

A escolha do método deve corresponder à propriedade que se deseja validar.

---

## 5. Cancelamento de operações redundantes

### 5.1. O que são operações redundantes?

Uma operação redundante é uma operação que pode ser removida ou substituída sem alterar o comportamento funcional do circuito.

Algumas portas possuem propriedades matemáticas que permitem simplificações.

Exemplos:

\[
X \cdot X = I
\]

\[
H \cdot H = I
\]

\[
Z \cdot Z = I
\]

\[
CX \cdot CX = I
\]

Essas identidades indicam que aplicar duas vezes determinadas operações consecutivas resulta na operação identidade.

### 5.2. Exemplo de simplificação

Considere um circuito com quatro operações:

```python
from qiskit import QuantumCircuit

circuito_original = QuantumCircuit(1)

circuito_original.h(0)
circuito_original.h(0)
circuito_original.x(0)
circuito_original.x(0)

print(circuito_original.draw())
```

O circuito possui:

- Duas portas Hadamard.
- Duas portas X.

Aplicando as identidades:

\[
H \cdot H = I
\]

\[
X \cdot X = I
\]

O circuito pode ser simplificado para:

```python
circuito_otimizado = QuantumCircuit(1)

print(circuito_otimizado.draw())
```

O circuito otimizado não precisa executar nenhuma porta.

### 5.3. Validando a simplificação

A redução de operações não é suficiente para comprovar que a otimização está correta.

É necessário comparar os operadores:

```python
from qiskit.quantum_info import Operator

operador_original = Operator(circuito_original)
operador_otimizado = Operator(circuito_otimizado)

equivalentes = operador_original.equiv(operador_otimizado)

print("Equivalentes:", equivalentes)
```

Resultado esperado:

```text
Equivalentes: True
```

Nesse exemplo, a validação demonstra que o circuito otimizado preserva a transformação unitária original.

### 5.4. Importância da justificativa das transformações

Um sistema de otimização não deve apresentar apenas as métricas antes e depois.

Também deve explicar:

1. Quais operações foram identificadas como redundantes.
2. Qual identidade matemática justifica cada simplificação.
3. Quais operações foram removidas ou substituídas.
4. Quais métricas foram alteradas.
5. Se a equivalência foi verificada.
6. Qual método foi utilizado para realizar a verificação.

Por exemplo:

> Foram identificadas duas aplicações consecutivas da porta Hadamard no mesmo qubit. Como \(H^2=I\), as duas operações podem ser removidas. A equivalência entre os circuitos original e otimizado foi verificada utilizando `Operator.equiv()`, que retornou `True`.

Essa explicação apresenta uma justificativa matemática e uma evidência de validação.

---

## 6. Validação antes e depois da otimização

### 6.1. Por que validar a otimização?

Uma otimização pode reduzir:

- Quantidade de portas.
- Profundidade do circuito.
- Quantidade de operações de dois qubits.
- Quantidade de operações necessárias para executar o circuito.

Entretanto, uma redução dessas métricas não garante que o circuito continue realizando a transformação original.

Um otimizador pode produzir um circuito menor, mas funcionalmente incorreto.

Por isso, a equivalência deve ser tratada como uma etapa independente da avaliação de desempenho.

### 6.2. Fluxo recomendado de validação

O processo de validação pode seguir as seguintes etapas:

1. Receber o circuito original.
2. Registrar suas métricas.
3. Aplicar a otimização.
4. Registrar as métricas do circuito otimizado.
5. Construir os operadores dos dois circuitos.
6. Comparar os operadores.
7. Registrar o resultado da verificação.
8. Apresentar as transformações e as evidências.

Fluxo conceitual:

```text
Circuito original
       |
       v
Coleta de métricas
       |
       v
Aplicação da otimização
       |
       v
Circuito otimizado
       |
       v
Coleta de métricas
       |
       v
Verificação de equivalência
       |
       v
Resultado da validação
       |
       v
Relatório com evidências
```

### 6.3. Exemplo de validação automatizada

O exemplo seguinte apresenta uma função simplificada para comparar circuitos unitários.

```python
from qiskit.quantum_info import Operator

def validar_equivalencia(circuito_original, circuito_otimizado):

    if circuito_original.num_qubits != circuito_otimizado.num_qubits:
        return {
            "valido": False,
            "equivalente": None,
            "motivo": "Os circuitos possuem quantidades diferentes de qubits."
        }

    try:
        operador_original = Operator.from_circuit(circuito_original)
        operador_otimizado = Operator.from_circuit(circuito_otimizado)

        equivalentes = operador_original.equiv(operador_otimizado)

        return {
            "valido": True,
            "equivalente": equivalentes,
            "motivo": (
                "Os operadores são equivalentes."
                if equivalentes
                else "Os operadores não são equivalentes."
            )
        }

    except Exception as erro:
        return {
            "valido": False,
            "equivalente": None,
            "motivo": f"Não foi possível realizar a comparação: {erro}"
        }
```

Utilização:

```python
resultado = validar_equivalencia(
    circuito_original,
    circuito_otimizado
)

print(resultado)
```

A função distingue três situações:

- Validação realizada e equivalência confirmada.
- Validação realizada e equivalência não confirmada.
- Validação não realizada por incompatibilidade ou erro durante a conversão.

Essa distinção é importante: uma falha na validação não deve ser apresentada como prova de que os circuitos são diferentes.

**Limitação:** essa implementação é destinada à comparação de circuitos unitários com a mesma quantidade de qubits. Circuitos com medições, operações não unitárias, diferentes larguras ou semânticas específicas exigem estratégias adicionais de validação.

---

## 7. Cuidados com circuitos que possuem medições

### 7.1. Por que Operator não é suficiente?

A classe `Operator` representa transformações lineares, especialmente operações unitárias.

Entretanto, medições são operações não reversíveis e não podem ser tratadas como portas unitárias comuns.

Considere:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(1, 1)

circuito.h(0)
circuito.measure(0, 0)
```

Esse circuito possui uma medição.

Não é correto assumir que sua execução pode ser representada simplesmente por um operador unitário equivalente ao circuito inteiro.

### 7.2. Estratégias para validar circuitos medidos

Quando os circuitos possuem medições, a validação deve considerar o comportamento observável.

Uma abordagem é:

1. Identificar a parte unitária do circuito.
2. Comparar as operações unitárias antes das medições, quando isso for apropriado.
3. Verificar os qubits medidos e os bits clássicos que recebem os resultados.
4. Comparar as distribuições de resultados esperadas.
5. Considerar a ordem dos bits e os mapeamentos entre qubits e bits clássicos.

Também é possível utilizar simulações com shots para comparar distribuições de resultados.

Entretanto, frequências obtidas por amostragem podem apresentar variações estatísticas. Uma comparação desse tipo deve utilizar critérios e tolerâncias adequados.

### 7.3. Atenção ao mapeamento de medições

Dois circuitos podem possuir estados quânticos equivalentes, mas armazenar os resultados em bits clássicos diferentes.

Por exemplo:

```python
from qiskit import QuantumCircuit

circuito_a = QuantumCircuit(2, 2)
circuito_a.x(0)
circuito_a.measure([0, 1], [0, 1])

circuito_b = QuantumCircuit(2, 2)
circuito_b.x(0)
circuito_b.measure([0, 1], [1, 0])
```

A correspondência entre qubits e bits clássicos foi alterada.

Portanto, não se deve comparar apenas os estados quânticos sem verificar também o significado dos resultados clássicos.

---

## 8. Equivalência após transpilação e layouts

### 8.1. O problema dos layouts

Durante a transpilação, o Qiskit pode mapear qubits virtuais do circuito original para qubits físicos do dispositivo.

Esse processo pode alterar a organização dos qubits e a estrutura do circuito.

O roteamento também pode inserir operações SWAP, modificando a posição lógica dos estados ao longo da execução.

Consequentemente, a comparação direta entre os circuitos pode produzir interpretações incorretas quando os layouts não são considerados.

### 8.2. Utilizando Operator.from_circuit()

O método `Operator.from_circuit()` permite construir um operador a partir de um circuito, considerando informações de layout disponíveis.

Exemplo:

```python
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

circuito_original = QuantumCircuit(2)

circuito_original.h(0)
circuito_original.cx(0, 1)

circuito_transpilado = transpile(
    circuito_original,
    optimization_level=3,
    seed_transpiler=42
)

operador_original = Operator.from_circuit(circuito_original)

operador_transpilado = Operator.from_circuit(circuito_transpilado)

equivalentes = operador_original.equiv(operador_transpilado)

print("Equivalência:", equivalentes)
```

O `Operator.from_circuit()` oferece suporte ao tratamento do layout associado ao circuito, incluindo informações de layout inicial e final.

Isso é importante para avaliar circuitos que passaram pelas etapas de layout e roteamento do transpiler.

### 8.3. Cuidados com circuitos de larguras diferentes

Um circuito lógico pode possuir menos qubits do que o circuito físico transpilado.

Por exemplo:

- Circuito lógico: 3 qubits.
- Circuito físico: 5 qubits disponíveis no backend.

A comparação direta dos operadores completos pode não ser apropriada, pois suas dimensões são diferentes.

Nesses casos, é necessário considerar a representação lógica, os qubits auxiliares, os layouts e as condições de entrada e saída.

Não se deve concluir que dois circuitos são diferentes apenas porque suas representações físicas possuem quantidades distintas de qubits.

Também não se deve declarar equivalência sem demonstrar como a comparação considerou os qubits adicionais e o mapeamento lógico-físico.

### 8.4. Layout e roteamento como evidências

Em análises de transpilação, recomenda-se registrar:

- Layout inicial.
- Layout final.
- Mapeamento dos qubits lógicos para os físicos.
- Operações SWAP inseridas.
- Quantidade de portas de dois qubits.
- Profundidade antes e depois da transpilação.
- Resultado da verificação de equivalência.

Essas informações permitem explicar não apenas se houve uma transformação, mas também como ela foi realizada.

---

## 9. Validação e confiabilidade dos resultados apresentados pelo agente

### 9.1. Métricas não comprovam equivalência

Considere dois circuitos:

| Métrica      | Original | Otimizado |
| ------------ | -------: | --------: |
| Operações    |        7 |         3 |
| Profundidade |        4 |         2 |

Esses números demonstram uma possível melhoria estrutural.

Entretanto, não comprovam que o circuito otimizado preserva o comportamento do original.

Para confirmar a otimização, é necessário apresentar uma verificação de equivalência adequada ao tipo de circuito.

### 9.2. Não confundir ausência de validação com equivalência

Um sistema pode encontrar dificuldades para converter um circuito em operador ou para comparar circuitos com características incompatíveis.

Nessa situação, o resultado correto é informar que a equivalência não foi verificada.

Não se deve:

- Declarar equivalência sem executar uma verificação.
- Interpretar uma exceção como confirmação de equivalência.
- Apresentar uma otimização como validada apenas porque as métricas diminuíram.
- Inventar resultados de execução.
- Apresentar código QASM como evidência de que o circuito foi executado.
- Afirmar que uma operação foi removida sem demonstrar a transformação.

### 9.3. Estados possíveis da validação

Para aumentar a confiabilidade dos resultados, recomenda-se distinguir três estados:

| Estado                      | Significado                                                |
| --------------------------- | ---------------------------------------------------------- |
| Equivalência confirmada     | A verificação foi realizada e retornou resultado positivo. |
| Equivalência não confirmada | A verificação foi realizada e retornou resultado negativo. |
| Não verificada              | A verificação não pôde ser realizada ou não foi executada. |

Essa classificação impede que a ausência de evidências seja apresentada como resultado positivo ou negativo.

### 9.4. Evidências recomendadas

Um relatório de otimização deve apresentar:

1. Circuito original.
2. Circuito otimizado.
3. Transformações realizadas.
4. Justificativa matemática das transformações.
5. Métricas antes e depois.
6. Método de validação utilizado.
7. Resultado da validação.
8. Limitações ou condições da comparação.

Se uma simulação tiver sido executada, o sistema deve informar o método, a quantidade de shots quando aplicável e os resultados efetivamente obtidos.

Se a simulação não tiver sido executada, deve separar claramente as deduções teóricas dos resultados experimentais.

---

## 10. Recomendações para desenvolvimento do componente Qiskit

Para o desenvolvimento de recursos de otimização e validação, recomenda-se:

1. Separar a função de otimização da função de validação.
2. Utilizar `Operator.equiv()` para comparar transformações unitárias completas.
3. Utilizar `Statevector.equiv()` quando o objetivo for comparar estados finais específicos.
4. Considerar a fase global na interpretação dos resultados.
5. Tratar circuitos com medições separadamente.
6. Considerar layouts e permutações ao validar circuitos transpilados.
7. Registrar as transformações realizadas e suas justificativas matemáticas.
8. Registrar as métricas antes e depois da otimização.
9. Diferenciar equivalência confirmada, não confirmada e não verificada.
10. Não apresentar resultados de execução que não tenham sido efetivamente obtidos.

### Possibilidades de evolução

O componente Qiskit pode ser ampliado futuramente com:

- Função automatizada de validação de equivalência.
- Detecção de operações redundantes.
- Registro das transformações realizadas durante a otimização.
- Comparação automatizada de operadores.
- Validação de circuitos após transpilação.
- Tratamento específico de circuitos com medições.
- Relatórios estruturados de validação.
- Testes automatizados para diferentes tipos de circuitos.

---

## 11. Resumo

Neste documento foram apresentados os principais conceitos e recursos utilizados para verificar a equivalência e a validade de transformações em circuitos quânticos.

Os conceitos fundamentais são:

- Igualdade estrutural: verifica se os circuitos possuem estruturas equivalentes segundo os critérios de comparação do Qiskit.
- Equivalência funcional: verifica se circuitos implementam a mesma transformação quântica.
- `Operator`: representa operações quânticas por matrizes.
- `Operator.equiv()`: verifica equivalência entre operadores, considerando fase global.
- `Statevector.equiv()`: compara estados quânticos, não transformações completas.
- Cancelamento de operações: utiliza identidades matemáticas para remover operações redundantes.
- `Operator.from_circuit()`: permite construir operadores considerando informações de layout.
- Validação após otimização: comprova se as transformações preservaram o comportamento do circuito.
- Evidências: justificativas matemáticas, métricas e resultados de validação devem ser apresentados separadamente.

A equivalência é uma etapa essencial para garantir a confiabilidade de sistemas de otimização de circuitos quânticos.

Um circuito menor ou com menor profundidade não é necessariamente correto. A otimização só deve ser considerada validada quando houver evidências adequadas de que o comportamento original foi preservado.

---

## 12. Referências 

1. **IBM Quantum — Operator API**  
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator

2. **IBM Quantum — Statevector API**  
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector

3. **IBM Quantum — QuantumCircuit API**  
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit

4. **IBM Quantum — TranspileLayout API**  
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.transpiler.TranspileLayout

5. **Qiskit — GitHub Repository**  
   https://github.com/Qiskit/qiskit

6. **Qiskit — Quantum Information Module**  
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/quantum_info
