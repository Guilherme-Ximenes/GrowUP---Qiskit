# DOC05 — Simulação e Medição de Circuitos Quânticos

## Objetivo

Este documento apresenta os conceitos e as ferramentas do Qiskit utilizados para simular circuitos quânticos, calcular probabilidades de medição e analisar resultados obtidos por amostragem.

O objetivo é compreender a diferença entre o estado quântico ideal de um circuito e os resultados observados após sua execução com uma quantidade limitada de medições (_shots_).

Os conceitos aqui apresentados complementam o DOC04: enquanto aquele documento trata da adaptação de um circuito às restrições do hardware, este trata de como simular o circuito, medi-lo e interpretar os resultados.

O conteúdo aborda:

- Simulação de estados quânticos com `Statevector`.
- Cálculo de probabilidades teóricas.
- Medição de circuitos quânticos.
- Execução com diferentes quantidades de shots.
- Utilização de `StatevectorSampler`.
- Simulação com `AerSimulator`.
- Comparação entre probabilidades teóricas e resultados simulados.

---

## 1. Estado ideal e resultados amostrados

Ao estudar um circuito quântico, existem duas visões distintas:

| Visão                 | Ferramenta                           | O que representa                                       |
| --------------------- | ------------------------------------ | ------------------------------------------------------ |
| Estado ideal          | `Statevector`                        | O vetor de amplitudes do circuito, sem medição.        |
| Resultados amostrados | `StatevectorSampler`, `AerSimulator` | Contagens obtidas ao medir o circuito repetidas vezes. |

Um circuito pode ser matematicamente descrito por seu estado ideal, mas o que se observa em um experimento são apenas amostras desse estado.

Compreender essa diferença é a base de todo o restante do documento.

---

## 2. Simulação de estados quânticos com Statevector

### 2.1 O que é Statevector?

Um estado quântico pode ser representado matematicamente por um vetor de amplitudes complexas, chamado _statevector_.

Para um sistema com n qubits, o vetor possui:

\[
2^n
\]

amplitudes complexas.

Por exemplo, um sistema de dois qubits possui quatro amplitudes:

\[
|\psi\rangle =
\begin{bmatrix}
\alpha*{00}\\
\alpha*{01}\\
\alpha*{10}\\
\alpha*{11}
\end{bmatrix}
\]

Cada amplitude representa a contribuição de um estado da base computacional.

A soma dos módulos quadrados das amplitudes deve ser igual a 1:

\[
\sum_i |\alpha_i|^2 = 1
\]

Essa propriedade é chamada de normalização do estado quântico.

No Qiskit, a classe `Statevector`, disponível em `qiskit.quantum_info`, permite representar e analisar esses estados.

### 2.2 Criando um Statevector a partir de um circuito

A função `Statevector.from_instruction()` recebe uma instrução ou circuito e calcula o estado quântico resultante, considerando que todos os qubits começam em \(|0\rangle\).

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

estado = Statevector.from_instruction(circuito)

print(estado)
```

Nesse exemplo:

1. São criados dois qubits.
2. A porta Hadamard é aplicada ao primeiro qubit.
3. A porta CNOT é aplicada, utilizando o primeiro qubit como controle e o segundo como alvo.
4. O estado resultante é calculado e armazenado em `estado`.

O circuito prepara um estado de Bell:

\[
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

O resultado contém duas amplitudes não nulas, correspondentes aos estados \(|00\rangle\) e \(|11\rangle\).

### 2.3 Limitações do Statevector

O `Statevector` representa o estado quântico ideal e não corresponde a uma execução física com medições reais.

Além disso:

- Não representa diretamente a frequência de resultados obtidos em diferentes shots.
- Não simula automaticamente ruídos físicos de um dispositivo.
- Não aceita operações não unitárias, como medições, durante a construção do estado por `from_instruction()`.
- Seu custo de memória cresce exponencialmente com o número de qubits.

Portanto, o `Statevector` é especialmente útil para estudar o comportamento matemático de circuitos pequenos e verificar seus resultados ideais.

---

## 3. Cálculo de probabilidades teóricas

### 3.1 Relação entre amplitudes e probabilidades

A probabilidade de medir determinado estado da base computacional é obtida pelo módulo quadrado de sua amplitude.

Se uma amplitude é representada por:

\[
\alpha = a + bi
\]

sua probabilidade é:

\[
P = |\alpha|^2 = a^2+b^2
\]

No caso do estado de Bell:

\[
P(00)=\frac{1}{2}
\qquad
P(11)=\frac{1}{2}
\]

Os demais resultados possuem probabilidade zero.

Isso significa que uma medição individual pode produzir `00` ou `11`, mas nunca `01` ou `10`, considerando o circuito ideal.

### 3.2 Obtendo probabilidades com Qiskit

A classe `Statevector` possui o método `probabilities_dict()`, que retorna um dicionário associando cada resultado da base computacional à sua probabilidade.

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

estado = Statevector.from_instruction(circuito)

probabilidades = estado.probabilities_dict()

print(probabilidades)
```

