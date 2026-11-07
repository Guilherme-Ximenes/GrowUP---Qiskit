# GrowUp — Módulo Qiskit

**Análise, otimização e validação de circuitos quânticos com Python e Qiskit.**

Este repositório reúne funções Python com Qiskit para analisar métricas, transpilar e otimizar circuitos quânticos, adaptar operações a restrições de hardware e verificar equivalência. O módulo faz parte do projeto acadêmico **GrowUp — Agente RAG para Otimização de Código em Next-Gen Computing**.

O objetivo é oferecer funções reutilizáveis para analisar circuitos, realizar transpilação, estudar restrições de hardware e avaliar propostas de otimização. A integração com o agente de IA e os demais serviços será feita no projeto principal da equipe.

> **Estado atual:** módulo funcional de prova de conceito, com dez funções principais, uma função auxiliar de validação, uma demonstração executável e 20 testes automatizados. **Este repositório não é o sistema GrowUp completo.**

## Escopo e funcionalidades

O arquivo principal, `qiskit_service.py`, disponibiliza estas dez funções de uso principal:

| Função | Responsabilidade |
| --- | --- |
| `obter_metricas(circuito)` | Retorna número de qubits, total de operações, profundidade e contagem por tipo de operação. |
| `otimizar_circuito(circuito, nivel_otimizacao=3)` | Utiliza o transpilador do Qiskit para otimização genérica, sem definir um hardware específico. |
| `comparar_niveis(circuito)` | Compara métricas e equivalência nos níveis 0, 1, 2 e 3, registrando também o status e o motivo quando a equivalência não puder ser verificada. |
| `verificar_equivalencia(original, otimizado, limite_qubits=10)` | Compara operadores unitários até fase global, considerando os metadados de layout e respeitando o teto de 10 qubits para essa verificação. |
| `otimizar_para_hardware(circuito, conectividade, layout_inicial=None, nivel_otimizacao=0, portas_nativas=None)` | Adapta o circuito a um mapa de conexões e, opcionalmente, a um conjunto de portas nativas. |
| `analisar_adaptacao_hardware(original, adaptado, portas_nativas=None)` | Compara métricas, equivalência e nomes das portas utilizadas pelo circuito adaptado. |
| `avaliar_proposta_ia(original, proposta)` | Avalia uma proposta de circuito comparando métricas e verificando equivalência. |
| `carregar_circuito_qasm(texto_qasm)` | Importa texto OpenQASM 2 para `QuantumCircuit`, verificando tipo, tamanho do texto, registradores e quantidade de operações. |
| `exportar_circuito_qasm(circuito)` | Converte um circuito compatível para texto OpenQASM 2. |
| `processar_circuito_qasm(texto_qasm, nivel_otimizacao=3)` | Importa, otimiza, analisa e devolve as métricas, o status de equivalência e o circuito otimizado em OpenQASM 2. |

A função auxiliar `validar_circuito()` centraliza a verificação de tipos para argumentos que devem ser objetos `QuantumCircuit`.

**Importante:** a função `avaliar_proposta_ia()` **não executa uma IA**. Ela recebe uma proposta de circuito já construída e aplica verificações técnicas. A geração das propostas pelo agente RAG ainda depende da integração com os outros componentes do GrowUp.

### Como interpretar as análises

As funções de análise retornam dicionários Python com campos como `diferenca_operacoes`, `diferenca_profundidade` e `status_verificacao`.

O campo `status_verificacao` pode ser:

- `"equivalente"` — o método confirmou equivalência unitária;
- `"nao_equivalente"` — o método identificou transformações diferentes;
- `"nao_verificado"` — a equivalência não pôde ser determinada pelo método utilizado.

Quando a verificação de equivalência não é suportada e gera o `ValueError` previsto pelo módulo, `equivalente` recebe `None` e `motivo` apresenta uma explicação. Isso **não** é a mesma coisa que retornar `False`. Os campos de redução válida de `avaliar_proposta_ia()` também recebem `None` quando não é possível verificar a equivalência.

