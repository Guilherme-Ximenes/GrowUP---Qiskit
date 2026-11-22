# DOC02 — Métricas de Circuitos Quânticos

**Projeto:** GrowUp — Módulo Qiskit  
**Tema:** Métricas e análise de circuitos quânticos  
**Compatibilidade:** Qiskit 2.6.0  
**Objetivo:** Apresentar as principais métricas utilizadas para analisar circuitos quânticos e interpretar seus resultados utilizando Qiskit.

---

## 1. Introdução às métricas de circuitos

As métricas de circuitos quânticos permitem avaliar características estruturais e quantitativas de um circuito.

Elas são importantes para:

- Analisar a complexidade estrutural de um circuito;
- Identificar a quantidade e os tipos de operações utilizadas;
- Avaliar o nível de paralelismo;
- Comparar circuitos originais e otimizados;
- Identificar possíveis melhorias antes da execução em hardware;
- Fornecer dados objetivos para processos de otimização.

No Qiskit, a classe `QuantumCircuit` disponibiliza métodos e atributos que permitem obter essas informações diretamente.

Neste projeto, a função `obter_metricas()` utiliza quatro métricas principais:

1. Quantidade de qubits;
2. Total de operações;
3. Profundidade do circuito;
4. Quantidade de cada tipo de operação.

## 2. Quantidade de qubits

A quantidade de qubits representa o número de unidades quânticas disponíveis no circuito.

No Qiskit, essa informação é obtida por meio do atributo:

```python
circuito.num_qubits
```

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(4)

print("Quantidade de qubits:", circuito.num_qubits)
```

Resultado esperado:

```text
Quantidade de qubits: 4
```

A quantidade de qubits não representa necessariamente a quantidade de qubits que receberam operações.

Um circuito pode possuir quatro qubits, mas utilizar apenas dois deles.

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(4)

circuito.h(0)
circuito.cx(0, 1)

print("Quantidade de qubits:", circuito.num_qubits)
```

Mesmo que os qubits 2 e 3 não recebam operações, o circuito continua possuindo quatro qubits.

### 2.1 Qubits e bits clássicos

O Qiskit também permite consultar a quantidade de bits clássicos:

```python
circuito.num_clbits
```

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(3, 2)

print("Qubits:", circuito.num_qubits)
print("Bits clássicos:", circuito.num_clbits)
```

Resultado esperado:

```text
Qubits: 3
Bits clássicos: 2
```

É importante distinguir a quantidade de qubits da largura do circuito.

O método:

```python
circuito.width()
```

retorna a soma da quantidade de qubits e bits clássicos.

Portanto, no exemplo anterior:

```text
width = 3 + 2 = 5
```

Neste projeto, a métrica `qubits` utiliza `num_qubits`, e não `width()`.

## 3. Total de operações

O total de operações representa a quantidade de instruções consideradas pelo método `size()` do Qiskit.

Para obter essa informação:

```python
circuito.size()
```

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.x(1)
circuito.cx(0, 1)

print("Total de operações:", circuito.size())
```

Resultado esperado:

```text
Total de operações: 3
```

Nesse circuito foram adicionadas três operações:

1. Porta H no qubit 0;
2. Porta X no qubit 1;
3. Porta CX entre os qubits 0 e 1.

### 3.1 Diferença entre operações e qubits

A quantidade de operações não corresponde à quantidade de qubits.

Um circuito com dois qubits pode possuir dezenas de operações, enquanto um circuito com dez qubits pode possuir poucas operações.

Essas métricas descrevem características diferentes:

- `num_qubits`: quantidade de qubits disponíveis;
- `size()`: quantidade de instruções consideradas pelo método.

### 3.2 Observação sobre instruções especiais

O método `size()` utiliza um filtro padrão que desconsidera diretivas, como barreiras (`barrier`).

Isso significa que o valor retornado não deve ser interpretado como uma contagem indiscriminada de todos os elementos visuais do circuito.

Operações como medições são instruções do circuito e são consideradas pela contagem padrão.

Essa distinção é importante ao analisar circuitos que possuem medições, barreiras ou outras diretivas.

## 4. Profundidade do circuito

A profundidade, ou `depth`, representa a quantidade de camadas de operações necessárias para executar o circuito, considerando as dependências entre as operações.

No Qiskit:

```python
circuito.depth()
```

A profundidade está relacionada ao caminho crítico do circuito.

Operações que atuam sobre qubits independentes podem ser executadas em paralelo, enquanto operações que dependem de resultados anteriores precisam respeitar a ordem necessária.

