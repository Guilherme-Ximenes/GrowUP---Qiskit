
# DOC04 — Conectividade de Hardware

## Objetivo

Este documento apresenta os conceitos de conectividade de hardware e adaptação de circuitos quânticos às restrições físicas de um processador quântico.

O objetivo é compreender como o Qiskit transforma um circuito lógico em uma representação compatível com a topologia e o conjunto de portas de um hardware específico.

No projeto, esses conceitos são utilizados principalmente pelas funções:

- `otimizar_para_hardware()`
- `analisar_adaptacao_hardware()`

---

## 1. Circuitos lógicos e circuitos físicos

Ao construir um circuito com `QuantumCircuit`, normalmente trabalhamos com qubits lógicos, também chamados de qubits virtuais.

Esses qubits representam os elementos utilizados pelo algoritmo quântico, mas ainda não estão associados a posições específicas de um processador físico.

Um hardware quântico real possui limitações, como:

- Quantidade limitada de qubits físicos.
- Conectividade restrita entre qubits.
- Conjunto específico de portas quânticas suportadas.
- Diferenças de desempenho e confiabilidade entre operações e qubits.

Por isso, um circuito lógico nem sempre pode ser executado diretamente em um processador quântico.

A etapa de adaptação precisa considerar essas restrições.

**Exemplo:**

Um circuito pode solicitar uma operação CNOT entre os qubits lógicos 0 e 2:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(3)

circuito.cx(0, 2)
```

Entretanto, se o hardware não permitir uma interação direta entre os qubits físicos correspondentes, o Qiskit precisará encontrar uma maneira de adaptar o circuito.

---

## 2. Mapa de conectividade — CouplingMap

O `CouplingMap` representa a conectividade entre os qubits físicos de um processador.

Ele funciona como um grafo:

- Os vértices representam os qubits físicos.
- As arestas representam as conexões permitidas entre eles.
- Cada conexão indica quais interações de dois qubits podem ser realizadas diretamente.

Uma característica importante é que o grafo é direcionado. Isso significa que a conexão entre dois qubits pode depender da direção da operação.

Por exemplo, uma conexão de 0 para 1 não significa necessariamente que a conexão de 1 para 0 também esteja disponível.

### 2.1 Criando mapas de conectividade

O Qiskit permite criar diferentes topologias utilizando `CouplingMap`.

```python
from qiskit.transpiler import CouplingMap

# Três qubits conectados em linha
conectividade = CouplingMap.from_line(3)

# Exibir as conexões
print(conectividade.get_edges())
```

Representação conceitual:

```text
Qubit 0 ----- Qubit 1 ----- Qubit 2
```

Por padrão, `from_line(3)` cria conexões bidirecionais.

Também existem outras topologias:

```python
# Todos os qubits conectados entre si
conectividade_completa = CouplingMap.from_full(3)

# Qubits organizados em uma grade
conectividade_grade = CouplingMap.from_grid(2, 2)

# Qubits organizados em um anel
conectividade_anel = CouplingMap.from_ring(4)
```

Essas estruturas permitem representar diferentes arquiteturas de processadores quânticos.

### 2.2 Importância da conectividade

Considere novamente três qubits organizados em linha:

```text
Qubit 0 ----- Qubit 1 ----- Qubit 2
```

Nesse cenário:

- O qubit 0 está conectado diretamente ao qubit 1.
- O qubit 1 está conectado diretamente ao qubit 2.
- Os qubits 0 e 2 não possuem conexão direta.

Portanto, uma operação de dois qubits entre 0 e 2 exige uma adaptação do circuito.

É nesse contexto que entra o processo de roteamento.

---

## 3. Mapeamento de qubits — Layout

O layout determina a associação entre os qubits virtuais do circuito e os qubits físicos do processador.

Essa associação é necessária porque o hardware possui posições físicas específicas.

Por exemplo:

```text
Qubits virtuais:

q0    q1    q2

        |
        v

Qubits físicos:

