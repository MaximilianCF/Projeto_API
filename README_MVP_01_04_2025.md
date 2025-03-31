# Pulso do Mercado API 🚀

**Versão MVP 1.0 – Entregue em 01/04/2025**

Esta é a primeira versão funcional da API Pulso do Mercado, um projeto focado em consolidar dados econômicos e financeiros em uma única interface moderna, segura e extensível. O MVP representa a camada 1 da nossa stack: a **API de dados**.

---

## ✅ Funcionalidades implementadas (MVP)

- 🔐 Autenticação via JWT
- 🧪 Testes automatizados com `pytest`
- ⚙️ CI/CD com GitHub Actions + Render
- 🧵 Middleware de logging com rastreamento de requisições
- 🐞 Integração com Sentry (modo condicional PROD/DEV)
- 🧠 Banco de dados local com `SqlModel` (SQLite)
- 📊 Endpoints de dados:
    - SELIC (via CSV/SGS BCB)
    - CDI
    - IBOVESPA
    - S&P 500
    - US Treasury 10Y
    - IPCA (local)
    - USD/BRL
    - Webscraping do Infomoney
- 👤 Sistema de usuários (com rotas protegidas)
- 🪛 Scripts auxiliares: seed de usuário demo

---

## 🛠️ Em desenvolvimento

- 🧩 Separação de schemas de entrada e saída
- 🌐 Exportação OpenAPI em `.yaml`
- 📄 Documentação externa em Markdown (`docs/api.md`)
- 🔎 Mais endpoints por scraping/API (FRED, IBGE, Tesouro Direto, etc)
- 🌱 Banco de dados SQL (PostgreSQL em produção)

---

## 📌 Rodando localmente

```bash
# Clonar o repositório
git clone https://github.com/MaximilianCF/Projeto_API.git
cd Projeto_API

# Rodar com Docker
docker-compose up --build

# Acessar documentação
http://localhost:8000/docs

🧬 Tecnologias
Python 3.11

FastAPI

SQLModel

Docker + Render

GitHub Actions (CI)

Sentry

BeautifulSoup4

httpx

pytest

✨ Visão futura
O Pulso do Mercado será composto por 3 camadas:

API de dados (esta etapa) 📡

Camada de comunidade e desafios técnicos (estilo Kaggle) 🤝

Marketplace e soluções premium com DaaS++ 💼

--

Feito com 💡 por Max e Hal