import json

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.settings import settings
from app.core.database import create_db_and_tables
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import limiter
from app.routes.v1.registry import include_v1_routes
from app.security.openapi_schema import custom_openapi

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do FastAPI
app = FastAPI(title="Pulso do Mercado API")

# Adiciona middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)

# Configura o esquema OpenAPI
app.openapi = lambda: custom_openapi(app)

# Configura o rate limiter
app.state.limiter = limiter


# Evento de inicialização para o banco de dados
@app.on_event("startup")
async def startup_event():
    await init_db()


# Tratamento de exceção para Rate Limit
@app.exception_handler(RateLimitExceeded)
async def _rate_limit_exceeded_handler(
        request: Request,
        exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Limite de requisições excedido. Tente novamente mais tarde.",
            "message": str(exc),
        },
    )


# Rota raiz
@app.get("/")
def read_root():
    return {
        "message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."
    }


# Inclui as rotas da versão 1
include_v1_routes(app)

# Endpoint para exportar OpenAPI

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_json():
    return get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
        description="Documentação da API Pulso do Mercado",
    )
