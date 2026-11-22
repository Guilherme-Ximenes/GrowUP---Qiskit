# DOC03 — Transpilação e Otimização de Circuitos Quânticos

**Projeto:** GrowUp — Módulo Qiskit  
**Tema:** Transpilação e otimização de circuitos quânticos  
**Compatibilidade:** Qiskit 2.6.0  
**Objetivo:** Explicar o processo de transpilação, os níveis de otimização do Qiskit e a utilização dessas ferramentas para melhorar circuitos quânticos, preservando seu comportamento.

---

## 1. Introdução à transpilação

A transpilação é o processo de transformar um circuito quântico em outra representação, buscando adequá-lo às instruções e às restrições de execução de um determinado ambiente.

Um circuito quântico pode ser construído utilizando diversas portas e operações disponíveis no Qiskit. Entretanto, um processador quântico real possui limitações específicas, como:

- Conjunto limitado de portas nativas;
- Restrições de conectividade entre qubits;
- Diferentes características físicas das operações;
- Limitações relacionadas ao ruído e às taxas de erro.

O transpilador do Qiskit transforma os circuitos para atender às restrições informadas e pode aplicar otimizações para reduzir sua complexidade estrutural.

Entre os principais objetivos da transpilação estão:

1. Decompor operações em instruções suportadas;
2. Adaptar circuitos à conectividade do hardware;
3. Reduzir operações redundantes;
4. Diminuir a profundidade do circuito;
5. Melhorar a estrutura das instruções utilizadas.

É importante compreender que transpilação e otimização estão relacionadas, mas não são sinônimos.

A transpilação é o processo mais amplo de transformação do circuito. A otimização é uma das atividades que podem ocorrer durante esse processo.

## 2. Função transpile()

O Qiskit disponibiliza a função `transpile()` para realizar a transpilação de circuitos.

Ela pode receber um circuito e parâmetros que determinam como a transformação será realizada.

Exemplo básico:

```python
from qiskit import QuantumCircuit, transpile

circuito = QuantumCircuit(2)

circuito.x(0)
circuito.x(0)
circuito.h(1)
circuito.cx(0, 1)

circuito_otimizado = transpile(
    circuito,
    optimization_level=3
)

print("Circuito original:")
print(circuito.draw())

print("\nCircuito transpilado:")
print(circuito_otimizado.draw())
```

Nesse exemplo:

1. É criado um circuito com dois qubits.
2. São adicionadas algumas operações.
3. A função `transpile()` recebe o circuito original.
4. O nível de otimização 3 é utilizado.
5. O resultado é armazenado em um novo objeto `QuantumCircuit`.

A função retorna o circuito transpilado, sem substituir diretamente o objeto original.

A quantidade de operações e a profundidade podem mudar durante esse processo.

Entretanto, não se deve presumir que todo circuito será necessariamente reduzido. O resultado depende da estrutura do circuito, dos parâmetros utilizados e das restrições de compilação.

## 3. Níveis de otimização

O Qiskit disponibiliza quatro níveis de otimização, identificados pelos valores de 0 a 3.

O parâmetro `optimization_level` determina o esforço e as estratégias utilizadas pelo transpilador durante a compilação.

Os níveis são:

| Nível | Descrição                           |
| ----- | ----------------------------------- |
| 0     | Sem esforço adicional de otimização |
| 1     | Otimização leve                     |
| 2     | Otimização de esforço intermediário |
| 3     | Otimização mais intensa             |

### 3.1 Nível 0 — Otimização mínima

O nível 0 utiliza o menor esforço de otimização.

Ele é útil quando se deseja realizar transformações básicas necessárias à compilação, sem aplicar as estratégias mais intensivas de otimização.

É importante destacar que nível 0 não significa ausência de transpilação.

O circuito ainda pode ser transformado para atender às condições de compilação informadas.

### 3.2 Nível 1 — Otimização leve

O nível 1 aplica estratégias de otimização relativamente simples.

Entre as possíveis transformações estão:

- Cancelamento de operações inversas consecutivas;
- Combinação de operações de um único qubit;
- Simplificação de sequências de portas.

O objetivo é melhorar a estrutura do circuito sem utilizar todo o esforço de otimização disponível.

### 3.3 Nível 2 — Otimização intermediária

O nível 2 utiliza estratégias mais elaboradas do que o nível 1.

Pode explorar relações de comutatividade entre operações e identificar oportunidades adicionais de simplificação.

