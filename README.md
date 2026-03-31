# MESsias — Front-End

Interface web do sistema MES (Manufacturing Execution System) para gerenciamento de ordens de produção automotiva.

---

## 📋 Sobre

O front-end consome a API back-end local (Flask + SQLite) e o serviço externo **Mockaroo** para listagem, criação e remoção de veículos, além de geração de chassis vinculados às ordens de produção.

---

## ⚙️ Configuração da API Key (Mockaroo)

Antes de executar, abra o arquivo `script.js` e substitua a chave pela fornecida na plataforma da PUC-Rio:

```javascript
// script.js — linha 4
const MOCKAROO_API_KEY = ''; // Altere aqui APIKEY
```

Essa é a única alteração necessária — todas as requisições ao Mockaroo usam essa variável automaticamente.

---

## 🚀 Executando o projeto completo (Front + Back)

O front e o back rodam juntos via **Docker Compose**. O arquivo `docker-compose.yml` fica em uma pasta raiz que contém as duas pastas dos repositórios.

### Estrutura esperada de pastas

```
pasta-raiz/
├── docker-compose.yml   ← arquivo de orquestração
├── front/               ← repositório do front-end
└── back_v2/             ← repositório do back-end
```

### Passos

1. Clone os dois repositórios dentro de uma mesma pasta raiz:

```bash
git clone <url-repositorio-front> front
git clone <url-repositorio-back> back_v2
```

2. Coloque o `docker-compose.yml` na pasta raiz (ele já está disponível no repositório do front).

3. Na pasta raiz, suba os containers:

```bash
docker compose up --build
```

4. Acesse:
   - **Front-end:** `http://localhost`
   - **API (Swagger):** `http://localhost:5000/openapi/swagger`

### Para derrubar os containers

```bash
docker compose down
```

---

## 🗂️ Estrutura do Front

```
front/
├── index.html      # Interface principal
├── script.js       # Lógica e chamadas à API
├── style.css       # Estilos
├── messias.svg     # Logo
└── Dockerfile      # Build do container Nginx
```

---

## 🌐 Componentes consumidos

| Componente | Endereço |
|---|---|
| Back-end (API Flask) | `http://localhost:5000` |
| Mockaroo (API externa) | `https://api.mockaroo.com` / `https://my.api.mockaroo.com` |
