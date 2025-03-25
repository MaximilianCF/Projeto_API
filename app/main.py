from fastapi import FastAPI
from app.routes import ipca

app = FastAPI()

app.include_router(ipca.router)