p2    p0    p1
```

Nesse exemplo:

- O qubit virtual 0 foi associado ao físico 2.
- O qubit virtual 1 foi associado ao físico 0.
- O qubit virtual 2 foi associado ao físico 1.

### 3.1 Layout inicial

O parâmetro `initial_layout` permite definir manualmente a posição inicial dos qubits virtuais.

No Qiskit, é possível fornecer esse mapeamento utilizando diferentes estruturas, como listas, dicionários ou objetos `Layout`.

Exemplo com lista:

```python
layout_inicial = [2, 0, 1]
```

A lista representa o mapeamento dos qubits virtuais para os físicos:

| Qubit virtual | Qubit físico |
|---|---|
| 0 | 2 |
| 1 | 0 |
| 2 | 1 |

O layout inicial pode influenciar diretamente a quantidade de operações necessárias para adaptar o circuito.

Um bom posicionamento pode reduzir a necessidade de SWAPs.

### 3.2 Layout final

O layout final representa a posição dos qubits após as transformações realizadas durante a transpilação.

É importante compreender que o layout final pode ser diferente do inicial.

Isso acontece porque o processo de roteamento pode inserir operações SWAP, alterando a associação entre os estados lógicos e as posições físicas.

O Qiskit armazena informações sobre essas transformações no atributo `layout` do circuito transpilado.

Exemplo:

```python
# Layout inicial
print(adaptado.layout.initial_index_layout())

# Layout final
print(adaptado.layout.final_index_layout())
```

Essas informações são importantes para interpretar corretamente o resultado da transpilação.

---

## 4. Roteamento e portas SWAP

O roteamento é responsável por adaptar as operações de dois qubits às conexões disponíveis no hardware.

Quando dois qubits não possuem uma conexão direta, o Qiskit pode inserir operações SWAP para aproximar seus estados lógicos na topologia física.

### 4.1 O que é uma porta SWAP?

A porta SWAP troca os estados de dois qubits.

Matematicamente:

\[
SWAP(|a\rangle \otimes |b\rangle)
=
|b\rangle \otimes |a\rangle
\]

Na adaptação ao hardware, essa operação permite reorganizar a distribuição dos estados lógicos entre os qubits físicos.

É importante destacar que o SWAP não movimenta fisicamente os qubits no processador. Ele troca os estados quânticos armazenados neles.

### 4.2 Exemplo de roteamento

Considere a seguinte topologia:

```text
Qubit 0 ----- Qubit 1 ----- Qubit 2
```

Se o circuito precisar executar uma operação entre os qubits físicos 0 e 2, será necessário adaptar a distribuição dos estados.

Uma possibilidade é utilizar uma operação SWAP entre os qubits 1 e 2:

```text
Antes:

Qubit 0 ----- Qubit 1 ----- Qubit 2

Depois do SWAP:

Qubit 0 ----- Qubit 1 ----- Qubit 2
                  |             |
             Estado 2      Estado 1
