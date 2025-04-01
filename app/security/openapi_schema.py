# app/security/openapi_schema.py

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Documentação da API Pulso do Mercado",
        routes=app.routes,
    )
    # (Opcional) Remover segurança global
    openapi_schema.pop("components", None)
    app.openapi_schema = openapi_schema
    return app.openapi_schema