A comutatividade permite reorganizar determinadas operações sem alterar o comportamento do circuito, desde que as condições matemáticas necessárias sejam respeitadas.

### 3.4 Nível 3 — Otimização intensa

O nível 3 utiliza estratégias mais intensivas de otimização.

Pode incluir:

- Análise e consolidação de blocos de operações;
- Síntese de operações unitárias;
- Otimização de decomposições;
- Estratégias mais elaboradas de simplificação.

Esse nível pode produzir circuitos mais eficientes, mas geralmente exige mais tempo de compilação.

**Importante:** utilizar um nível mais alto não garante que todas as métricas do circuito serão menores.

O resultado depende do circuito de entrada, das restrições e das estratégias aplicadas.

### 3.5 Comparação entre os níveis

Uma das formas de compreender os níveis de otimização é executar o mesmo circuito utilizando cada um deles.

Exemplo:

```python
from qiskit import QuantumCircuit, transpile

circuito = QuantumCircuit(2)

circuito.x(0)
circuito.x(0)

circuito.h(0)
circuito.h(0)

circuito.cx(0, 1)
circuito.cx(0, 1)

for nivel in range(4):

    otimizado = transpile(
        circuito,
        optimization_level=nivel,
        seed_transpiler=42
    )

    print(f"\nNível de otimização: {nivel}")
    print(otimizado.draw())
    print("Operações:", otimizado.size())
    print("Profundidade:", otimizado.depth())
    print("Tipos:", dict(otimizado.count_ops()))
```

O exemplo executa quatro transpilations, uma para cada nível.

Os resultados podem apresentar diferenças na quantidade de operações, profundidade e composição do circuito.

Não existe uma redução fixa ou garantida para cada nível. Os resultados devem ser observados e comparados para o circuito analisado.

## 4. Seed do transpilador

Algumas etapas do transpilador utilizam algoritmos estocásticos, ou seja, algoritmos que podem envolver escolhas pseudoaleatórias.

Para controlar essas escolhas, o Qiskit disponibiliza o parâmetro:

```python
seed_transpiler
```

Exemplo:

```python
from qiskit import QuantumCircuit, transpile

circuito = QuantumCircuit(3)

circuito.h(0)
circuito.cx(0, 2)
circuito.cx(0, 1)

otimizado = transpile(
    circuito,
    optimization_level=3,
    seed_transpiler=42
)
```

O valor `42` é uma semente utilizada para inicializar os geradores pseudoaleatórios envolvidos nas etapas correspondentes.

A utilização de uma semente fixa ajuda a tornar os resultados reproduzíveis em condições equivalentes.

Entretanto, isso não garante resultados idênticos entre diferentes versões do Qiskit, configurações, alvos de compilação ou ambientes.

No projeto GrowUp, a função `otimizar_circuito()` utiliza:

```python
seed_transpiler=42
```

Essa escolha busca facilitar a repetição dos testes e a comparação entre resultados.

## 5. Etapas do processo de transpilação

O transpilador do Qiskit utiliza uma estrutura modular formada por diferentes etapas.

O pipeline predefinido possui seis estágios principais:

1. `init`;
2. `layout`;
3. `routing`;
4. `translation`;
5. `optimization`;
6. `scheduling`.

Nem todos os estágios necessariamente realizam transformações em toda chamada. Seu comportamento depende dos parâmetros e das restrições fornecidas.

### 5.1 Init — Inicialização

A etapa de inicialização prepara o circuito para as etapas seguintes.

Entre suas atividades podem estar:

- Validação das instruções;
- Decomposição de operações complexas;
- Conversão de operações com vários qubits em operações menores.

Essa etapa prepara a estrutura do circuito para as transformações posteriores.

### 5.2 Layout — Mapeamento de qubits

A etapa de layout estabelece uma correspondência entre os qubits lógicos do circuito e os qubits físicos disponíveis no processador.

Os qubits lógicos representam os qubits utilizados na construção do algoritmo.

Os qubits físicos representam os recursos efetivamente existentes no hardware.

A escolha do mapeamento influencia a quantidade de operações adicionais necessárias para executar o circuito.

Um bom layout pode reduzir a necessidade de operações SWAP.

### 5.3 Routing — Roteamento

A etapa de roteamento adapta as interações entre qubits às restrições de conectividade do hardware.

Em um processador quântico, nem todos os qubits necessariamente possuem conexão direta entre si.

Quando uma operação controlada precisa ocorrer entre qubits que não são diretamente conectados, podem ser necessárias operações SWAP para aproximar os estados quânticos.