### 4.1 Exemplo de operações em paralelo

Considere um circuito com quatro qubits:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(4)

circuito.h(0)
circuito.cx(0, 1)

circuito.h(2)
circuito.cx(2, 3)

print(circuito.draw())
print("Profundidade:", circuito.depth())
```

Resultado esperado:

```text
Profundidade: 2
```

Embora o código contenha quatro operações, a profundidade é dois.

Isso acontece porque:

- Na primeira camada, as portas H podem ser aplicadas simultaneamente aos qubits 0 e 2.
- Na segunda camada, as portas CX podem ser aplicadas simultaneamente aos pares de qubits 0–1 e 2–3.

Representação simplificada:

```text
Camada 1: H(q0) e H(q2)
Camada 2: CX(q0,q1) e CX(q2,q3)
```

As operações são independentes entre os dois pares de qubits, permitindo paralelismo.

### 4.2 Exemplo de operações sequenciais

Agora considere um circuito em que todas as operações atuam sobre o mesmo qubit:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(1)

circuito.h(0)
circuito.x(0)
circuito.z(0)
circuito.s(0)

print(circuito.draw())
print("Profundidade:", circuito.depth())
```

Resultado esperado:

```text
Profundidade: 4
```

Nesse caso, as quatro operações precisam respeitar a sequência definida no circuito.

Não é possível colocar essas operações em uma única camada porque todas atuam sobre o mesmo qubit.

### 4.3 Relação entre profundidade e paralelismo

A profundidade permite identificar a quantidade de camadas do circuito e compreender seu nível de paralelismo.

De forma geral:

- Menor profundidade pode indicar maior paralelismo;
- Maior profundidade pode indicar mais dependências sequenciais;
- Circuitos com a mesma quantidade de operações podem apresentar profundidades diferentes.

A profundidade não representa diretamente o tempo real de execução em segundos.

Ela é uma métrica estrutural que pode servir como indicador aproximado da duração de um circuito. O tempo efetivo depende também das durações das instruções, do hardware, do agendamento e de outras restrições físicas.

O método `depth()` também possui limitações para circuitos com operações de controle de fluxo. Nesses casos, seu resultado não deve ser interpretado como uma medida geral e exata de todos os caminhos possíveis de execução.

## 5. Tipos e quantidade de operações

Além de conhecer a quantidade total de operações, é importante identificar quais operações estão presentes no circuito e quantas vezes cada uma aparece.

O Qiskit disponibiliza o método:

```python
circuito.count_ops()
```

Esse método retorna uma estrutura semelhante a um dicionário, contendo o nome de cada operação e sua quantidade.

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.h(1)
circuito.cx(0, 1)
circuito.x(0)

print(circuito.count_ops())
```

Resultado esperado:

```text
OrderedDict([('h', 2), ('cx', 1), ('x', 1)])
```

A interpretação é:

- `h`: duas ocorrências;
- `cx`: uma ocorrência;
- `x`: uma ocorrência.

Para converter o resultado em um dicionário Python convencional:

```python
tipos_operacoes = dict(circuito.count_ops())

print(tipos_operacoes)
```

Resultado:

```python
{'h': 2, 'cx': 1, 'x': 1}
```

### 5.1 Importância da contagem por tipo

A contagem por tipo permite identificar a composição do circuito.

Por exemplo:

- Muitas operações `cx` indicam uma quantidade elevada de portas controladas entre qubits;
- Muitas operações `swap` podem indicar custos adicionais de movimentação lógica durante o roteamento;
- Muitas operações de um único qubit podem indicar oportunidades de simplificação ou combinação, dependendo do circuito.

A contagem, isoladamente, não determina se o circuito é eficiente.

A relevância de cada operação depende do contexto, das portas nativas disponíveis e das características do hardware.

### 5.2 Relação entre size() e count_ops()

Os métodos `size()` e `count_ops()` apresentam informações relacionadas, mas não são exatamente a mesma coisa.

- `size()` retorna uma quantidade total de instruções, aplicando seu filtro padrão;
- `count_ops()` apresenta a quantidade de cada tipo de operação.

Em circuitos sem diretivas, como barreiras, a soma das ocorrências retornadas por `count_ops()` normalmente corresponde ao valor de `size()`.

Entretanto, diretivas podem ser contabilizadas por `count_ops()` e desconsideradas pelo filtro padrão de `size()`.

Por isso, os resultados não devem ser considerados obrigatoriamente iguais em todos os circuitos.

## 6. Obtendo as métricas com Qiskit

O Qiskit permite consultar todas as métricas principais diretamente a partir de um objeto `QuantumCircuit`.

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(4)

circuito.h(0)
circuito.cx(0, 1)
circuito.h(2)
circuito.cx(2, 3)

print("Qubits:", circuito.num_qubits)
print("Total de operações:", circuito.size())
print("Profundidade:", circuito.depth())
print("Tipos de operações:", dict(circuito.count_ops()))
```

