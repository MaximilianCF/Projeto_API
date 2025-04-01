
# app/main.py

from app.routes import users
from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.middleware.logging import LoggingMiddleware
from app.security.openapi_schema import custom_openapi
from app.routes import token, me
from app.routes import selic, ipca, cdi, ibov, sp500, usdbrl, treasury

load_dotenv()

app = FastAPI(title="Pulso do Mercado API")

# Middleware de logging
app.add_middleware(LoggingMiddleware)

# Documentação Swagger customizada
app.openapi = lambda: custom_openapi(app)

@app.get("/")
def read_root():
    return {"message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."}

# Rotas públicas de indicadores
app.include_router(selic.router, prefix="/api", tags=["SELIC"])
app.include_router(ipca.router, prefix="/api", tags=["IPCA"])
app.include_router(cdi.router, prefix="/api", tags=["CDI"])
app.include_router(ibov.router, prefix="/api", tags=["IBOVESPA"])
app.include_router(sp500.router, prefix="/api", tags=["S&P 500"])
app.include_router(usdbrl.router, prefix="/api", tags=["USD/BRL"])
app.include_router(treasury.router, prefix="/api", tags=["US Treasury"])
app.include_router(users.router, prefix="/api", tags=["Usuários"])

# Autenticação e dados do usuário autenticado
app.include_router(token.router, tags=["Autenticação"])
app.include_router(me.router, prefix="/api", tags=["Usuário"])
