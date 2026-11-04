# GrowUp — Módulo Qiskit

**Análise, otimização e validação de circuitos quânticos com Python e Qiskit.**

Este repositório é dedicado **exclusivamente ao desenvolvimento e aos testes do módulo Qiskit**, contribuição do Integrante 5 para o projeto acadêmico **GrowUp — Agente RAG para Otimização de Código em Next-Gen Computing**. O agente, o RAG, o ChromaDB e a API são desenvolvidos no repositório principal da equipe.

> **Estado atual:** prova de conceito de análise e transpilação com Qiskit. Este repositório **não implementa o sistema GrowUp completo**.

## Escopo deste repositório

**Inclui:** criação e leitura de circuitos, análise de métricas, transpilação e otimização, validação de equivalência, experimentos com recursos do Qiskit e testes locais. Também pode definir funções e formatos de entrada/saída para facilitar o consumo do módulo pelo projeto principal.

**Não inclui:** implementação da LLM, pipeline RAG, banco vetorial ChromaDB, servidor FastAPI, endpoints da API principal ou frontend. A integração dos componentes e os testes de ponta a ponta pertencem ao repositório da equipe, em colaboração com os responsáveis por cada área.

## Objetivo

Oferecer ferramentas para:
- Analisar propriedades de circuitos quânticos;
- Comparar circuitos antes e depois da transpilação;
- Medir quantidade de operações e profundidade;
- Verificar equivalência de circuitos unitários pequenos;
- Disponibilizar funções e saídas estruturadas para serem consumidas pelo projeto principal, sem implementar a API neste repositório.

## Tecnologias

- **Python** — linguagem do protótipo (ambiente de desenvolvimento informado: Python 3.14.7).
- **Qiskit 2.6.0** — SDK para construção, análise e transpilação de circuitos quânticos.
- **JSON** — representação de métricas para futura troca de informações com a API.

O protótipo **não exige Qiskit Aer**: ele não realiza simulações de medidas.

## Estrutura do repositório

```text
GrowUP---Qiskit/
├── .gitignore
├── README.md
├── requirements.txt
└── prototipo_qiskit_growup.py
```

## Como executar

Com Python instalado, clone o projeto:

```bash
git clone https://github.com/Guilherme-Ximenes/GrowUP---Qiskit.git
cd GrowUP---Qiskit
```

Crie e ative um ambiente virtual. No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências e execute o protótipo:

```bash
python -m pip install -r requirements.txt
python prototipo_qiskit_growup.py
```

> A instalação pressupõe uma versão do Python compatível com o Qiskit 2.6.0 e com os pacotes distribuídos para o seu sistema. A execução deve ser validada no ambiente local.

## O que o protótipo faz?

O arquivo `prototipo_qiskit_growup.py`:

1. Cria um circuito com **2 qubits**, usando portas X, H e CNOT (CX).
2. Insere operações redundantes, como X seguida de X.
3. Executa `transpile(circuito, optimization_level=3, seed_transpiler=42)`.
4. Exibe o circuito original e o circuito transpilado.
5. Compara a **quantidade de operações** (`size()`) e a **profundidade** (`depth()`).
6. Lista os tipos de operações com `count_ops()`.
7. Verifica a equivalência matemática usando `Operator(...).equiv(...)`.
8. Calcula a redução percentual de operações e exibe um resumo em **JSON**.

### Exemplo didático

O circuito original tem **8 operações**: 2 portas X, 3 portas H e 3 portas CX. Por propriedades dessas portas, é possível representá-lo por apenas **H e CX**, preservando a transformação.

Essa é a simplificação **esperada**. O resultado efetivo do `transpile()` deve ser verificado ao executar o programa; transformações e representação podem variar conforme o ambiente e as opções de transpilação.

Exemplo ilustrativo do resumo JSON, caso a transpilação reduza o circuito a duas operações:

```json
{
  "qubits": 2,
  "portas_antes": 8,
  "portas_depois": 2,
  "profundidade_antes": 8,
  "profundidade_depois": 2,
  "reducao_percentual": 75.0,
  "equivalente": true
}
```

## Limitações atuais

- O circuito é fixo e definido no código; o módulo ainda não oferece uma função reutilizável para receber circuitos externos.
- A otimização é realizada pelo transpilador do Qiskit, **não por uma IA**.
- `Operator.equiv()` verifica equivalência entre operações unitárias (até fase global) e não serve, sem adaptações, para qualquer circuito com medidas, ruído ou fluxo de controle.
- Não há escolha de hardware quântico, topologia física ou modelo de ruído.
- Menos operações ou menor profundidade **não garantem**, isoladamente, menor erro ou maior velocidade em hardware real.
- A integração com os demais componentes do GrowUp será realizada no repositório principal da equipe.

## Próximos passos — Sprint 3

- [ ] Refatorar o protótipo em funções reutilizáveis.
- [ ] Aceitar circuitos de entrada em um formato estruturado e validado.
- [ ] Comparar diferentes níveis de otimização e métricas adicionais.
- [ ] Validar propostas de otimização produzidas pela IA com Qiskit.
- [ ] Definir e documentar funções e formatos de entrada/saída para a equipe integrar o módulo.
- [ ] Entregar o módulo Qiskit e exemplos de uso aos responsáveis pela integração no repositório principal.
- [ ] Adicionar testes automatizados e documentar limitações.

## Relação com o agente GrowUp

No projeto principal, o agente RAG utilizará conhecimento de computação quântica e documentação do Qiskit para **analisar e propor** melhorias em circuitos. **Este repositório fornece apenas o componente Qiskit**, responsável por métricas, transpilação de referência e verificação técnica. A conexão com o agente será realizada pela equipe fora deste repositório.

A mentoria orientou a explorar tanto as ferramentas de otimização nativas do Qiskit quanto propostas formuladas pela própria IA. A validação é fundamental: uma sugestão não deve ser tratada como correta apenas porque reduziu o número de portas.

## Referências

- [Documentação oficial do Qiskit](https://docs.quantum.ibm.com/)
- [Repositório oficial Qiskit (GitHub)](https://github.com/Qiskit/qiskit)

---

**Projeto GrowUp · Módulo Qiskit · Integrante 5**
