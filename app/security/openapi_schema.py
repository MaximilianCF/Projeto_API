# app/security/openapi_schema.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Documentação da API Pulso do Mercado",
        routes=app.routes,
        # Você PODE adicionar security schemes aqui se precisar customizar,
        # mas geralmente o FastAPI detecta baseado nas dependências.
        # A linha abaixo foi removida/comentada:
        # openapi_schema.pop("components", None)
    )
    # Se você quiser garantir que NENHUMA rota peça auth por padrão globalmente,
    # o correto seria mexer em openapi_schema.get("security"), e não remover "components".
    # Mas geralmente é melhor definir segurança por rota ou por router.

    app.openapi_schema = openapi_schema
    return app.openapi_schema