Essas operações permitem reorganizar a posição lógica dos estados no hardware.

O roteamento busca encontrar uma sequência compatível com a conectividade disponível.

A quantidade de SWAPs inseridas pode aumentar o número de operações e a profundidade do circuito.

### 5.4 Translation — Tradução de portas

A etapa de tradução transforma as operações do circuito em instruções pertencentes ao conjunto de portas suportadas pelo alvo de compilação.

Esse conjunto é conhecido como conjunto de portas nativas ou basis gates.

Por exemplo, um circuito pode utilizar uma porta SWAP, mas o hardware pode não disponibilizar essa operação diretamente.

Nesse caso, o transpilador pode decompor a SWAP em operações disponíveis no conjunto de instruções do dispositivo.

Uma decomposição comum de SWAP utiliza três portas CX:

\[
SWAP(a,b) =
CX(a,b)\ CX(b,a)\ CX(a,b)
\]

A ordem de aplicação deve ser interpretada conforme a convenção de composição das operações.

A tradução permite adaptar a representação abstrata do circuito às instruções aceitas pelo hardware.

### 5.5 Optimization — Otimização

A etapa de otimização aplica transformações destinadas a melhorar a estrutura do circuito.

Entre as possíveis estratégias estão:

- Cancelamento de portas redundantes;
- Combinação de operações;
- Simplificação de sequências;
- Reorganização de operações compatíveis;
- Síntese de blocos de operações.

O objetivo é encontrar representações mais eficientes sem alterar o comportamento que precisa ser preservado.

As estratégias utilizadas dependem do nível de otimização e das configurações do transpilador.

### 5.6 Scheduling — Escalonamento

O escalonamento organiza temporalmente as instruções do circuito, considerando as durações das operações e as restrições de tempo do hardware.

Essa etapa pode inserir instruções `Delay` para representar intervalos de espera entre operações.

O scheduling é importante para análises que consideram:

- Duração das portas;
- Tempo de execução;
- Intervalos de ociosidade dos qubits;
- Restrições temporais do dispositivo.

O estágio de scheduling não é executado por padrão em todas as chamadas. É necessário configurar o método de escalonamento apropriado.

## 6. Transpilação genérica e transpilação para hardware

É importante distinguir dois cenários.

### 6.1 Transpilação genérica

A transpilação genérica aplica as transformações disponíveis sem receber necessariamente as restrições de um processador específico.

Exemplo:

```python
from qiskit import QuantumCircuit, transpile

circuito = QuantumCircuit(2)

circuito.h(0)
circuito.cx(0, 1)

otimizado = transpile(
    circuito,
    optimization_level=3,
    seed_transpiler=42
)
```

Nesse exemplo, não foi informado um backend, Target ou mapa de conectividade específico.

Portanto, o resultado não deve ser interpretado como uma garantia de compatibilidade com determinado processador quântico.

### 6.2 Transpilação orientada a hardware

Quando são informadas as características de um hardware, o transpilador pode adaptar o circuito às suas restrições.

Entre os parâmetros utilizados estão:

- `backend`: backend de execução;
- `target`: descrição das instruções e propriedades do dispositivo;
- `basis_gates`: conjunto de portas permitidas;
- `coupling_map`: conectividade entre qubits;
- `initial_layout`: mapeamento inicial dos qubits;
- `optimization_level`: esforço de otimização.

Exemplo simplificado utilizando um mapa de conectividade:

```python
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap

circuito = QuantumCircuit(3)

circuito.h(0)
circuito.cx(0, 2)

conectividade = CouplingMap.from_line(3)

adaptado = transpile(
    circuito,
    coupling_map=conectividade,
    optimization_level=3,
    seed_transpiler=42
)

print(adaptado.draw())
```

Nesse exemplo, a conectividade representa uma topologia linear de três qubits.

A operação CX entre os qubits 0 e 2 não corresponde a uma conexão direta nessa topologia.

O transpilador precisa adaptar o circuito para respeitar as restrições informadas.

O estudo detalhado de conectividade, layout e roteamento será desenvolvido no DOC04.

## 7. Otimização no serviço Qiskit do projeto

O projeto GrowUp possui uma função própria para realizar a otimização genérica de circuitos:

```python
otimizar_circuito(circuito, nivel_otimizacao=3)
```

Essa função está implementada em `qiskit_service.py`.

Sua implementação atual é:

