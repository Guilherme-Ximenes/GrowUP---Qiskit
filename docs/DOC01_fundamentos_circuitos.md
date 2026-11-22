# DOC01 — Fundamentos de Circuitos Quânticos

**Projeto:** GrowUp — Módulo Qiskit  
**Tema:** Fundamentos de circuitos quânticos  
**Compatibilidade:** Qiskit 2.6.0  
**Objetivo:** Apresentar os conceitos fundamentais para construção, interpretação e análise de circuitos quânticos utilizando Qiskit.

---

## 1. Introdução à computação quântica

A computação quântica utiliza princípios da mecânica quântica para processar informações. Sua unidade básica de informação é o **qubit**, que apresenta propriedades diferentes das unidades de informação da computação clássica.

Entre os principais conceitos necessários para compreender circuitos quânticos estão:

- Qubit e estados quânticos;
- Superposição;
- Portas quânticas;
- Entrelaçamento;
- Medição;
- Representação de estados por Statevector.

Esses conceitos formam a base para a construção e otimização de circuitos utilizando Qiskit.

## 2. Qubit e estados quânticos

### 2.1 O que é um qubit?

O qubit é a unidade fundamental de informação quântica.

Enquanto um bit clássico assume um valor definido entre 0 e 1, um qubit pode ser representado por uma combinação linear dos estados da base computacional:

\[
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle
\]

Em que:

- \(|0\rangle\) representa o estado zero;
- \(|1\rangle\) representa o estado um;
- \(\alpha\) e \(\beta\) são amplitudes complexas;
- \(|\alpha|^2\) representa a probabilidade de obter 0 em uma medição na base computacional;
- \(|\beta|^2\) representa a probabilidade de obter 1.

Para que o estado seja válido, suas amplitudes devem satisfazer a condição de normalização:

\[
|\alpha|^2 + |\beta|^2 = 1
\]

### 2.2 Estados da base computacional

Os estados \(|0\rangle\) e \(|1\rangle\) são chamados de estados da base computacional.

Eles podem ser representados por vetores:

\[
|0\rangle =
\begin{pmatrix}
1\\
0
\end{pmatrix}
\qquad
|1\rangle =
\begin{pmatrix}
0\\
1
\end{pmatrix}
\]

Esses estados são utilizados como referência para representar e analisar outros estados quânticos.

## 3. Superposição

A superposição ocorre quando um qubit está em uma combinação linear de estados da base computacional.

Um exemplo é:

\[
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
\]

Nesse caso, as amplitudes associadas aos estados \(|0\rangle\) e \(|1\rangle\) possuem o mesmo módulo.

Consequentemente, uma medição na base computacional apresenta:

- 50% de probabilidade de obter 0;
- 50% de probabilidade de obter 1.

A superposição não significa que o qubit armazena simultaneamente dois bits clássicos. Ela descreve um estado quântico cujas amplitudes determinam as probabilidades dos resultados possíveis de uma medição.

Também é importante distinguir uma superposição de uma distribuição clássica de probabilidades: estados quânticos possuem amplitudes e fases, que podem produzir interferência.

## 4. Circuitos quânticos no Qiskit

### 4.1 QuantumCircuit

A classe `QuantumCircuit`, disponibilizada pelo Qiskit, permite construir circuitos quânticos por meio da definição de qubits, bits clássicos e instruções.

Um circuito pode ser criado da seguinte maneira:

```python
from qiskit import QuantumCircuit

# Circuito com dois qubits
circuito = QuantumCircuit(2)

# Circuito com dois qubits e dois bits clássicos
circuito_com_medicao = QuantumCircuit(2, 2)
```

A primeira declaração cria um circuito com dois qubits.

A segunda cria um circuito com dois qubits e dois bits clássicos, permitindo armazenar resultados de medições.

As operações são adicionadas na ordem em que são chamadas.

Para visualizar um circuito:

```python
print(circuito.draw())
```

### 4.2 Portas quânticas

Portas quânticas são operações aplicadas aos qubits para modificar seus estados.

As portas unitárias são representadas matematicamente por matrizes unitárias e preservam a normalização do estado quântico.

A seguir, são apresentadas três portas fundamentais.

#### 4.2.1 Porta X — Pauli-X

A porta X realiza uma inversão entre os estados da base computacional.

Sua representação matricial é:

\[
X =
\begin{pmatrix}
0 & 1\\
1 & 0
\end{pmatrix}
\]

Suas transformações são:

\[
X|0\rangle = |1\rangle
\]

\[
X|1\rangle = |0\rangle
\]

No Qiskit:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(1)