O resultado esperado é equivalente a:

```python
{
    '00': 0.5,
    '11': 0.5
}
```

A ordem das chaves segue a convenção de representação de bits do Qiskit (ver seção 9.4).

### 3.3 Probabilidades de qubits específicos

O método `probabilities()` também permite calcular probabilidades considerando apenas determinados qubits.

```python
probabilidades_q0 = estado.probabilities([0])

probabilidades_q1 = estado.probabilities([1])

print("Qubit 0:", probabilidades_q0)
print("Qubit 1:", probabilidades_q1)
```

Essa funcionalidade é útil quando o objetivo é analisar o comportamento individual de um qubit sem considerar diretamente todos os resultados do sistema.

---

## 4. Medição de circuitos quânticos

### 4.1 O que é uma medição?

A medição é o processo pelo qual informações sobre um estado quântico são obtidas.

Diferentemente de uma operação unitária, a medição produz um resultado clássico e altera o estado quântico de acordo com o resultado observado.

Para um qubit no estado:

\[
|\psi\rangle = \alpha|0\rangle+\beta|1\rangle
\]

as probabilidades de medição na base computacional são:

\[
P(0)=|\alpha|^2
\qquad
P(1)=|\beta|^2
\]

Após a medição, o resultado é armazenado em um bit clássico.

### 4.2 Registradores clássicos

No Qiskit, os circuitos podem possuir registradores quânticos e clássicos:

- `QuantumRegister`: representa os qubits.
- `ClassicalRegister`: representa os bits clássicos utilizados para armazenar resultados de medições.

A classe `QuantumCircuit` também permite criar esses registradores diretamente por meio de seus argumentos.

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2, 2)

circuito.h(0)
circuito.cx(0, 1)

circuito.measure([0, 1], [0, 1])

print(circuito.draw())
```

Nesse exemplo:

1. São criados dois qubits.
2. São criados dois bits clássicos.
3. O circuito prepara um estado de Bell.
4. Os qubits são medidos.
5. Os resultados são armazenados nos bits clássicos correspondentes.

### 4.3 measure_all()

O método `measure_all()` adiciona medições para todos os qubits e cria um registrador clássico para armazenar os resultados.

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

circuito.measure_all()

print(circuito.draw())
```

Essa abordagem é prática quando todos os qubits precisam ser medidos.

| Método          | Qubits medidos          | Destino dos resultados                                |
| --------------- | ----------------------- | ----------------------------------------------------- |
| `measure()`     | Definidos pelo usuário. | Bits clássicos escolhidos pelo usuário.               |
| `measure_all()` | Todos.                  | Registrador clássico criado automaticamente (`meas`). |

---

## 5. Shots e amostragem de resultados

### 5.1 O que são shots?

Um _shot_ representa uma execução individual do circuito para obtenção de um resultado de medição.

Como os resultados quânticos são probabilísticos, uma única execução não é suficiente para conhecer a distribuição de probabilidades de um circuito. Por isso, o circuito é executado repetidas vezes.

- 100 shots: 100 execuções.
- 1.000 shots: 1.000 execuções.
- 10.000 shots: 10.000 execuções.

Quanto maior a quantidade de shots, maior tende a ser a precisão estatística das frequências observadas em relação às probabilidades teóricas.

Entretanto, aumentar os shots não elimina erros sistemáticos ou ruídos presentes em uma simulação com modelo de ruído ou em um dispositivo físico.

### 5.2 Frequência observada

A frequência relativa de um resultado é calculada pela divisão entre a quantidade de vezes que ele apareceu e o número total de shots:

\[
F(x)=\frac{N(x)}{N\_{\text{shots}}}
\]

Onde:

- \(F(x)\): frequência relativa do resultado.
- \(N(x)\): quantidade de ocorrências do resultado.
- \(N\_{\text{shots}}\): quantidade total de execuções.

Por exemplo, se o resultado `00` aparece 510 vezes em 1.000 shots:

