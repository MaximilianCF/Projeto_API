from fastapi import APIRouter
from app.services.ipca_service import get_ipca_data, generate_ipca_analysis

router = APIRouter(prefix="/ipca")  # <- isso é o que faltava!

@router.get("/")
async def read_ipca():
    data = get_ipca_data()
    analysis = generate_ipca_analysis(data)
    return {
        "dados": data,
        "analise": analysis
    }
