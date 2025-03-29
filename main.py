# main.py

#Os comandos abaixo estão comentados para evitar a execução de código desnecessário
#Comentei o Sentry pois não está sendo utilizado no momento

#import sentry_sdk

#sentry_sdk.init(
#    dsn="https://a34502bf8869b33a2a794d71a97af2c6@o4509056723976192.ingest.de.sentry.io/4509056728432720",
#    traces_sample_rate=1.0
#)

from fastapi import FastAPI
from dotenv import load_dotenv
from core.database import create_db_and_tables

# Carrega variáveis do .env
load_dotenv()

# Importa todos os routers já existentes
from routes.selic import router as selic_router
from routes.ibov import router as ibov_router
from routes.cambio import router as cambio_router
from routes.cdi import router as cdi_router
from routes.sp500 import router as sp500_router
from routes.treasury import router as treasury_router
from routes.selic_csv import router as selic_csv_router
from routes.ipca import router as ipca_router
from routes.usdbrl import router as usdbrl_router 


app = FastAPI(title="Pulso do Mercado API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Rotas principais organizadas
app.include_router(selic_router, prefix="/api", tags=["SELIC"])
app.include_router(ibov_router, prefix="/api", tags=["IBOVESPA"])
app.include_router(cambio_router, prefix="/api", tags=["CÂMBIO"])
app.include_router(cdi_router, prefix="/api", tags=["CDI"])
app.include_router(sp500_router, prefix="/api", tags=["S&P 500"])
app.include_router(treasury_router, prefix="/api", tags=["US Treasury"])
app.include_router(selic_csv_router, prefix="/api", tags=["SELIC CSV"])
app.include_router(ipca_router, prefix="/ipca", tags=["IPCA"])
app.include_router(usdbrl_router, prefix="/usdbrl", tags=["USD/BRL"])
