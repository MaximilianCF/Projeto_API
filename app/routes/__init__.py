# app/routes/__init__.py

from app.routes.v1.cdi import router as cdi_router
from app.routes.v1.ibov import router as ibov_router
from app.routes.v1.infomoney import router as infomoney_router
from app.routes.v1.ipca import router as ipca_router
from app.routes.v1.me import router as me_router
from app.routes.v1.protected import router as protected_router
from app.routes.v1.selic import router as selic_router
from app.routes.v1.sp500 import router as sp500_router
from app.routes.v1.status import router as status_router
from app.routes.v1.token import router as token_router
from app.routes.v1.treasury import router as treasury_router
from app.routes.v1.usd_brl import router as usd_brl_router
from app.routes.v1.users import router as users_router
