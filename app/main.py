from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import limiter
from app.security.openapi_schema import custom_openapi
#from app.core.limiter import limiter
from app.routes.v1 import (
    selic, ipca, cdi, ibov, sp500, usdbrl, treasury,
    users, token, me
)
from app.routes.v1.status import router as status_router
from app.routes.v1.users import router as users_router
from app.routes.v1.token import router as token_router
from app.routes.v1.protected import router as protected_router
from app.routes.v1.infomoney import router as infomoney_router
from app.routes.v1.registry import include_v1_routes

load_dotenv()

app = FastAPI(title="Pulso do Mercado API")
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)  # (opcional, mas recomendado)
app.openapi = lambda: custom_openapi(app)
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Limite de requisições excedido. Tente novamente mais tarde.",
            "message": str(exc),
        },
    )
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/")
def read_root():
    return {"message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."}

include_v1_routes(app)

# endpoint para exportar OpenAPI
from fastapi.openapi.utils import get_openapi
import json

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_json():
    return get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
        description="Documentação da API Pulso do Mercado"
    )