\[
F(00)=\frac{510}{1000}=0{,}51
\]

Sua frequência observada é de 51%, que pode ser comparada à probabilidade teórica de 50%.

A diferença ocorre devido à natureza probabilística da amostragem.

---

## 6. Utilização do StatevectorSampler

### 6.1 O que é StatevectorSampler?

O `StatevectorSampler` é uma implementação de referência da interface Sampler V2 do Qiskit.

Ele utiliza simulação baseada em statevector para obter resultados de circuitos medidos por amostragem.

Diferentemente do uso direto de `Statevector`, o Sampler trabalha com circuitos que possuem medições e retorna resultados amostrados.

É importante não confundir:

- `Statevector`: calcula o estado quântico ideal.
- `StatevectorSampler`: utiliza o estado ideal para produzir resultados de medição por amostragem.

### 6.2 Executando um circuito com StatevectorSampler

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

circuito.measure_all()

sampler = StatevectorSampler(seed=42)

job = sampler.run([circuito], shots=1000)

resultado = job.result()

contagens = resultado[0].data.meas.get_counts()

print(contagens)
```

Nesse exemplo:

1. É criado um circuito de dois qubits.
2. O estado de Bell é preparado.
3. Todos os qubits são medidos.
4. O `StatevectorSampler` é instanciado com uma semente para reprodutibilidade da amostragem.
5. O circuito é executado com 1.000 shots.
6. O resultado é obtido por meio de `job.result()`.
7. `get_counts()` retorna a quantidade de ocorrências de cada resultado.

O resultado esperado apresenta apenas as combinações `00` e `11`, com frequências próximas de 500 ocorrências para cada uma. A distribuição exata pode variar conforme a amostragem.

### 6.3 Entendendo os resultados

A expressão:

```python
resultado[0].data.meas.get_counts()
```

pode ser dividida em partes:

| Trecho          | Função                                                                               |
| --------------- | ------------------------------------------------------------------------------------ |
| `resultado[0]`  | Acessa o resultado do primeiro circuito enviado ao Sampler.                          |
| `.data`         | Acessa os dados produzidos pelo circuito.                                            |
| `.meas`         | Acessa o registrador clássico criado por `measure_all()`, cujo nome padrão é `meas`. |
| `.get_counts()` | Retorna a quantidade de ocorrências de cada bitstring.                               |

**Atenção:** o nome do registrador depende de como o circuito foi construído. Se forem utilizados registradores clássicos com outros nomes, o acesso aos dados deverá considerar esses nomes.

### 6.4 Alterando a quantidade de shots

A quantidade de shots pode ser modificada diretamente na chamada de `run()`:

```python
resultado_100 = sampler.run(
    [circuito],
    shots=100
).result()

resultado_1000 = sampler.run(
    [circuito],
    shots=1000
).result()

resultado_10000 = sampler.run(
    [circuito],
    shots=10000
).result()

print("100 shots:")
print(resultado_100[0].data.meas.get_counts())

print("1000 shots:")
print(resultado_1000[0].data.meas.get_counts())

print("10000 shots:")
print(resultado_10000[0].data.meas.get_counts())
```

Esse experimento permite observar como a distribuição de resultados tende a se aproximar das probabilidades teóricas quando a quantidade de shots aumenta.

A semente controla a aleatoriedade da amostragem para facilitar a reprodução de experimentos. Ela não significa que os resultados serão exatamente iguais entre diferentes quantidades de shots.

---

## 7. Simulação com AerSimulator

### 7.1 O que é AerSimulator?

O `AerSimulator` pertence ao pacote Qiskit Aer e fornece recursos de simulação de circuitos quânticos.

Ele permite executar circuitos e obter resultados de medições por meio de um backend de simulação, com suporte a diferentes métodos de simulação e configurações de ruído.

Enquanto o `StatevectorSampler` é uma implementação de referência do Sampler V2 baseada em statevector, o `AerSimulator` oferece uma interface de backend e recursos adicionais para simulações.

### 7.2 Executando um circuito com AerSimulator

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

circuito.measure_all()

simulador = AerSimulator()

circuito_transpilado = transpile(
    circuito,
    simulador
)

resultado = simulador.run(
    circuito_transpilado,
    shots=1000
).result()

contagens = resultado.get_counts(circuito_transpilado)

print(contagens)
```

Etapas:

1. O circuito é construído.
2. As medições são adicionadas.
3. O `AerSimulator` é instanciado.
4. O circuito é transpilado para o simulador.
5. O circuito é executado com 1.000 shots.
6. O resultado é recuperado.
7. `get_counts()` apresenta as frequências observadas.

