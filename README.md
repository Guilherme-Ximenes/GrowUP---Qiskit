# GrowUp — Módulo Qiskit

**Análise, otimização e validação de circuitos quânticos com Python e Qiskit.**

Este repositório reúne funções Python com Qiskit para analisar métricas, transpilar e otimizar circuitos quânticos, adaptar operações a restrições de hardware e verificar equivalência. O módulo faz parte do projeto acadêmico **GrowUp — Agente RAG para Otimização de Código em Next-Gen Computing**.

O objetivo é oferecer funções reutilizáveis para analisar circuitos, realizar transpilação, estudar restrições de hardware e avaliar propostas de otimização. A integração com o agente de IA e os demais serviços será feita no projeto principal da equipe.

> **Estado atual:** módulo funcional de prova de conceito, com sete funções reutilizáveis, uma demonstração executável e 14 testes automatizados. **Este repositório não é o sistema GrowUp completo.**

## Escopo e funcionalidades

O arquivo principal, `qiskit_service.py`, disponibiliza:

| Função | Responsabilidade |
| --- | --- |
| `obter_metricas(circuito)` | Retorna número de qubits, total de operações, profundidade e contagem por tipo de operação. |
| `otimizar_circuito(circuito, nivel_otimizacao=3)` | Utiliza o transpilador do Qiskit para otimização genérica, sem definir um hardware específico. |
| `comparar_niveis(circuito)` | Compara métricas e equivalência nos níveis 0, 1, 2 e 3, registrando também o status e o motivo quando a equivalência não puder ser verificada. |
| `verificar_equivalencia(original, otimizado)` | Compara operadores unitários até fase global, considerando metadados de layout quando disponíveis. |
| `otimizar_para_hardware(circuito, conectividade, layout_inicial=None, nivel_otimizacao=0, portas_nativas=None)` | Adapta o circuito a um mapa de conexões e, opcionalmente, a um conjunto de portas nativas. |
| `analisar_adaptacao_hardware(original, adaptado, portas_nativas=None)` | Compara métricas, equivalência e nomes das portas utilizadas pelo circuito adaptado. |
| `avaliar_proposta_ia(original, proposta)` | Avalia uma proposta de circuito comparando métricas e verificando equivalência. |

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

## Testes automatizados

O arquivo `teste_qiskit_service.py` contém **14 testes automatizados** com a biblioteca padrão `unittest` do Python.

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
- Tratamento de uma proposta com medição cuja equivalência unitária não pode ser verificada.

**Os 14 testes foram executados com sucesso no ambiente local de desenvolvimento**, conforme verificação realizada pelo responsável pelo módulo. Ainda não existe configuração de integração contínua (CI) no repositório para executá-los a cada push, e a cobertura não garante ausência de erros em todos os casos.

**Teste ainda pendente:** criar um caso específico para confirmar o novo retorno `"nao_verificado"` de `comparar_niveis()` em situações de equivalência inconclusiva. Os testes atuais confirmam o comportamento padrão da comparação, mas não cobrem diretamente esse novo caminho.

## Limitações conhecidas

- **Equivalência unitária:** `verificar_equivalencia()` utiliza `Operator.from_circuit()` e `Operator.equiv()`. É adequada aos circuitos unitários pequenos estudados; não é uma verificação geral de circuitos com medições, `reset`, ruído ou fluxo clássico.
- **Custo computacional:** a construção de operadores completos cresce exponencialmente com o número de qubits. Não há ainda limite de tamanho implementado para entradas externas.
- **Tratamento de verificações não suportadas:** `verificar_equivalencia()` gera `ValueError` quando ocorre um `QiskitError` na construção do operador. `avaliar_proposta_ia()`, `analisar_adaptacao_hardware()` e, agora, `comparar_niveis()` registram esse `ValueError` como `"nao_verificado"`, preenchendo `motivo`. Erros de transpilação ou outros tipos de exceção não são cobertos automaticamente por esse tratamento.
- **Diferença de qubits:** o verificador atual retorna `False` quando os circuitos têm quantidades diferentes de qubits.
- **Hardware:** `otimizar_para_hardware()` considera conectividade e, opcionalmente, portas permitidas. Ainda não representa integralmente um processador físico com tempos, fidelidades, calibrações e ruído.
- **Compatibilidade de portas:** `somente_portas_permitidas` confere os **nomes das operações**; não valida sozinha todas as restrições de conectividade, direção, calibração ou execução física.
- **Métricas:** menor contagem de operações ou profundidade não assegura menor erro ou melhor execução em hardware real.
- **Propostas externas:** o módulo recebe objetos Python `QuantumCircuit`. Ainda não há um contrato implementado de serialização, validação e limites para circuitos vindos de uma API. Código Python produzido por uma IA não deve ser executado diretamente sem controle.

## Integração com o projeto principal

No GrowUp completo, o agente RAG poderá consultar sua base de conhecimento e **propor** melhorias em circuitos. O módulo Qiskit será responsável por análises e verificações técnicas dessas propostas, quando aplicáveis.

Este repositório **não inclui** LLM, RAG, ChromaDB, endpoints FastAPI ou frontend. O trabalho aqui é disponibilizar e preparar as funções Qiskit para consumo externo; o contrato de entrada e saída ainda precisa ser alinhado com o responsável pela API. A conexão efetiva com endpoints e com o agente acontece no projeto principal.

### Próximos passos

- [x] Criar funções reutilizáveis para métricas, otimização e equivalência.
- [x] Comparar níveis de otimização e explorar conectividade e portas nativas.
- [x] Implementar avaliação estruturada de propostas de circuitos.
- [x] Criar demonstração usando o módulo reutilizável.
- [x] Ampliar a suíte de nove para 14 testes automatizados, incluindo layouts, níveis inválidos, propostas incorretas e portas não permitidas.
- [x] Registrar status e motivo de equivalência inconclusiva em `comparar_niveis()`.
- [ ] Testar especificamente esse novo caminho de `comparar_niveis()` e ampliar a validação de entradas inválidas.
- [ ] Definir com a equipe um formato seguro e validado para receber circuitos externos.
- [ ] Estabelecer limites de recursos e padronizar o tratamento de erros para integração.
- [ ] Validar a integração com API, agente RAG e fluxo ponta a ponta no projeto principal.
- [ ] Opcional: adicionar execução automática dos testes via GitHub Actions.

## Referências

- [Documentação oficial do Qiskit](https://quantum.cloud.ibm.com/docs)
- [Código-fonte oficial do Qiskit](https://github.com/Qiskit/qiskit)
- [Biblioteca unittest do Python](https://docs.python.org/3/library/unittest.html)

---

**Projeto GrowUp · Módulo Qiskit**