```

Após a troca, os estados lógicos podem ocupar posições que permitam executar a operação desejada.

O roteamento pode inserir uma ou mais operações SWAP, dependendo da topologia e da sequência de operações do circuito.

### 4.3 Custo das operações SWAP

As portas SWAP podem representar um custo significativo.

Muitos processadores não possuem SWAP como operação nativa.

Quando isso acontece, o Qiskit pode decompor uma operação SWAP em três operações CNOT:

\[
SWAP = CX_{0,1} \cdot CX_{1,0} \cdot CX_{0,1}
\]

Essa decomposição aumenta a quantidade de operações do circuito.

Consequentemente, pode aumentar:

- A quantidade total de portas.
- A profundidade do circuito.
- O tempo necessário para execução.
- A exposição do circuito ao ruído quântico.

Por isso, reduzir a quantidade de SWAPs é um dos objetivos importantes da adaptação ao hardware.

---

## 5. Portas nativas — Basis Gates

Cada processador quântico possui um conjunto de operações que consegue executar diretamente.

Essas operações são chamadas de portas nativas.

Um circuito pode utilizar portas abstratas como:

- H (Hadamard).
- X (Pauli-X).
- CX (CNOT).
- T.
- CCX (Toffoli).

Entretanto, o hardware pode suportar apenas um subconjunto dessas operações.

O parâmetro `basis_gates` permite informar ao Qiskit quais portas devem ser utilizadas como base para a tradução do circuito.

Exemplo:

```python
portas_nativas = ["rz", "sx", "x", "cx"]
```

Nesse caso, o circuito será traduzido para utilizar as portas especificadas, quando necessário.

### 5.1 Tradução das portas

Considere uma operação Hadamard:

```python
circuito.h(0)
```

Se a porta H não estiver disponível no conjunto informado, o Qiskit precisará encontrar uma decomposição equivalente utilizando as portas permitidas.

O mesmo princípio se aplica às portas SWAP e às operações mais complexas.

Essa transformação acontece durante o estágio de tradução da transpilação.

A tradução pode aumentar a quantidade de operações e a profundidade do circuito.

### 5.2 Basis Gates não representam todo o hardware

A lista `basis_gates` representa uma restrição sobre as portas utilizadas, mas não descreve necessariamente todas as características de um processador real.

Um hardware também pode possuir:

- Restrições específicas por qubit.
- Diferentes operações disponíveis em diferentes pares de qubits.
- Tempos de execução específicos.
- Taxas de erro diferentes.
- Restrições de medição e reset.

Para representar essas características de maneira mais completa, o Qiskit oferece estruturas como `Target` e a configuração de um backend.

---

## 6. Adaptação ao hardware no projeto

No projeto, a função `otimizar_para_hardware()` é responsável por adaptar um circuito às restrições de conectividade e portas nativas informadas.

Sua implementação utiliza `transpile()`:

```python
def otimizar_para_hardware(
    circuito: QuantumCircuit,
    conectividade: CouplingMap,
    layout_inicial=None,
    nivel_otimizacao: int = 0,
    portas_nativas: list[str] | None = None
):
    validar_circuito(circuito)

    if not isinstance(conectividade, CouplingMap):
        raise TypeError(
            "O parâmetro 'conectividade' deve ser um CouplingMap."
        )

    if nivel_otimizacao not in (0, 1, 2, 3):
        raise ValueError(
            "Nível de otimização deve ser 0, 1, 2 ou 3."
        )

    otimizado = transpile(
        circuito,
        coupling_map=conectividade,
        basis_gates=portas_nativas,
        initial_layout=layout_inicial,
        layout_method="sabre" if layout_inicial is None else None,
        routing_method="basic",
        optimization_level=nivel_otimizacao,
        seed_transpiler=42
    )

    return otimizado
