
# 📊 Pulso do Mercado - API de Dados Financeiros

API desenvolvida em FastAPI para centralizar o acesso a dados econômicos e financeiros do Brasil e do mundo. Suporta rotas públicas com limitação de uso e rotas premium para usuários autenticados via frontend.

---

## 🚀 Como executar o projeto localmente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/pulso-do-mercado.git
cd pulso-do-mercado

# (Opcional) Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn app.main:app --reload --port 8002
```

---

## 🧪 Testar via Swagger

Acesse [http://localhost:8002/docs](http://localhost:8002/docs)

> ⚠️ O Swagger é usado apenas para **documentação**.  
> Autenticação com token JWT é feita **via frontend** e não é obrigatória para o uso básico da API.

---

## 🔐 Como funciona o acesso

- **Usuários anônimos** têm acesso gratuito com limitação de requisições.
- **Usuários Pro** (autenticados via frontend) têm acesso completo usando JWT.
- A autenticação ocorre apenas no frontend. O token é enviado via `Authorization: Bearer <token>`.

---

## 📂 Estrutura do projeto

```
app/
├── core/                  # Conexão com banco e segurança (JWT)
│   └── security/
│       └── jwt_auth.py
├── models/                # Modelos de dados (User, indicadores)
├── routes/                # Rotas de indicadores e autenticação
│   ├── selic.py
│   ├── ipca.py
│   ├── ...
│   └── token.py
├── scripts/               # Scripts utilitários (ex: seed de usuário demo)
├── middleware/            # Middlewares úteis (ex: logging)
├── security/              # Swagger customizado
└── main.py
```

---

## 📌 Rotas disponíveis (MVP)

- `GET /api/selic` → dados de SELIC
- `GET /api/ipca` → dados de IPCA
- `GET /api/cdi` → dados de CDI
- `POST /token` → geração de JWT (via frontend)
- `GET /me` → retorno de dados do usuário autenticado

---

## 🛡️ Roadmap próximo

- Implementar rate limit para usuários anônimos vs autenticados
- Criar painel frontend para login e gestão de tokens
- Adicionar fontes reais com scraping (ex: Infomoney)
- Expandir endpoints com dados históricos e agrupamentos

---

Pulso do Mercado © 2025