```python
def otimizar_circuito(
    circuito: QuantumCircuit,
    nivel_otimizacao: int = 3
):
    validar_circuito(circuito)

    if nivel_otimizacao not in (0, 1, 2, 3):
        raise ValueError(
            "Nível de otimização deve ser 0, 1, 2 ou 3."
        )

    circuito_otimizado = transpile(
        circuito,
        optimization_level=nivel_otimizacao,
        seed_transpiler=42
    )

    return circuito_otimizado
```

A função realiza as seguintes etapas:

1. Valida se a entrada é um objeto `QuantumCircuit`.
2. Verifica se o nível de otimização está entre 0 e 3.
3. Executa a função `transpile()`.
4. Utiliza a semente fixa 42.
5. Retorna o circuito transpilado.

O nível padrão definido pelo serviço é 3.

Isso significa que, quando o parâmetro não é informado, a função utiliza o nível 3.

Essa configuração é uma escolha específica do projeto. A função `transpile()` possui seu próprio comportamento padrão quando `optimization_level` não é informado, mas o serviço não depende desse padrão porque fornece explicitamente o nível.

### 7.1 Comparação dos níveis no serviço

O projeto também possui a função:

```python
comparar_niveis(circuito)
```

Ela executa a otimização do circuito utilizando os quatro níveis disponíveis.

A função:

1. Recebe o circuito original;
2. Executa a otimização nos níveis 0, 1, 2 e 3;
3. Calcula as métricas de cada resultado;
4. Tenta verificar a equivalência com o circuito original;
5. Organiza os resultados em um dicionário.

Sua estrutura de retorno contém:

```python
{
    0: {
        "metricas": {
            "qubits": 2,
            "total_operacoes": 0,
            "profundidade": 0,
            "tipos_operacoes": {}
        },
        "equivalente": True,
        "status_verificacao": "equivalente",
        "motivo": None
    }
}
```

O exemplo acima representa apenas a estrutura dos campos. Os valores das métricas dependem do circuito e do resultado da transpilação.

Os resultados são armazenados separadamente para cada nível.

### 7.2 Interpretação da equivalência

O projeto utiliza a função:

```python
verificar_equivalencia(original, otimizado)
```

para verificar se o circuito original e o circuito transpilado implementam a mesma operação unitária.

A verificação utiliza operadores unitários por meio de `Operator.from_circuit()`.

O resultado pode indicar:

- `True`: os circuitos foram considerados equivalentes;
- `False`: os circuitos não são equivalentes;
- Erro de validação: não foi possível realizar a comparação.

A função `comparar_niveis()` converte falhas de verificação em um estado específico:

```python
"status_verificacao": "nao_verificado"
```

Nesse caso, o campo `equivalente` recebe `None`, e o motivo da falha é armazenado.

**Importante:** a comparação por operadores unitários é destinada a circuitos unitários. Circuitos com medições ou operações incompatíveis com essa representação podem não ser verificáveis por esse método.

Portanto, `nao_verificado` não significa necessariamente que o circuito está incorreto. Significa que o método utilizado não conseguiu confirmar sua equivalência.

## 8. Avaliação de propostas de otimização

No projeto GrowUp, uma proposta de otimização pode ser gerada por um componente externo e posteriormente avaliada pelo serviço Qiskit.

A função:

```python
avaliar_proposta_ia(original, proposta)
```

recebe dois circuitos:

- Circuito original;
- Circuito proposto.

Ela calcula as métricas de ambos e tenta verificar a equivalência.

Entre os resultados retornados estão:

```python
{
    "original": {},
    "proposta": {},
    "equivalente": True,
    "status_verificacao": "equivalente",
    "motivo": None,
    "diferenca_operacoes": -2,
    "diferenca_profundidade": -1,
    "reduziu_operacoes": True,
    "reduziu_profundidade": True
}
```

Os valores são ilustrativos e dependem dos circuitos avaliados.

### 8.1 Cálculo das diferenças

O serviço utiliza a seguinte lógica:

\[
\Delta*{\text{operações}} =
O*{\text{proposta}} - O\_{\text{original}}
\]

\[
\Delta*{\text{profundidade}} =
D*{\text{proposta}} - D\_{\text{original}}
\]

Em que:

- \(O\) representa o total de operações;
- \(D\) representa a profundidade do circuito.

Uma diferença negativa indica redução da métrica.

Uma diferença positiva indica aumento.

Uma diferença igual a zero indica que a métrica permaneceu inalterada.

### 8.2 Quando uma redução é considerada válida?

