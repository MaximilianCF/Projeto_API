# main.py

from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from datetime import timedelta
from pydantic import BaseModel
from sqlmodel import Session, select
from app.models.user import User
from app.core.database import get_session
from passlib.context import CryptContext

# internos (app.)
from app.core.database import create_db_and_tables
from app.core.security.jwt_auth import get_current_user, create_access_token, verify_token

# Ativação Sentry-SDK
import os
from dotenv import load_dotenv

# Carrega variáveis antes de tudo
load_dotenv()

import sentry_sdk

if os.getenv("ENV") == "production" and os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        traces_sample_rate=1.0,
        environment="production"
    )

# Modelo simples para autenticação (para testes/demo)
class UserLogin(BaseModel):
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rota atualizada para criar Token JWT
@app.post('/api/token')
async def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Rota protegida atualizada com JWT
@app.get('/api/protected')
async def protected(current_user: User = Depends(get_current_user)):
    return {"message": f"Bem-vindo(a), {current_user.username}!"}


# Rota temporária para testar envio de erros ao Sentry
#@app.get("/api/test-sentry")
#async def test_sentry():
#    raise ValueError("Erro forçado para testar o Sentry 🚨")


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

@app.get("/")
def read_root():
    return {"message": "Pulso do Mercado API rodando com sucesso 🚀. Acesse /docs para a documentação."}