circuito.x(0)
```

Nesse exemplo, a porta X é aplicada ao qubit de índice 0.

Considerando que o circuito começa no estado \(|0\rangle\), o resultado será \(|1\rangle\).

#### 4.2.2 Porta H — Hadamard

A porta Hadamard é utilizada para criar superposição.

Sua representação matricial é:

\[
H = \frac{1}{\sqrt{2}}
\begin{pmatrix}
1 & 1\\
1 & -1
\end{pmatrix}
\]

Quando aplicada aos estados da base computacional:

\[
H|0\rangle =
\frac{|0\rangle + |1\rangle}{\sqrt{2}}
\]

\[
H|1\rangle =
\frac{|0\rangle - |1\rangle}{\sqrt{2}}
\]

No Qiskit:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(1)

circuito.h(0)
```

Quando aplicada ao estado inicial \(|0\rangle\), a porta H produz uma superposição com probabilidades iguais para os resultados 0 e 1 em uma medição na base computacional.

#### 4.2.3 Porta CX — Controlled-X

A porta CX, também conhecida como CNOT, é uma operação controlada que atua sobre dois qubits.

Ela possui dois elementos:

- **Controle:** determina se a operação será executada.
- **Alvo:** recebe a operação X quando o qubit de controle está no estado \(|1\rangle\).

Seu comportamento na base computacional é:

- Se o controle estiver em \(|0\rangle\), o alvo permanece inalterado.
- Se o controle estiver em \(|1\rangle\), o alvo é invertido.

No Qiskit:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2)

circuito.cx(0, 1)
```

A ordem dos argumentos é importante:

- `0`: qubit de controle;
- `1`: qubit alvo.

Portanto, `cx(0, 1)` utiliza o qubit 0 como controle e o qubit 1 como alvo.

Essa convenção deve ser observada ao interpretar os diagramas e os resultados dos circuitos.

## 5. Entrelaçamento quântico

O entrelaçamento ocorre quando dois ou mais qubits apresentam correlações quânticas que não podem ser descritas como estados independentes de cada qubit.

Um exemplo é o estado de Bell:

\[
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

Esse estado pode ser preparado utilizando duas operações:

1. Aplicar uma porta H ao primeiro qubit.
2. Aplicar uma porta CX utilizando o primeiro qubit como controle e o segundo como alvo.

Exemplo no Qiskit:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

print(circuito.draw())
```

O circuito produz o estado:

\[
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

Ao medir os dois qubits na base computacional, os resultados possíveis são:

- `00`, com probabilidade de 50%;
- `11`, com probabilidade de 50%.

Os resultados `01` e `10` possuem probabilidade zero no modelo ideal.

Esse exemplo demonstra como portas quânticas podem ser combinadas para produzir estados entrelaçados.

## 6. Medição quântica

A medição permite obter informação clássica a partir de um estado quântico.

No Qiskit, a medição padrão é realizada na base computacional, também conhecida como base Z.

Para um qubit no estado:

\[
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle
\]

as probabilidades dos resultados são:

\[
P(0) = |\alpha|^2
\]

\[
P(1) = |\beta|^2
\]

Após a medição, o estado é projetado no resultado obtido.

### 6.1 Medição no Qiskit

A operação `measure(qubit, cbit)` associa a medição de um qubit a um bit clássico.

Exemplo:

```python
from qiskit import QuantumCircuit

circuito = QuantumCircuit(1, 1)

circuito.h(0)
circuito.measure(0, 0)

print(circuito.draw())
```

Nesse exemplo:

1. É criado um circuito com um qubit e um bit clássico.
2. A porta H prepara o qubit em superposição.
3. A medição registra o resultado no bit clássico de índice 0.

A construção desse circuito não executa, por si só, uma simulação ou uma execução em hardware. Para obter resultados de medições, é necessário executá-lo em um simulador ou serviço compatível.

A medição é uma operação não reversível e não deve ser confundida com uma porta unitária.

## 7. Ordenação de bits no Qiskit

O Qiskit utiliza a convenção little-endian para a representação de bits e qubits.

Isso significa que:

- O qubit 0 é o menos significativo.
- O qubit de maior índice é o mais significativo.
- Em uma string de resultados, o qubit de maior índice aparece mais à esquerda.
- O qubit 0 aparece mais à direita.

Em um circuito com dois qubits, a string representa a ordem `q1 q0`.

| Estado |  q1 |  q0 |
| ------ | --: | --: |
| `00`   |   0 |   0 |
| `01`   |   0 |   1 |
| `10`   |   1 |   0 |
| `11`   |   1 |   1 |

Por exemplo:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

circuito = QuantumCircuit(2)

circuito.x(0)

estado = Statevector.from_instruction(circuito)

print(estado.probabilities_dict())
```

O resultado esperado é:

```python
{'01': 1.0}
```

Isso ocorre porque o qubit 0 foi colocado no estado \(|1\rangle\), enquanto o qubit 1 permaneceu no estado \(|0\rangle\).

A string `01` representa `q1 = 0` e `q0 = 1`.

Essa convenção é fundamental para interpretar corretamente resultados de circuitos, Statevector e medições.

## 8. Análise de estados com Statevector

O Qiskit disponibiliza a classe `Statevector`, pertencente ao módulo `qiskit.quantum_info`, para representar e analisar estados quânticos.

O método `Statevector.from_instruction()` calcula o estado resultante de uma instrução ou circuito, considerando como entrada o estado inicial:

\[
|00...0\rangle
\]

Exemplo:

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

estado = Statevector.from_instruction(circuito)

print("Statevector:")
print(estado)

print("\nProbabilidades:")
print(estado.probabilities_dict())
```

Para o circuito apresentado, o estado esperado é:

\[
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

Consequentemente, as probabilidades esperadas são:

```python
{
    '00': 0.5,
    '11': 0.5
}
```

Pequenas diferenças de precisão numérica podem aparecer na saída.

### 8.1 probabilities_dict()

O método `probabilities_dict()` retorna um dicionário contendo as probabilidades de medição na base computacional.

Cada chave representa um estado da base e seu respectivo valor representa a probabilidade de obter aquele resultado.

Exemplo:

```python
probabilidades = estado.probabilities_dict()

print(probabilidades)
```

Também é possível utilizar o argumento `decimals` para limitar a quantidade de casas decimais:

```python
probabilidades = estado.probabilities_dict(decimals=3)
```

### 8.2 Limitações do Statevector

O Statevector representa um estado quântico puro e permite calcular sua evolução ideal por meio de instruções suportadas pelo simulador.

É importante considerar que:

- O cálculo não representa uma execução física em um processador quântico.
- O método não incorpora automaticamente ruídos de hardware.
- O cálculo do estado não utiliza shots.
- Circuitos com medições não devem ser passados diretamente para `Statevector.from_instruction()`.
- Instruções não suportadas pelo simulador de estado puro podem gerar `QiskitError`.

Além disso, a representação de um estado com \(n\) qubits exige \(2^n\) amplitudes complexas. Por isso, o custo de memória cresce exponencialmente com o número de qubits.

O Statevector é especialmente útil para analisar circuitos pequenos, verificar estados e validar comportamentos ideais.

## 9. Boas práticas

Ao desenvolver circuitos quânticos com Qiskit, recomenda-se:

1. Verificar a quantidade de qubits e bits clássicos do circuito.
2. Observar a ordem dos argumentos nas portas controladas.
3. Distinguir superposição de entrelaçamento.
4. Considerar a convenção little-endian ao interpretar strings de resultados.
5. Não confundir a construção de um circuito com sua execução.
6. Distinguir resultados ideais de simulação de resultados obtidos em hardware.
7. Verificar se as instruções utilizadas são compatíveis com o método de análise escolhido.
8. Utilizar as probabilidades e amplitudes do Statevector para validar comportamentos esperados em circuitos pequenos.

## 10. Relação com os exemplos do módulo Qiskit

Este documento estabelece a base conceitual para os seguintes exemplos:

- **EX01 — Portas X, H e CX:** aplicação de portas fundamentais e análise dos estados resultantes.
- **EX02 — Estado de Bell:** construção e análise de um estado entrelaçado.
- **EX07 — Statevector, Sampler e ordenação:** análise de estados, probabilidades e interpretação dos resultados.

Os conceitos apresentados também são necessários para compreender as etapas posteriores de transpilação, otimização, adaptação a hardware e validação de circuitos.

## 11. Referências

1. IBM Quantum Documentation — QuantumCircuit:
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit

2. IBM Quantum Documentation — Bit ordering in the Qiskit SDK:
   https://quantum.cloud.ibm.com/docs/en/qiskit/bit-ordering

3. IBM Quantum Documentation — Statevector:
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector

4. IBM Quantum Documentation — Construct circuits:
   https://quantum.cloud.ibm.com/docs/en/qiskit/construct-circuits

5. IBM Quantum Documentation — Circuit conventions:
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/circuit

---

**Projeto:** GrowUp — Módulo Qiskit  
**Documento:** DOC01  
**Tema:** Fundamentos de Circuitos Quânticos
