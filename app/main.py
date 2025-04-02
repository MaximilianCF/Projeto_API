# app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv

from app.middleware.logging import LoggingMiddleware
from app.security.openapi_schema import custom_openapi

# Routers
from app.routes.selic import router as selic_router
from app.routes.ipca import router as ipca_router
from app.routes.cdi import router as cdi_router
from app.routes.ibov import router as ibov_router
from app.routes.sp500 import router as sp500_router
from app.routes.usdbrl import router as usdbrl_router
from app.routes.treasury import router as treasury_router
from app.routes.users import router as users_router
from app.routes.token import router as token_router
from app.routes.me import router as me_router
from app.routes.status import router as status_router
from app.routes.protected import router as protected_router
from app.routes.infomoney import router as infomoney_router

load_dotenv()

app = FastAPI(title="Pulso do Mercado API")

# Middleware
app.add_middleware(LoggingMiddleware)

# Documentação customizada
app.openapi = lambda: custom_openapi(app)

@app.get("/")
def read_root():
    return {"message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."}

# Indicadores públicos
app.include_router(selic_router, prefix="/api", tags=["SELIC"])
app.include_router(ipca_router, prefix="/api", tags=["IPCA"])
app.include_router(cdi_router, prefix="/api", tags=["CDI"])
app.include_router(ibov_router, prefix="/api", tags=["IBOVESPA"])
app.include_router(sp500_router, prefix="/api", tags=["S&P 500"])
app.include_router(usdbrl_router, prefix="/api", tags=["USD/BRL"])
app.include_router(treasury_router, prefix="/api", tags=["US Treasury"])

# Usuários e autenticação
app.include_router(users_router, prefix="/api/users", tags=["Usuários"])
app.include_router(token_router, prefix="/api/token", tags=["Autenticação"])
app.include_router(me_router, prefix="/api", tags=["Usuário"])

# Rota protegida (para testes de token)
app.include_router(protected_router, prefix="/api", tags=["Protegido"])

# Webscraping
app.include_router(infomoney_router, prefix="/api/webscraping", tags=["Webscraping"])

# Status da API
app.include_router(status_router, prefix="/api", tags=["Status"])