O serviço não considera uma proposta uma otimização válida apenas porque ela possui menos operações.

Primeiro, é necessário verificar a equivalência.

A lógica atual é:

- Se a equivalência for confirmada e houver redução, a respectiva métrica recebe `True`.
- Se a equivalência for confirmada, mas não houver redução, a métrica recebe `False`.
- Se a equivalência não puder ser verificada, a métrica recebe `None`.

Exemplo:

| Equivalência   | Redução de operações                | Resultado |
| -------------- | ----------------------------------- | --------- |
| Confirmada     | Sim                                 | `True`    |
| Confirmada     | Não                                 | `False`   |
| Não verificada | Não é possível confirmar            | `None`    |
| Negada         | Não é considerada otimização válida | `False`   |

Essa validação é importante para impedir que uma proposta que remove operações necessárias seja classificada como otimização bem-sucedida.

### 8.3 Exemplo de proposta incorreta

Considere um circuito que prepara um estado de Bell:

```python
from qiskit import QuantumCircuit

original = QuantumCircuit(2)

original.h(0)
original.cx(0, 1)
```

Agora considere uma proposta que remove a porta CX:

```python
proposta = QuantumCircuit(2)

proposta.h(0)
```

A proposta possui menos operações, mas não produz o mesmo estado quântico do circuito original.

Portanto, a redução no número de operações não é suficiente para classificá-la como otimização válida.

O serviço deve identificar a diferença de comportamento por meio da verificação de equivalência.

## 9. Limitações e cuidados na otimização

A otimização de circuitos quânticos exige atenção a alguns aspectos.

### 9.1 Mais otimização não significa sempre melhor resultado

Um nível de otimização maior representa maior esforço de compilação, mas não garante que todas as métricas serão reduzidas.

É necessário comparar os resultados obtidos.

### 9.2 Otimização depende das restrições

Um circuito otimizado sem informações de hardware pode não ser a melhor representação para um processador específico.

A topologia, as portas nativas e as características físicas do dispositivo podem modificar a estratégia mais adequada.

### 9.3 A transpilação pode aumentar métricas

A tradução de portas e a inserção de SWAPs podem aumentar a quantidade de operações e a profundidade.

Isso não significa necessariamente que a transpilação falhou.

O circuito pode ter ficado maior justamente para se tornar compatível com as restrições de execução.

### 9.4 Equivalência deve ser verificada

Uma proposta que reduz operações, mas altera o comportamento do circuito, não deve ser aceita como uma otimização correta.

A validação deve considerar a equivalência e as condições de execução.

### 9.5 Resultados dependem da versão

As estratégias internas do transpilador podem mudar entre versões do Qiskit.

Por isso, comparações experimentais devem registrar a versão utilizada e os parâmetros de transpilação.

## 10. Relação com os exemplos do módulo Qiskit

Este documento estabelece a base conceitual para os seguintes exemplos:

- **EX04 — Cancelamento de portas redundantes:** demonstração de simplificações e cancelamento de operações.
- **EX05 — Transpile e níveis de otimização:** comparação dos níveis 0, 1, 2 e 3.
- **EX06 — CouplingMap, layout e roteamento:** aplicação da transpilação com restrições de conectividade.

Os conceitos apresentados também são utilizados diretamente pelas funções:

- `otimizar_circuito()`;
- `comparar_niveis()`;
- `verificar_equivalencia()`;
- `avaliar_proposta_ia()`.

## 12. Referências

### Documentação IBM Quantum

1. Introduction to transpilation:
   https://quantum.cloud.ibm.com/docs/en/qiskit/transpile

2. Transpiler stages:
   https://quantum.cloud.ibm.com/docs/en/qiskit/transpiler-stages

3. Set transpiler optimization level:
   https://quantum.cloud.ibm.com/docs/en/qiskit/set-optimization

4. Transpilation default settings and configuration options:
   https://quantum.cloud.ibm.com/docs/en/qiskit/defaults-and-configuration-options

### Implementação do projeto

5. GrowUP — Qiskit — `qiskit_service.py`:
   https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/qiskit_service.py

6. GrowUP — Qiskit — `demonstracao_qiskit.py`:
   https://github.com/Guilherme-Ximenes/GrowUP---Qiskit/blob/main/demonstracao_qiskit.py

---

**Projeto:** GrowUp — Módulo Qiskit  
**Documento:** DOC03  
**Tema:** Transpilação e Otimização de Circuitos Quânticos