```

### 6.1 Parâmetros utilizados

| Parâmetro | Função |
|---|---|
| `circuito` | Circuito quântico original. |
| `conectividade` | Define as conexões permitidas entre os qubits físicos. |
| `layout_inicial` | Permite definir o mapeamento inicial dos qubits. |
| `nivel_otimizacao` | Controla o esforço de otimização, de 0 a 3. |
| `portas_nativas` | Define o conjunto de portas utilizado na tradução. |
| `layout_method` | Define o método utilizado para selecionar o layout. |
| `routing_method` | Define o método de roteamento. |
| `seed_transpiler` | Controla a aleatoriedade dos estágios estocásticos. |

### 6.2 Escolhas da implementação atual

A implementação possui algumas decisões específicas:

**Layout**

Quando `layout_inicial` não é informado, utiliza:

```python
layout_method="sabre"
```

Assim, o Qiskit utiliza o método Sabre para auxiliar na escolha do mapeamento inicial.

Quando um layout inicial é fornecido, o parâmetro `layout_method` recebe `None`, permitindo que o Qiskit utilize seu comportamento padrão para essa etapa.

**Roteamento**

A implementação utiliza:

```python
routing_method="basic"
```

Esse método utiliza uma estratégia gulosa para inserir SWAPs conforme as operações são processadas.

Embora seja uma opção válida, o método `basic` geralmente produz resultados de qualidade inferior aos métodos heurísticos mais avançados.

O método `sabre` é uma alternativa importante para comparação, pois procura reduzir a quantidade de SWAPs inseridos.

**Reprodutibilidade**

A utilização de:

```python
seed_transpiler=42
```

ajuda a tornar os resultados reproduzíveis quando os mesmos parâmetros e ambiente são utilizados.

Entretanto, a mesma seed não garante resultados idênticos entre diferentes versões do Qiskit ou ambientes computacionais.

---

## 7. Análise da adaptação ao hardware

Após adaptar o circuito, é importante avaliar o resultado.

No projeto, essa responsabilidade pertence à função:

```python
analisar_adaptacao_hardware()
```

Ela compara o circuito original com o circuito adaptado.

Entre as informações retornadas estão:

- Métricas do circuito original.
- Métricas do circuito adaptado.
- Diferença na quantidade de operações.
- Diferença na profundidade.
- Resultado da verificação de equivalência.
- Compatibilidade com a lista de portas informada.

### 7.1 Diferença de operações

A função calcula:

\[
\Delta O = O_{adaptado} - O_{original}
\]

Onde:

- \(O_{adaptado}\) representa a quantidade de operações após a adaptação.
- \(O_{original}\) representa a quantidade de operações do circuito original.

Interpretação:

- Resultado negativo: houve redução de operações.
- Resultado positivo: houve aumento de operações.
- Resultado igual a zero: a quantidade permaneceu igual.

### 7.2 Diferença de profundidade

A profundidade também é comparada:

\[
\Delta D = D_{adaptado} - D_{original}
\]

Uma profundidade maior pode indicar que as restrições do hardware exigiram operações adicionais ou reduziram o paralelismo possível.

Uma profundidade menor pode indicar que a transformação encontrou uma organização mais eficiente.

É importante lembrar que profundidade não representa diretamente o tempo real de execução do processador.

### 7.3 Verificação de equivalência

Uma adaptação precisa preservar o comportamento quântico do circuito.

Por isso, o projeto utiliza `verificar_equivalencia()` para comparar os circuitos.

Essa função utiliza `Operator.from_circuit()` para verificar a equivalência de circuitos unitários.

A verificação é importante porque um circuito com menos operações não é necessariamente uma implementação correta do circuito original.

**Atenção:** a implementação atual possui limitações nessa comparação. Ela retorna `False` diretamente quando os circuitos possuem quantidades diferentes de qubits. Portanto, uma adaptação que altere a largura do circuito pode ser classificada como não equivalente sem que isso represente, por si só, uma prova de incorreção semântica.

Além disso, a comparação deve considerar corretamente as permutações de layout inicial e final produzidas pela transpilação.

A função atual não deve ser tratada como um verificador universal de equivalência para qualquer circuito físico.

---

## 8. Limitações importantes da implementação atual

A função `otimizar_para_hardware()` representa uma adaptação baseada em duas restrições principais:

1. Conectividade entre os qubits.
2. Conjunto de portas informado.

Isso é suficiente para experimentos e demonstrações de topologias hipotéticas, mas não representa todas as características de um processador quântico real.

### 8.1 Ausência de Backend ou Target

A implementação não recebe um objeto `backend` ou `Target`.

Consequentemente, não considera diretamente informações específicas de um dispositivo, como:

- Calibração dos qubits.
- Taxas de erro das portas.
- Tempos de execução.
- Disponibilidade de operações por qubit ou par de qubits.

Para uma adaptação mais próxima de um hardware real, o uso de um backend ou `Target` é uma alternativa mais completa.

### 8.2 Contagem de portas SWAP

Na demonstração atual, existe uma verificação semelhante a:

```python
adaptado.count_ops().get("swap", 0)
```

Entretanto, essa contagem precisa ser interpretada com cuidado.

Como o projeto informa:

```python
portas_nativas = ["rz", "sx", "x", "cx"]
```

a porta SWAP não faz parte do conjunto de portas utilizado na tradução.

Assim, uma SWAP inserida durante o roteamento pode ser decomposta em outras operações, principalmente CNOTs.

Nesse caso, a contagem final de portas SWAP pode retornar zero mesmo que o roteamento tenha utilizado operações SWAP internamente.

Portanto, não é correto utilizar somente essa contagem como prova de que nenhuma SWAP foi necessária.

### 8.3 Verificação das portas permitidas

A implementação atual verifica a compatibilidade utilizando os nomes retornados por `count_ops()`.

Essa abordagem funciona como uma verificação simplificada, mas precisa ser ampliada para circuitos reais.

Por exemplo, instruções como `measure`, `reset` e `delay` podem fazer parte da execução de um hardware sem estarem presentes na lista de portas quânticas utilizada em `basis_gates`.

Uma verificação mais completa deve considerar as instruções realmente suportadas pelo backend ou pelo `Target`.

---

## 9. Exemplo prático de adaptação

O exemplo abaixo cria um circuito de três qubits e o adapta a uma topologia linear.

O circuito possui interações entre diferentes pares de qubits, permitindo observar como a conectividade influencia a transpilação.

```python
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap

