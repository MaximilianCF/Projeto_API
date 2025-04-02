from fastapi import FastAPI
from dotenv import load_dotenv
from app.middleware.logging import LoggingMiddleware
from app.security.openapi_schema import custom_openapi

from app.routes.v1 import (
    selic, ipca, cdi, ibov, sp500, usdbrl, treasury,
    users, token, me
)

# 👇 Essas aqui são as novas
from app.routes.v1.status import router as status_router
from app.routes.v1.users import router as users_router
from app.routes.v1.token import router as token_router
from app.routes.v1.protected import router as protected_router
from app.routes.v1.infomoney import router as infomoney_router
from app.routes.v1.registry import include_v1_routes

load_dotenv()

app = FastAPI(title="Pulso do Mercado API")
app.add_middleware(LoggingMiddleware)
app.openapi = lambda: custom_openapi(app)

@app.get("/")
def read_root():
    return {"message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."}

include_v1_routes(app)