Resultado esperado:

```text
Qubits: 4
Total de operações: 4
Profundidade: 2
Tipos de operações: {'h': 2, 'cx': 2}
```

Esse exemplo demonstra como obter as métricas sem utilizar funções adicionais.

## 7. Métricas utilizadas pelo serviço Qiskit do projeto

O projeto GrowUp possui uma função específica para calcular as métricas de um circuito:

```python
obter_metricas(circuito)
```

Essa função está implementada no arquivo `qiskit_service.py`.

Sua implementação atual é:

```python
def obter_metricas(circuito: QuantumCircuit):
    validar_circuito(circuito)

    metricas = {
        "qubits": circuito.num_qubits,
        "total_operacoes": circuito.size(),
        "profundidade": circuito.depth(),
        "tipos_operacoes": dict(circuito.count_ops())
    }

    return metricas
```

A função realiza as seguintes etapas:

1. Verifica se a entrada é um objeto `QuantumCircuit`.
2. Obtém a quantidade de qubits.
3. Calcula o total de operações.
4. Calcula a profundidade.
5. Conta a quantidade de cada tipo de operação.
6. Retorna os resultados em um dicionário Python.

### 7.1 Estrutura do retorno

A função retorna um dicionário com quatro campos:

```python
{
    "qubits": 4,
    "total_operacoes": 4,
    "profundidade": 2,
    "tipos_operacoes": {
        "h": 2,
        "cx": 2
    }
}
```

Os nomes das chaves fazem parte da estrutura atual do serviço e devem ser preservados ao integrar novos componentes.

### 7.2 Exemplo utilizando o serviço do projeto

```python
from qiskit import QuantumCircuit
from qiskit_service import obter_metricas

circuito = QuantumCircuit(4)

circuito.h(0)
circuito.cx(0, 1)
circuito.h(2)
circuito.cx(2, 3)

metricas = obter_metricas(circuito)

print(metricas)
```

Resultado esperado:

```python
{
    'qubits': 4,
    'total_operacoes': 4,
    'profundidade': 2,
    'tipos_operacoes': {'h': 2, 'cx': 2}
}
```

## 8. Comparação de métricas entre circuitos

As métricas também permitem comparar um circuito original com uma versão modificada ou otimizada.

Essa comparação ajuda a identificar se houve redução ou aumento na quantidade de operações e na profundidade.

Uma forma de calcular a diferença é:

\[
\Delta = M*{\text{novo}} - M*{\text{original}}
\]

Em que:

- \(\Delta\) representa a diferença entre as métricas;
- \(M\_{\text{novo}}\) representa a métrica do circuito novo;
- \(M\_{\text{original}}\) representa a métrica do circuito original.

A interpretação é:

| Resultado | Significado                |
| --------- | -------------------------- |
| Negativo  | Houve redução da métrica   |
| Zero      | A métrica permaneceu igual |
| Positivo  | Houve aumento da métrica   |

Exemplo:

```python
operacoes_originais = 10
operacoes_otimizadas = 7

diferenca = operacoes_otimizadas - operacoes_originais

print("Diferença:", diferenca)
```

Resultado:

```text
Diferença: -3
```

Nesse exemplo, a versão nova possui três operações a menos.

### 8.1 Comparação de profundidade

O mesmo raciocínio pode ser utilizado para comparar profundidades.

```python
profundidade_original = 8
profundidade_otimizada = 5

diferenca = profundidade_otimizada - profundidade_original

print("Diferença de profundidade:", diferenca)
```

Resultado:

```text
Diferença de profundidade: -3
```

A profundidade foi reduzida em três camadas.

### 8.2 Interpretação no serviço do projeto

O serviço Qiskit possui funções que utilizam essas métricas para avaliar propostas de otimização.

A função `avaliar_proposta_ia()` retorna, entre outras informações:

- `diferenca_operacoes`;
- `diferenca_profundidade`;
- `reduziu_operacoes`;
- `reduziu_profundidade`;
- `equivalente`;
- `status_verificacao`.

As diferenças são calculadas entre a proposta e o circuito original.

