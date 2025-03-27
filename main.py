# main.py

from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

from routes.selic import router as selic_router
from routes.ibov import router as ibov_router
from routes.cambio import router as cambio_router
from routes.cdi import router as cdi_router
from routes.sp500 import router as sp500_router
from routes.treasury import router as treasury_router

app = FastAPI(title="Pulso do Mercado API")

app.include_router(selic_router, prefix="/api")
app.include_router(ibov_router, prefix="/api")
app.include_router(cambio_router, prefix="/api")
app.include_router(cdi_router, prefix="/api")
app.include_router(sp500_router, prefix="/api")
app.include_router(treasury_router, prefix="/api")
