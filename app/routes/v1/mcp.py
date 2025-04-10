from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai_client import gerar_codigo_analise

router = APIRouter(prefix="/api/v1/mcp", tags=["MCP"])

class MCPRequest(BaseModel):
    ticker: str

@router.post("/")
async def executar_analise(request: MCPRequest):
    try:
        codigo = gerar_codigo_analise(request.ticker.upper())
        return {"codigo": codigo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))