Em `comparar_niveis(circuito)`, o retorno é um dicionário cujas chaves são os níveis `0`, `1`, `2` e `3`. Cada nível contém `metricas`, `equivalente`, `status_verificacao` e `motivo`. A função mantém os campos originais `metricas` e `equivalente`, para não quebrar os exemplos já existentes.

Diferenças de métricas são calculadas como **valor do circuito adaptado/proposto menos valor do original**. Assim, um número negativo indica redução; não garante, por si só, melhor desempenho em um dispositivo real.

### Validações e limite da equivalência

As funções que recebem circuitos verificam, diretamente ou por meio de outras funções do módulo, se os argumentos são objetos `QuantumCircuit`. `otimizar_para_hardware()` também exige que `conectividade` seja um `CouplingMap`. Um tipo de entrada inválido gera `TypeError`; níveis de otimização fora dos valores aceitos (`0`, `1`, `2` ou `3`) geram `ValueError`.

A função `verificar_equivalencia()` usa o parâmetro `limite_qubits`, cujo valor padrão é **10**. No código atual, `LIM_MAX_EQUIV = 10` também define um **teto máximo**: a chamada pode solicitar um limite inteiro positivo menor, mas não pode solicitar um limite maior do que 10.

```python
from qiskit import QuantumCircuit
from qiskit_service import verificar_equivalencia

circuito = QuantumCircuit(2)

# Dentro do limite: a equivalência pode ser verificada.
print(verificar_equivalencia(circuito, circuito, limite_qubits=2))

# Limite acima do teto: gera ValueError antes de construir operadores.
# verificar_equivalencia(circuito, circuito, limite_qubits=30)
```

Quando os circuitos têm a mesma quantidade de qubits, mas ultrapassam o limite aplicável, a verificação lança `ValueError` **antes** de criar os operadores. Nas funções `comparar_niveis()`, `analisar_adaptacao_hardware()` e `avaliar_proposta_ia()`, esse erro é registrado como `"nao_verificado"`, sem afirmar que os circuitos são diferentes. Se as quantidades de qubits dos dois circuitos forem diferentes, `verificar_equivalencia()` retorna `False` antes de construir as matrizes.

**Escopo do limite:** os 10 qubits restringem somente a verificação por operadores densos (`Operator.from_circuit()`), não as funções de métricas ou transpilação. O módulo ainda precisa de controles adicionais de quantidade de operações, tempo e recursos para ser exposto a uma API.

## Estrutura do repositório

```text
GrowUP---Qiskit/
├── .gitignore
├── README.md
├── requirements.txt
├── qiskit_service.py         # Funções reutilizáveis do módulo
├── demonstracao_qiskit.py    # Demonstração das funcionalidades
└── teste_qiskit_service.py   # Testes automatizados com unittest
```

O antigo `prototipo_qiskit_growup.py` foi substituído por `demonstracao_qiskit.py`. Seu conteúdo anterior continua disponível no histórico de commits do GitHub.

## Requisitos e instalação

- Python em versão compatível com as dependências instaladas.
- **Qiskit 2.6.0**, fixado em `requirements.txt`.
- Não é necessário instalar o **Qiskit Aer** para os exemplos atuais, pois eles não fazem simulação por amostragem ou de ruído.

Clone o repositório:

```bash
git clone https://github.com/Guilherme-Ximenes/GrowUP---Qiskit.git
cd GrowUP---Qiskit
```

Crie um ambiente virtual e instale as dependências.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> O ambiente utilizado durante o desenvolvimento foi informado como Python 3.14.7 e Qiskit 2.6.0. A instalação deve ser validada no sistema e na versão de Python de cada integrante.

## Executar a demonstração

```bash
python demonstracao_qiskit.py
```

A demonstração tem três partes:

1. **Otimização genérica:** cria um circuito com portas redundantes, aplica `otimizar_circuito()`, apresenta métricas e compara os níveis de otimização 0 a 3.
2. **Adaptação ao hardware:** usa um `CouplingMap` linear de três qubits e o conjunto hipotético de portas `["rz", "sx", "x", "cx"]` para demonstrar layout, roteamento e tradução para portas permitidas.
3. **Avaliação de propostas:** simula uma proposta equivalente gerada pelo transpilador e uma proposta não equivalente, utilizando `avaliar_proposta_ia()`.

Os resultados são exibidos no terminal, inclusive em formato JSON para facilitar a leitura. **A demonstração não se conecta a uma LLM, API ou processador quântico real.**

## Exemplo de uso do módulo

As funções podem ser importadas em outros arquivos Python:

```python
from qiskit import QuantumCircuit
from qiskit_service import (
    obter_metricas,
    otimizar_circuito,
    verificar_equivalencia,
    avaliar_proposta_ia,
)

# Circuito com redundância
original = QuantumCircuit(2)
original.x(0)
original.x(0)
original.h(0)
original.cx(0, 1)

# Transpilação genérica
otimizado = otimizar_circuito(original, nivel_otimizacao=3)

print("Métricas originais:", obter_metricas(original))
print("Métricas otimizadas:", obter_metricas(otimizado))
print("Equivalentes:", verificar_equivalencia(original, otimizado))

# Avaliação estruturada, como se fosse uma proposta recebida
resultado = avaliar_proposta_ia(original, otimizado)
print("Status:", resultado["status_verificacao"])
print("Diferença de operações:", resultado["diferenca_operacoes"])
```

Para adaptar circuitos a uma topologia e a portas permitidas:

```python
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit_service import (
    otimizar_para_hardware,
    analisar_adaptacao_hardware,
)

circuito = QuantumCircuit(3)
circuito.h(0)
circuito.cx(0, 2)
circuito.cx(0, 1)

conectividade = CouplingMap.from_line(3)
portas_nativas = ["rz", "sx", "x", "cx"]

adaptado = otimizar_para_hardware(
    circuito,
    conectividade,
    portas_nativas=portas_nativas,
)

analise = analisar_adaptacao_hardware(
    circuito,
    adaptado,
    portas_nativas=portas_nativas,
)

print(analise)
```

O mapa linear e a lista de portas são **exemplos didáticos**, não a caracterização completa de um dispositivo quântico real.

## Integração inicial por OpenQASM 2

O módulo agora dispõe de um adaptador Python: **texto OpenQASM 2 → QuantumCircuit → otimização/análise → texto OpenQASM 2**. Ele não publica endpoints HTTP. A função de entrada principal para esse fluxo é **processar_circuito_qasm()**.

### Exemplo em Python

~~~python
import json
from qiskit import QuantumCircuit, qasm2
from qiskit_service import processar_circuito_qasm

circuito = QuantumCircuit(2)
circuito.x(0)
circuito.x(0)
circuito.h(0)
circuito.cx(0, 1)

texto = qasm2.dumps(circuito)
resultado = processar_circuito_qasm(texto, nivel_otimizacao=3)

print(resultado["status_verificacao"])
print(resultado["circuito_otimizado_qasm"])
print(json.dumps(resultado, ensure_ascii=False, indent=2))
~~~

O retorno é um dicionário com **original**, **proposta** (métricas), **equivalente**, **status_verificacao**, **motivo**, **diferenca_operacoes**, **diferenca_profundidade**, **reduziu_operacoes**, **reduziu_profundidade** e **circuito_otimizado_qasm**. O exemplo demonstra a serialização JSON. O teste integrado `test_processar_circuito_qasm()` também executa `json.dumps(resultado, ensure_ascii=False)` para verificar a serialização.

### Formato JSON proposto para alinhamento com Vlad

Este é um **exemplo de contrato sugerido**, não um endpoint existente ou um formato definitivamente acordado:

~~~json
{
  "circuito_qasm": "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\nh q[0];\ncx q[0],q[1];",
  "nivel_otimizacao": 3
}
~~~

No projeto principal, o serviço FastAPI poderá ler esses campos, chamar a função Python e serializar o dicionário retornado. A rota HTTP, os códigos de resposta, o esquema definitivo e a conexão com o agente RAG ainda precisam ser definidos pela equipe.

### Validações e limites implementados

A função `carregar_circuito_qasm()` aplica os seguintes limites iniciais:

| Recurso | Constante no código | Limite |
| --- | --- | --- |
| Comprimento do texto OpenQASM 2 | `MAX_CARACTERES_QASM` | 10.000 caracteres |
| Qubits do circuito importado | `MAX_QUBITS_QASM` | 32 qubits |
| Bits clássicos do circuito importado | `MAX_BITS_CLASSICOS_QASM` | 32 bits |
| Operações do circuito importado | `MAX_OPERACOES_QASM` | 500 operações |
| Verificação de equivalência unitária | `LIM_MAX_EQUIV` | 10 qubits |

- **Antes da conversão:** a entrada deve ser uma string não vazia dentro do limite de caracteres. Uma pré-verificação com expressões regulares identifica declarações convencionais `qreg` e `creg`, ignorando comentários, para rejeitar registradores que ultrapassem os limites de qubits e bits clássicos.
- **Durante a conversão:** `qasm2.loads(texto_qasm, include_path=())` interpreta OpenQASM 2 sem buscar arquivos de inclusão em diretórios externos. Erros `QASM2Error` são convertidos em `ValueError`.
- **Depois da conversão:** o circuito reconstruído é conferido por `num_qubits`, `num_clbits` e `size()`. O limite de **500 operações é conferido somente após o parsing**, não antes.
- **Exportação:** `qasm2.dumps()` converte circuitos compatíveis; nem todo recurso do Qiskit é representável em OpenQASM 2. O circuito otimizado exportado não recebe nessa função uma nova conferência desses limites de entrada.
- **Equivalência:** a análise por operadores unitários permanece limitada a 10 qubits. Circuitos com mais qubits podem ser otimizados, mas sua equivalência pode ser classificada como `"nao_verificado"`.
- **Erros:** tipo inadequado gera `TypeError`; textos vazios, inválidos ou que excedem os limites geram `ValueError`. A interpretação dos erros como respostas HTTP será responsabilidade do serviço de integração.

**Limitação de segurança:** a pré-verificação com expressões regulares não substitui um parser seguro ou um isolamento de execução. Um texto malicioso ou uma definição de operações complexas ainda pode consumir recursos durante o parsing ou a transpilação. Não há limites de tempo, memória ou isolamento de processo. Não exponha esse adaptador diretamente a entradas públicas não confiáveis sem essas proteções.

## Testes automatizados

O arquivo `teste_qiskit_service.py` contém **20 métodos de teste automatizado** com a biblioteca padrão `unittest` do Python.

Execute:

```bash
python -m unittest -v teste_qiskit_service
```

Ou execute o arquivo diretamente:

```bash
python teste_qiskit_service.py
```

Os testes atualmente cobrem:

- Métricas básicas, otimização genérica e comparação dos níveis `0` a `3`;
- Rejeição de níveis de otimização inválidos, tanto na otimização genérica quanto na adaptação ao hardware;
- Equivalência e não equivalência, inclusive após aplicação de um layout físico diferente;
- Adaptação ao hardware e verificação de nomes de portas permitidas e não permitidas;
- Análise de hardware equivalente e com equivalência inconclusiva;
- Avaliação de proposta correta e incorreta, sem considerar uma redução de operações como válida quando a proposta não é equivalente;
- Tratamento de propostas com medição e de `comparar_niveis()` quando a equivalência unitária não pode ser verificada;
- Rejeição de entradas que não sejam `QuantumCircuit` nas funções principais e rejeição de conectividade que não seja `CouplingMap`;
- Limite padrão de 10 qubits, limite personalizado menor e rejeição de limites inválidos ou superiores ao teto, incluindo `0`, `-1`, `True`, `"10"`, `11` e `30`;
- Carregamento de OpenQASM 2 válido e rejeição de tipo inválido, texto inválido e texto acima do limite de caracteres;
- Processamento integrado OpenQASM 2, exportação do circuito otimizado, verificação de equivalência e serialização do resultado com `json.dumps()` em exemplo simples;
- Rejeição de uma declaração de 33 qubits e de um circuito com 501 operações na importação OpenQASM 2.

