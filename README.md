# AI Technical Knowledge Assistant

Assistente de IA para consulta de documentação técnica, utilizando **Langflow, MCP, Gemini e Notion**.

O projeto explora uma arquitetura para facilitar o acesso ao conhecimento técnico de times de tecnologia por meio de consultas em linguagem natural.

> **Status:** MVP — V1 concluída

![Demonstração do projeto](assets/demo.gif)

---

## 1. Sobre o projeto

Em times de tecnologia, informações importantes podem estar distribuídas entre documentações, regras de negócio, registros técnicos e diferentes ferramentas.

O problema nem sempre é a ausência da informação, mas o tempo necessário para **encontrar, interpretar e conectar a informação correta**.

Este projeto implementa um **Assistente de IA para consulta de conhecimento técnico**, utilizando um agente no Langflow conectado ao Notion através do **Model Context Protocol (MCP)**.

A proposta é explorar uma arquitetura em que o conhecimento técnico possa ser consultado por linguagem natural, reduzindo a necessidade de localizar manualmente páginas e informações distribuídas na documentação.

---

## 2. Problema

Em um ambiente de desenvolvimento, uma mesma resposta pode depender de informações presentes em diferentes documentos:

* regras de negócio;
* documentação de projetos;
* procedimentos técnicos;
* informações de APIs;
* estruturas e conceitos relacionados ao sistema;
* histórico e contexto de decisões técnicas.

Quando a documentação cresce, localizar rapidamente a informação relevante pode consumir tempo do time e interromper o fluxo de desenvolvimento.

Além disso, o conhecimento pode ficar concentrado em pessoas que já conhecem determinado sistema ou projeto.

O projeto busca explorar uma alternativa: permitir que o desenvolvedor consulte a documentação utilizando **linguagem natural**, enquanto o agente acessa a fonte de conhecimento necessária.

---

## 3. Visão do produto

O V1 implementa apenas uma parte dessa visão: **consulta de documentação técnica armazenada no Notion**.

A arquitetura foi pensada como uma base que pode futuramente conectar outras fontes de conhecimento e informações operacionais.

### Acesso ao conhecimento

O assistente pode atuar como uma interface de consulta para:

* localizar informações técnicas;
* encontrar páginas relevantes;
* recuperar o conteúdo da documentação;
* responder perguntas utilizando o conteúdo disponível na fonte.

### Eficiência operacional

Uma evolução possível é utilizar a mesma arquitetura para facilitar atividades como:

* onboarding de novos integrantes;
* preparação para reuniões;
* consulta rápida de procedimentos;
* recuperação de contexto técnico.

### Apoio à tomada de decisão

Com a integração de outras fontes, como ferramentas de gestão e bases operacionais, a arquitetura poderia futuramente apoiar consultas relacionadas a:

* incidentes;
* bugs recorrentes;
* histórico de tarefas;
* gargalos técnicos;
* informações necessárias para priorização.

Esses cenários fazem parte da **visão de evolução do projeto** e não estão implementados no V1.

---

## 4. Objetivo do MVP

O objetivo do V1 é validar uma arquitetura simples para consulta de conhecimento técnico utilizando um agente de IA.

O MVP permite:

1. receber uma pergunta em linguagem natural;
2. encaminhar a solicitação ao agente no Langflow;
3. utilizar ferramentas MCP para consultar o Notion;
4. localizar uma página relevante;
5. recuperar o conteúdo da página;
6. utilizar esse contexto para gerar a resposta.

O foco do MVP foi manter a arquitetura pequena e funcional, evitando adicionar componentes que não fossem necessários para validar a ideia.

---

## 5. Arquitetura

### Visão do V1

```text
┌──────────────┐
│  OpenWebUI   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Langflow   │
│              │
│    Agent     │
│      +       │
│    Gemini    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  MCP Notion  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Notion    │
│ Documentação │
└──────────────┘
```

### Visão de evolução

A arquitetura pode ser expandida posteriormente para conectar outras fontes de conhecimento:

```text
                   ┌──────────────┐
                   │    Notion    │
                   └──────┬───────┘
                          │
                   ┌──────▼───────┐
                   │              │
                   │     MCP      │
                   │              │
                   └──────┬───────┘
                          │
┌──────────────┐    ┌─────▼─────┐
│   OpenWebUI  │───►│ Langflow  │
└──────────────┘    │   Agent   │
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │   Gemini  │
                    └───────────┘
```

Integrações futuras podem adicionar outras fontes, como ferramentas de gestão, incidentes ou bases operacionais, sem fazer parte do escopo atual.

![Arquitetura do projeto](assets/image_flow.png)

---

## 6. Tecnologias

| Tecnologia                  | Utilização                                                         |
| --------------------------- | ------------------------------------------------------------------ |
| **Python**                  | Pipeline de integração com o OpenWebUI                             |
| **Langflow**                | Orquestração do agente e do fluxo                                  |
| **Gemini 2.5 Flash**        | Modelo utilizado pelo agente                                       |
| **MCP**                     | Comunicação padronizada entre o agente e o servidor de ferramentas |
| **Notion**                  | Fonte de documentação técnica                                      |
| **OpenWebUI**               | Interface para interação com o assistente                          |
| **Docker / Docker Compose** | Execução e integração dos serviços                                 |
| **PostgreSQL**              | Persistência do Langflow                                           |
| **Node.js**                 | Runtime utilizado pelo servidor MCP do Notion                      |

---

## 7. Como funciona

A consulta segue o seguinte fluxo:

```text
Usuário
   │
   │ pergunta em linguagem natural
   ▼
OpenWebUI
   │
   ▼
Langflow
   │
   ▼
Agent + Gemini
   │
   │ decide utilizar uma ferramenta
   ▼
MCP Notion
   │
   ├── Busca páginas
   │
   └── Recupera conteúdo
   │
   ▼
Notion
   │
   ▼
Contexto retornado ao Agent
   │
   ▼
Resposta ao usuário
```

No V1, as principais operações utilizadas pelo MCP são:

* `api_post_search` — busca páginas no Notion;
* `api_retrieve_page_markdown` — recupera o conteúdo de uma página.

A resposta é então construída pelo agente utilizando o contexto recuperado da documentação.

---

## 8. Pré-requisitos

Para executar o projeto localmente, é necessário ter:

* Docker;
* Docker Compose;
* uma conta no Notion;
* uma integração configurada no Notion;
* token de acesso do Notion;
* credencial para utilização do Gemini;
* credencial configurada para o Langflow;
* Git, caso o projeto seja clonado do repositório.

---

## 9. Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

Exemplo:

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=langflow

LANGFLOW_API_KEY=sua_chave

NOTION_TOKEN=seu_token_notion
MCP_AUTH_TOKEN=seu_token_mcp

LANGFLOW_URL=http://localhost:7860
```

> **Importante:** não versione o arquivo `.env`. As credenciais devem permanecer fora do repositório.

A credencial utilizada pelo modelo Gemini é configurada no ambiente do Langflow, conforme a configuração do fluxo.

---

## 10. Como executar

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd ai-technical-docs-assistant
```

Crie o arquivo `.env` com as variáveis necessárias.

Em seguida, inicie os serviços:

```bash
docker compose -f docker-compose-dev.yaml up -d
```

Verifique os containers:

```bash
docker compose -f docker-compose-dev.yaml ps
```

### Serviços principais

| Serviço    |  Porta |
| ---------- | -----: |
| OpenWebUI  | `3000` |
| Langflow   | `7860` |
| MCP Notion | `8000` |
| Adminer    | `8080` |
| PostgreSQL | `5433` |

Após iniciar os containers:

* OpenWebUI: `http://localhost:3000`
* Langflow: `http://localhost:7860`
* Adminer: `http://localhost:8080`

---

## 11. Configuração do Notion / MCP

O servidor MCP utiliza o pacote oficial:

```text
@notionhq/notion-mcp-server
```

O container executa o servidor MCP utilizando transporte HTTP:

```text
notion-mcp-server --transport http --host 0.0.0.0 --port 8000
```

O token do Notion é disponibilizado ao container através da variável:

```env
NOTION_TOKEN=seu_token_notion
```

O servidor MCP também utiliza um token de autenticação definido em:

```env
MCP_AUTH_TOKEN=seu_token_mcp
```

### Permissão no Notion

A integração do Notion precisa ter acesso às páginas que serão consultadas pelo agente.

A documentação utilizada pelo MVP deve estar acessível pela integração configurada.

No Langflow, o agente utiliza o servidor MCP como fonte externa de ferramentas para:

```text
Buscar página
     ↓
Recuperar conteúdo
     ↓
Fornecer contexto ao agente
     ↓
Gerar resposta
```

---

## 12. Demonstração

O GIF abaixo apresenta uma execução do MVP:

![Demonstração do projeto](assets/demo.gif)

A demonstração mostra o fluxo de consulta utilizando a documentação técnica como fonte de conhecimento.

---

## 13. Estrutura do projeto

```text
ai-technical-docs-assistant/
├── assets/
│   ├── demo.gif
│   └── image_flow.png
│
├── flows/
│   └── version_01_flow.json
│
├── langflow_data/
│   └── fluxo.json
│
├── openwebui_data/
│   └── pipeline_function.py
│
├── docker-compose-dev.yaml
├── README.md
└── .gitignore
```

### Principais arquivos

**`flows/version_01_flow.json`**

Fluxo versionado do Langflow correspondente ao V1.

**`openwebui_data/pipeline_function.py`**

Pipeline utilizado para integração do OpenWebUI com o Langflow.

**`docker-compose-dev.yaml`**

Configuração dos serviços necessários para executar o ambiente local.

**`assets/`**

Recursos utilizados na documentação do projeto, incluindo demonstração e diagrama da arquitetura.

---

## 14. Limitações / Escopo da V1

O V1 foi desenvolvido como uma prova de conceito funcional e possui um escopo deliberadamente reduzido.

### Implementado

* consulta de documentação técnica;
* integração com Notion;
* comunicação através de MCP;
* agente configurado no Langflow;
* utilização do Gemini 2.5 Flash;
* interface através do OpenWebUI;
* execução dos serviços utilizando Docker Compose.

### Não implementado no V1

* integração com Jira;
* consulta a incidentes ou histórico de bugs;
* integração com múltiplas fontes de dados;
* análise de métricas operacionais;
* consolidação de dados para relatórios executivos;
* priorização automática de backlog;
* arquitetura multiagente;
* memória vetorial ou sistema de RAG adicional.

Esses itens podem fazer parte de futuras versões, dependendo da necessidade e dos objetivos da aplicação.

---

## Próximas evoluções

A arquitetura permite explorar novas fontes de conhecimento e casos de uso sem alterar o objetivo central do projeto.

Entre as possibilidades estão:

* integração com Jira;
* consulta a incidentes e bugs;
* integração com outras bases de conhecimento;
* combinação de documentação técnica com dados operacionais;
* geração de resumos a partir de diferentes fontes;
* apoio à identificação de padrões e gargalos técnicos.

Essas evoluções fazem parte da visão do projeto e não representam funcionalidades disponíveis na V1.

