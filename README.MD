# MESsias — Sistema MES (Manufacturing Execution System)

API REST de um sistema MES desenvolvido como MVP para gerenciamento de produção industrial, com cadastro de veículos, controle de ordens de produção e geração de chassis, integrando dados externos via **Mockaroo**.

---

## 📋 Sobre o Projeto

O MESsias é um sistema para controle e execução de manufatura automotiva que permite:

- Cadastrar e gerenciar veículos (cadastro mestre), sincronizando com o Mockaroo como fonte externa
- Criar e acompanhar ordens de produção vinculadas a veículos
- Gerar e persistir chassis vinculados às ordens de produção
- Auto-cadastrar veículos no banco local caso existam no Mockaroo mas ainda não estejam na base local

---

## 🏗️ Arquitetura

```
┌─────────────────────┐        REST          ┌──────────────────────┐
│   Front-End (HTML)  │ ◄──────────────────► │  API Flask (Back-End)│
│   Porta 80          │                      │  Porta 5000          │
└────────┬────────────┘                      └──────────┬───────────┘
         │                                             │
         │  GET/POST/DELETE                            │  SQLite
         ▼                                             ▼
┌─────────────────────┐                      ┌──────────────────────┐
│  Mockaroo API       │                      │  banco db.sqlite3    │
│  (API Externa)      │                      │  produto             │
│  Listagem, criação  │                      │  ordem_producao      │
│  e chassis de OPs   │                      │  chassi              │
└─────────────────────┘                      └──────────────────────┘
```

Este projeto segue o **Cenário 1** do MVP: Interface (Front-End) consome uma API externa (Mockaroo) para listagem/criação de produtos, e uma API Back-End própria (Flask + SQLite) para persistência e regras de negócio.

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Flask** | Framework web |
| **flask-openapi3** | Documentação automática Swagger / ReDoc / RapiDoc |
| **SQLAlchemy** | ORM para banco de dados |
| **SQLite** | Banco de dados local |
| **Pydantic** | Validação de schemas |
| **Flask-CORS** | Controle de acesso cross-origin |
| **requests** | Chamadas HTTP ao Mockaroo no lado do servidor |
| **Docker** | Containerização dos serviços |

---

## 📁 Estrutura do Projeto

```
.
├── app.py                      # Rotas da API (GET, POST, PUT, DELETE)
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Build do container da API
├── docker-compose.yml          # Orquestração dos serviços (API + Front)
├── model/
│   ├── __init__.py             # Configuração do banco e engine SQLAlchemy
│   ├── base.py                 # Base declarativa
│   ├── produto.py              # Model Produto
│   ├── ordem_producao.py       # Model OrdemDeProducao
│   └── chassi.py               # Model Chassi
├── schemas/
│   ├── __init__.py             # Exportação centralizada dos schemas
│   ├── produto.py              # Schemas de Produto
│   ├── ordem_producao.py       # Schemas de OrdemDeProducao
│   ├── chassi.py               # Schemas de Chassi
│   └── error.py                # Schema de erro
├── logger.py                   # Configuração de logs
└── database/
    └── db.sqlite3              # Banco de dados (gerado automaticamente)
```

---

## 🗄️ Modelo de Dados

### Produto
| Campo | Tipo | Descrição |
|---|---|---|
| `pk_produto` | Integer (PK) | ID externo vindo do Mockaroo |
| `veiculo` | String | Nome da montadora |
| `modelo` | String | Modelo do veículo |
| `facelift` | String | Código de geração/facelift |
| `data_insercao` | DateTime | Data de cadastro |

### OrdemDeProducao
| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer (PK) | Identificador da OP |
| `produto_id` | Integer (FK) | Referência ao Produto |
| `quantidade_prevista` | Float | Quantidade a produzir |
| `status` | String | PENDENTE / EM_PRODUCAO / CONCLUIDA |
| `data_criacao` | DateTime | Data de criação |

### Chassi
| Campo | Tipo | Descrição |
|---|---|---|
| `numero_ordem` | Integer (PK) | Número sequencial único do chassi |
| `ordem_id` | Integer (FK) | Referência à OrdemDeProducao |
| `codigo_chassi` | String | Código do chassi gerado pelo Mockaroo |

---

## 🔌 Endpoints da API

### Produtos

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/produtos` | Lista todos os produtos cadastrados no banco local |
| `POST` | `/produto` | Cadastra um novo produto |
| `DELETE` | `/produto?id={id}` | Remove um produto pelo ID |

### Ordens de Produção

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/ordens_producao` | Lista todas as OPs com nome do veículo |
| `POST` | `/ordem_producao` | Cria uma OP; auto-cadastra o produto se não existir localmente |

### Chassis

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/chassis` | Lista todos os chassis salvos |
| `PUT` | `/chassi` | Insere ou atualiza um chassi (upsert por `numero_ordem`) |

---

## 🌐 API Externa — Mockaroo

O sistema integra com a **Mockaroo API** para:

- **Listar veículos** disponíveis para seleção nas OPs
- **Criar veículos** sincronizando com o dataset remoto
- **Deletar veículos** do dataset externo
- **Gerar chassis** com base na quantidade prevista de cada OP

| Informação | Detalhe |
|---|---|
| Serviço | [Mockaroo](https://mockaroo.com) |
| Licença | Gratuita (plano free, até 200 linhas/requisição) |
| Cadastro | Necessário para obter API Key |
| Rotas utilizadas | `GET /api/{schema_id}`, `POST /api/datasets/{dataset}`, `DELETE /deletecar`, `PUT /GenerateChassis` |

> Os dados são consumidos e tratados dentro da aplicação — nenhuma requisição redireciona o usuário para o Mockaroo.

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado e rodando

### Executando com Docker Compose

1. Clone os repositórios do front e do back na mesma pasta raiz:

```bash
git clone <url-repositorio-back> back_v2
git clone <url-repositorio-front> front
```

2. Na raiz (onde está o `docker-compose.yml`), execute:

```bash
docker compose up --build
```

3. Acesse:
   - **Front-end:** `http://localhost`
   - **API (Swagger):** `http://localhost:5000/openapi`

### Executando localmente (sem Docker)

1. Crie e ative o ambiente virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie a API:

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

---

## 📚 Documentação Interativa

Com a aplicação rodando, acesse:

- **Swagger UI:** `http://localhost:5000/openapi`
- **ReDoc:** `http://localhost:5000/openapi/redoc`
- **RapiDoc:** `http://localhost:5000/openapi/rapidoc`

---

## 🔒 Regras de Negócio

- Ao criar uma OP, se o veículo selecionado não existir no banco local, ele é **cadastrado automaticamente** com os dados enviados pelo front (Montadora, Modelo, FaceliftID)
- Chassis são persistidos via **upsert** — rodar o gerador múltiplas vezes não duplica registros
- O DELETE de produto remove o registro do banco local **e** do dataset Mockaroo de forma sincronizada
- Todas as ordens são criadas com status `PENDENTE` por padrão

---

## 📝 Logs

Todas as operações relevantes são registradas via módulo `logger`, facilitando debug e rastreabilidade das requisições.

---

**Desenvolvido como MVP — Pós-Graduação em Desenvolvimento Full Stack**