A suíte possui **20 métodos de teste**. Para confirmar o resultado no ambiente de execução, rode o comando acima. **Ainda não existe integração contínua (CI)** configurada no repositório para executá-los automaticamente a cada push. A cobertura atual não garante ausência de erros em todos os casos.

## Limitações conhecidas

- **Equivalência unitária:** `verificar_equivalencia()` utiliza `Operator.from_circuit()` e `Operator.equiv()`. É adequada aos circuitos unitários pequenos estudados; não é uma verificação geral de circuitos com medições, `reset`, ruído ou fluxo clássico.
- **Custo computacional:** a construção de operadores completos cresce exponencialmente com o número de qubits. A verificação unitária possui teto de 10 qubits; o carregamento OpenQASM tem limites de 32 qubits, 32 bits clássicos e 500 operações. Entretanto, os limites de operações são conferidos após o parsing, e **não há limitação de tempo/memória nem isolamento de processos**. Isso não equivale à proteção de um serviço público.
- **Tratamento de verificações não suportadas:** `verificar_equivalencia()` gera `ValueError` quando ocorre um `QiskitError` na construção do operador. `avaliar_proposta_ia()`, `analisar_adaptacao_hardware()` e, agora, `comparar_niveis()` registram esse `ValueError` como `"nao_verificado"`, preenchendo `motivo`. Erros de transpilação ou outros tipos de exceção não são cobertos automaticamente por esse tratamento.
- **Diferença de qubits:** o verificador atual retorna `False` quando os circuitos têm quantidades diferentes de qubits.
- **Hardware:** `otimizar_para_hardware()` considera conectividade e, opcionalmente, portas permitidas. Ainda não representa integralmente um processador físico com tempos, fidelidades, calibrações e ruído.
- **Compatibilidade de portas:** `somente_portas_permitidas` confere os **nomes das operações**; não valida sozinha todas as restrições de conectividade, direção, calibração ou execução física.
- **Métricas:** menor contagem de operações ou profundidade não assegura menor erro ou melhor execução em hardware real.
- **Propostas externas:** o módulo já importa e exporta OpenQASM 2 por funções Python, com validações iniciais e limites no carregamento. O contrato JSON/HTTP ainda não é definitivo, os limites não cobrem todas as fases do processamento e não há isolamento de recursos. Código Python produzido por uma IA não deve ser executado diretamente sem controle.

## Integração com o projeto principal

No GrowUp completo, o agente RAG poderá consultar sua base de conhecimento e **propor** melhorias em circuitos. O módulo Qiskit será responsável por análises e verificações técnicas dessas propostas, quando aplicáveis.

Este repositório **não inclui** LLM, RAG, ChromaDB, endpoints FastAPI ou frontend. O trabalho aqui é disponibilizar as funções Qiskit e um adaptador Python para OpenQASM 2. O contrato JSON/HTTP definitivo ainda precisa ser alinhado com o responsável pela API. A conexão efetiva com endpoints e com o agente acontece no projeto principal.

## Referências

- [Documentação oficial do Qiskit](https://quantum.cloud.ibm.com/docs)
- [Código-fonte oficial do Qiskit](https://github.com/Qiskit/qiskit)
- [Biblioteca unittest do Python](https://docs.python.org/3/library/unittest.html)

---

**Projeto GrowUp · Módulo Qiskit**