from qiskit_service import (
    otimizar_para_hardware,
    analisar_adaptacao_hardware
)

# Criar circuito original
circuito = QuantumCircuit(3)

circuito.h(0)
circuito.cx(0, 1)
circuito.cx(1, 2)
circuito.cx(0, 2)

# Criar hardware hipotético com três qubits em linha
conectividade = CouplingMap.from_line(3)

# Definir portas permitidas
portas_nativas = ["rz", "sx", "x", "cx"]

# Adaptar circuito ao hardware
adaptado = otimizar_para_hardware(
    circuito,
    conectividade,
    nivel_otimizacao=0,
    portas_nativas=portas_nativas
)

# Exibir resultados
print("Conexões do hardware:")
print(conectividade.get_edges())

print("\nCircuito original:")
print(circuito.draw())

print("\nCircuito adaptado:")
print(adaptado.draw())

print("\nMétricas da adaptação:")
print(analisar_adaptacao_hardware(
    circuito,
    adaptado,
    portas_nativas
))
```

A saída pode variar conforme o algoritmo de layout, roteamento, versão do Qiskit e parâmetros utilizados.

O objetivo do exemplo não é obter uma quantidade fixa de operações, mas observar como as restrições físicas influenciam o circuito resultante.

---

## 10. Recomendações para o projeto

Para melhorar a qualidade da adaptação ao hardware, algumas possibilidades podem ser exploradas futuramente:

1. Comparar `routing_method="basic"` com `routing_method="sabre"`.
2. Comparar diferentes layouts iniciais.
3. Avaliar a quantidade total de operações e a profundidade após a adaptação.
4. Analisar corretamente as permutações de layout inicial e final.
5. Utilizar `Target` ou um backend quando for necessário representar um processador específico.
6. Melhorar a verificação de equivalência para considerar circuitos com diferentes larguras físicas.
7. Avaliar a compatibilidade das instruções utilizando as características completas do hardware.

Essas melhorias podem ajudar a produzir circuitos mais eficientes e adequados às restrições dos processadores quânticos.

---

## 11. Resumo

A conectividade de hardware é um fator fundamental na execução de circuitos quânticos.

Um circuito pode ser matematicamente correto e, mesmo assim, não ser diretamente executável em determinado processador.

O processo de adaptação precisa considerar:

- **CouplingMap:** representa as conexões disponíveis entre os qubits físicos.
- **Layout:** associa os qubits virtuais às posições físicas.
- **Routing:** adapta as operações às conexões disponíveis.
- **SWAP:** permite reorganizar os estados entre qubits físicos conectados.
- **Basis Gates:** define as portas utilizadas na tradução do circuito.
- **Transpile:** executa as transformações necessárias para atender às restrições informadas.

No projeto, esses conceitos são aplicados pela função `otimizar_para_hardware()`, enquanto `analisar_adaptacao_hardware()` permite avaliar as mudanças produzidas no circuito.

O principal objetivo é adaptar circuitos quânticos sem perder sua funcionalidade, considerando as limitações físicas do hardware.

---

## 12. Referências

### Documentação oficial

- [IBM Quantum — Transpilation](https://quantum.cloud.ibm.com/docs/en/qiskit/transpile)
- [IBM Quantum — Transpiler Stages](https://quantum.cloud.ibm.com/docs/en/qiskit/transpiler-stages)
- [IBM Quantum — CouplingMap API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.5/qiskit.transpiler.CouplingMap)
- [IBM Quantum — Compiler API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.5/compiler)
- [IBM Quantum — Operator API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.5/qiskit.quantum_info.Operator)

### Implementação do projeto

- [Repositório do projeto — qiskit_service.py](https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/qiskit_service.py)
- [Repositório do projeto — demonstracao_qiskit.py](https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/demonstracao_qiskit.py)
