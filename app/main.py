# main.py

from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from datetime import timedelta
from pydantic import BaseModel

# internos (app.)
from app.core.database import create_db_and_tables
from app.core.security.jwt_auth import create_access_token, verify_token

# Carrega variáveis do .env
load_dotenv()

# Modelo simples para autenticação (para testes/demo)
class User(BaseModel):
    username: str
    password: str

# Rotas internas (ajustadas corretamente)
from app.routes.selic import router as selic_router
from app.routes.ibov import router as ibov_router
from app.routes.cambio import router as cambio_router
from app.routes.cdi import router as cdi_router
from app.routes.sp500 import router as sp500_router
from app.routes.treasury import router as treasury_router
from app.routes.selic_csv import router as selic_csv_router
from app.routes.ipca import router as ipca_router
from app.routes.usdbrl import router as usdbrl_router 
from app.routes import users_router
from app.routes import challenges_router
from app.routes import submissions_router

app = FastAPI(title="Pulso do Mercado API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Rota atualizada para criar Token JWT
@app.post('/api/token')
async def login(user: User):
    if user.username != "usuario_demo" or user.password != "senha_demo":
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rota protegida atualizada com JWT
@app.get('/api/protected')
async def protected(token_data=Depends(verify_token)):
    return {"message": f"Bem-vindo(a), {token_data.username}!"}

# Rotas principais
app.include_router(selic_router, prefix="/api", tags=["SELIC"])
app.include_router(ibov_router, prefix="/api", tags=["IBOVESPA"])
app.include_router(cambio_router, prefix="/api", tags=["CÂMBIO"])
app.include_router(cdi_router, prefix="/api", tags=["CDI"])
app.include_router(sp500_router, prefix="/api", tags=["S&P 500"])
app.include_router(treasury_router, prefix="/api", tags=["US Treasury"])
app.include_router(selic_csv_router, prefix="/api", tags=["SELIC CSV"])
app.include_router(ipca_router, prefix="/ipca", tags=["IPCA"])
app.include_router(usdbrl_router, prefix="/usdbrl", tags=["USD/BRL"])
app.include_router(users_router, prefix="/api", tags=["USERS"])
app.include_router(challenges_router, prefix="/api/challenges", tags=["CHALLENGES"])
app.include_router(submissions_router, prefix="/api/submissions", tags=["SUBMISSIONS"])