Entretanto, as reduções só são consideradas válidas quando a equivalência foi confirmada.

A interpretação dos campos de redução é:

- `True`: o circuito foi verificado como equivalente e apresentou redução naquela métrica;
- `False`: não foi confirmada uma redução válida;
- `None`: não foi possível verificar a equivalência, portanto não é possível confirmar a redução.

Essa distinção impede que uma proposta incorreta seja considerada uma otimização válida apenas porque possui menos operações ou menor profundidade.

## 9. Métricas e eficiência de circuitos

Uma análise de eficiência não deve considerar apenas uma métrica isolada.

Por exemplo, um circuito pode apresentar:

- Menor quantidade de operações, mas maior profundidade;
- Maior quantidade de operações, mas menor profundidade;
- Menos portas de um tipo e mais portas de outro;
- Mais operações após a adaptação às restrições do hardware.

Esses cenários demonstram que a eficiência depende do objetivo da otimização.

Para avaliar uma proposta, é importante observar:

1. Se o circuito continua funcionalmente equivalente ao original;
2. Se houve redução no total de operações;
3. Se houve redução na profundidade;
4. Quais tipos de operações foram removidos ou adicionados;
5. Se a nova composição é compatível com as restrições do hardware.

### 9.1 Limitações das métricas

As métricas estruturais não são suficientes para determinar, isoladamente, o desempenho real de um circuito em hardware.

Elas não representam diretamente:

- Taxas de erro das portas;
- Ruído do processador quântico;
- Fidelidade real da execução;
- Duração física de cada operação;
- Tempo real de execução;
- Custo de comunicação ou disponibilidade de conexões entre qubits.

A profundidade pode fornecer uma indicação estrutural do caminho crítico, mas não substitui uma análise de duração baseada nas características do hardware.

O número de operações também não representa necessariamente o custo físico de todas as portas. Diferentes instruções podem apresentar durações e taxas de erro distintas.

Portanto, as métricas devem ser utilizadas em conjunto com a análise de equivalência, transpilação e compatibilidade com hardware.

## 10. Outras métricas disponíveis no Qiskit

Além das métricas utilizadas atualmente por `obter_metricas()`, o Qiskit disponibiliza outras informações que podem ser úteis em análises mais avançadas.

| Método ou atributo          | Descrição                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `num_clbits`                | Quantidade de bits clássicos                                                               |
| `width()`                   | Soma dos qubits e bits clássicos                                                           |
| `num_nonlocal_gates()`      | Quantidade de operações que envolvem dois ou mais qubits                                   |
| `num_parameters`            | Quantidade de parâmetros do circuito                                                       |
| `count_ops_per_qubit()`     | Contagem de operações separada por qubit                                                   |
| `estimate_duration(target)` | Estimativa de duração de um circuito agendado, utilizando informações de duração do Target |

Essas informações não fazem parte do retorno atual de `obter_metricas()`.

Elas podem ser incorporadas futuramente ao serviço, caso o projeto necessite de análises mais detalhadas.

Em particular, `estimate_duration(target)` exige que o circuito tenha sido agendado e que o objeto `Target` possua as informações de duração necessárias para as instruções.

## 11. Relação com os exemplos do módulo Qiskit

Este documento estabelece a base conceitual para:

- **EX03 — Gate count, depth e paralelismo:** cálculo e interpretação das métricas fundamentais.
- **EX04 — Cancelamento de portas redundantes:** análise da redução de operações e profundidade.
- **EX05 — Transpile e níveis de otimização:** comparação das métricas antes e depois da transpilação.
- **EX06 — CouplingMap, layout e roteamento:** análise do impacto das restrições de hardware na estrutura do circuito.

Os conceitos apresentados também são utilizados pelas funções `comparar_niveis()`, `analisar_adaptacao_hardware()` e `avaliar_proposta_ia()` presentes no serviço Qiskit do projeto.

## 12. Referências

### Documentação oficial

1. IBM Quantum Documentation — QuantumCircuit:
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit

2. IBM Quantum Documentation — Construct circuits:
   https://quantum.cloud.ibm.com/docs/en/guides/construct-circuits

### Implementação do projeto

3. GrowUP — Qiskit — `qiskit_service.py`:
   https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/qiskit_service.py

4. GrowUP — Qiskit — `teste_qiskit_service.py`:
   https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/teste_qiskit_service.py

---

**Projeto:** GrowUp — Módulo Qiskit  
**Documento:** DOC02  
**Tema:** Métricas de Circuitos Quânticos