### 7.3 Quando utilizar AerSimulator?

O `AerSimulator` é indicado quando se deseja:

- Executar circuitos em um backend de simulação.
- Trabalhar com diferentes métodos de simulação.
- Estudar efeitos de ruído por meio de modelos configurados.
- Comparar resultados de circuitos ideais e simulados com ruído.
- Desenvolver experimentos locais sem acesso a um computador quântico físico.

A utilização de um simulador não significa que o circuito foi executado em hardware quântico real.

### 7.4 Comparação entre as ferramentas

| Ferramenta           | Entrada                            | Saída                        | Uso principal                          |
| -------------------- | ---------------------------------- | ---------------------------- | -------------------------------------- |
| `Statevector`        | Circuito sem medições.             | Amplitudes e probabilidades. | Análise do estado ideal.               |
| `StatevectorSampler` | Circuito com medições.             | Contagens amostradas.        | Amostragem ideal (Sampler V2).         |
| `AerSimulator`       | Circuito com medições transpilado. | Contagens amostradas.        | Backend de simulação, métodos e ruído. |

---

## 8. Comparação entre probabilidades teóricas e resultados simulados

### 8.1 Por que comparar?

A comparação entre probabilidades teóricas e frequências observadas permite verificar se os resultados obtidos pela simulação estão de acordo com o comportamento esperado do circuito.

- A probabilidade teórica é calculada a partir do estado quântico ideal.
- A frequência observada é obtida por meio das medições realizadas durante os shots.

Esses valores podem ser diferentes devido à amostragem finita.

### 8.2 Exemplo de comparação

Considere novamente o estado de Bell:

\[
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

As probabilidades teóricas são:

| Resultado | Probabilidade teórica |
| --------- | --------------------: |
| 00        |                   50% |
| 01        |                    0% |
| 10        |                    0% |
| 11        |                   50% |

Suponha que, após 1.000 shots, o simulador retorne:

| Resultado | Ocorrências | Frequência |
| --------- | ----------: | ---------: |
| 00        |         510 |        51% |
| 01        |           0 |         0% |
| 10        |           0 |         0% |
| 11        |         490 |        49% |

A distribuição observada está próxima da distribuição teórica.

A diferença entre 51% e 50% não representa necessariamente um erro no circuito. É uma variação esperada em uma amostragem probabilística finita.

### 8.3 Implementando a comparação em Python

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

# Construção do circuito
circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

# Cálculo das probabilidades teóricas
estado = Statevector.from_instruction(circuito)

probabilidades = estado.probabilities_dict()

# Adicionando medições
circuito.measure_all()

# Execução por amostragem
sampler = StatevectorSampler(seed=42)

resultado = sampler.run(
    [circuito],
    shots=1000
).result()

contagens = resultado[0].data.meas.get_counts()

# Comparação
total_shots = sum(contagens.values())

print("Comparação dos resultados:\n")

for estado_qubit, probabilidade in probabilidades.items():

    ocorrencias = contagens.get(estado_qubit, 0)

    frequencia = ocorrencias / total_shots

    print(f"Estado: {estado_qubit}")
    print(f"Probabilidade teórica: {probabilidade:.3f}")
    print(f"Frequência observada: {frequencia:.3f}")
    print("-" * 30)
```

O código realiza duas análises distintas:

1. Calcula as probabilidades teóricas antes da medição.
2. Obtém as frequências observadas depois da execução com shots.

Em seguida, compara os valores correspondentes para cada estado.

**Atenção:** o exemplo considera um circuito simples, sem ruído, e medições na base computacional. Para circuitos com outros registradores clássicos ou mapeamentos de medição, é necessário adaptar a correspondência entre as chaves de resultados e os estados teóricos.

---

## 9. Limitações e cuidados importantes

### 9.1 Crescimento exponencial do Statevector

O número de amplitudes cresce exponencialmente conforme a quantidade de qubits aumenta.

| Qubits |       Amplitudes |
| -----: | ---------------: |
|      2 |                4 |
|     10 |            1.024 |
|     20 |        1.048.576 |
|     30 | Mais de 1 bilhão |

Isso significa que a simulação completa por statevector pode exigir quantidades elevadas de memória e processamento.

### 9.2 Simulação ideal não representa hardware real

O `Statevector` e o `StatevectorSampler` utilizam uma representação ideal do estado quântico.

Eles não reproduzem automaticamente as imperfeições de um dispositivo físico, como:

- Erros de portas.
- Decoerência.
- Erros de leitura.
- Ruídos ambientais.

Para estudar esses efeitos, é necessário configurar modelos de ruído e utilizar recursos apropriados, como os oferecidos pelo Qiskit Aer.

### 9.3 Diferença entre probabilidade e frequência

Probabilidade teórica e frequência observada não são conceitos equivalentes.

- A probabilidade representa o comportamento matemático esperado do sistema.
- A frequência representa o resultado efetivamente observado em uma quantidade finita de execuções.

Mesmo em uma simulação ideal, as frequências podem variar entre execuções devido à amostragem.

### 9.4 Ordem dos bits

O Qiskit utiliza convenções próprias de ordenação de bits.

Em strings de resultados, o bit mais significativo aparece à esquerda, enquanto o bit de índice 0 aparece à direita.

Por exemplo, para dois qubits, o resultado:

```text
10
```

representa o qubit 1 no estado 1 e o qubit 0 no estado 0.

Essa convenção deve ser considerada ao comparar resultados, interpretar medições e analisar circuitos.

### 9.5 Medições e Statevector

Um circuito que contém operações de medição não deve ser passado diretamente para `Statevector.from_instruction()` como se fosse um circuito unitário.

A medição é uma operação não unitária e não pode ser tratada como uma evolução unitária comum do estado.

Uma abordagem adequada é calcular o estado com a parte unitária do circuito e, separadamente, executar a versão medida com um Sampler ou backend de simulação, como feito no exemplo da seção 8.3.

---

## 10. Recomendações para desenvolvimento e análise

Para utilizar corretamente os recursos apresentados, recomenda-se:

1. Utilizar `Statevector` para analisar estados quânticos ideais e calcular probabilidades teóricas.
2. Utilizar `StatevectorSampler` para estudar resultados de medições por amostragem em circuitos ideais.
3. Utilizar `AerSimulator` quando for necessário trabalhar com um backend de simulação ou modelos de ruído.
4. Comparar resultados com diferentes quantidades de shots.
5. Registrar a semente utilizada nos experimentos quando a reprodutibilidade for importante.
6. Considerar a ordenação de bits ao interpretar resultados.
7. Separar claramente simulação ideal, simulação com ruído e execução em hardware real.
8. Considerar o custo exponencial de memória e processamento ao utilizar statevectors em circuitos maiores.

### Possibilidades de evolução

O componente Qiskit pode ser ampliado futuramente com:

- Comparação automatizada entre diferentes quantidades de shots.
- Cálculo de erros entre probabilidades teóricas e frequências observadas.
- Construção de histogramas de resultados.
- Simulações com modelos de ruído.
- Análise de erros de medição.
- Comparação entre diferentes métodos de simulação.
- Avaliação de circuitos em backends físicos, incluindo circuitos adaptados conforme o DOC04.

---

## 11. Resumo

Neste documento foram apresentados os principais recursos do Qiskit para simulação e medição de circuitos quânticos.

Os conceitos fundamentais são:

- **Statevector:** representa o estado quântico e permite calcular probabilidades teóricas.
- **probabilities_dict():** retorna as probabilidades dos estados da base computacional.
- **measure() e measure_all():** adicionam operações de medição aos circuitos.
- **Shots:** representam execuções individuais utilizadas para obter resultados por amostragem.
- **StatevectorSampler:** realiza amostragem de resultados utilizando simulação ideal baseada em statevector.
- **AerSimulator:** fornece um backend de simulação com suporte a diferentes métodos e configurações.
- **Comparação entre probabilidades e frequências:** permite analisar a diferença entre o comportamento matemático esperado e os resultados amostrados.

A compreensão desses recursos é essencial para analisar o comportamento de circuitos quânticos, validar resultados e desenvolver experimentos de simulação.

---

## 12. Referências

- [IBM Quantum — Statevector API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector)
- [IBM Quantum — Exact Simulation with Qiskit SDK Primitives](https://quantum.cloud.ibm.com/docs/en/qiskit/simulate-with-qiskit-sdk-primitives)
- [IBM Quantum — Introduction to Primitives](https://qiskit.qotlabs.org/docs/guides/primitives)
- [Qiskit Aer — AerSimulator Documentation and Tutorials](https://qiskit.github.io/qiskit-aer/tutorials/1_aersimulator.html)
- [Qiskit Aer — GitHub Repository](https://github.com/Qiskit/qiskit-aer)
