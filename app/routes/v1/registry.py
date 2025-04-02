# app/routes/v1/registry.py

from fastapi import FastAPI

from app.routes.v1 import (
    selic,
    ipca,
    cdi,
    ibov,
    sp500,
    usdbrl,
    treasury,
    users,
    token,
    me,
    infomoney,
    protected,
    status,
)

def include_v1_routes(app: FastAPI):
    app.include_router(selic.router, prefix="/api/v1", tags=["SELIC"])
    app.include_router(ipca.router, prefix="/api/v1", tags=["IPCA"])
    app.include_router(cdi.router, prefix="/api/v1", tags=["CDI"])
    app.include_router(ibov.router, prefix="/api/v1", tags=["IBOVESPA"])
    app.include_router(sp500.router, prefix="/api/v1", tags=["S&P 500"])
    app.include_router(usdbrl.router, prefix="/api/v1", tags=["USD/BRL"])
    app.include_router(treasury.router, prefix="/api/v1", tags=["US Treasury"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Usuários"])
    app.include_router(token.router, prefix="/api/v1/token", tags=["Autenticação"])
    app.include_router(me.router, prefix="/api/v1", tags=["Usuário"])
    app.include_router(infomoney.router, prefix="/api/v1/webscraping", tags=["WEBSCRAPING"])
    app.include_router(protected.router, prefix="/api/v1")
    app.include_router(status.router, prefix="/api/v1", tags=["Status"])
