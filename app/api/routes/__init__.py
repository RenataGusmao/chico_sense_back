from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router
from app.modules.integracoes.thingspeak.routes import router as thingspeak_router
from app.modules.auth.routes import router as auth_router
from app.api.routes.usuarios import router as usuarios_router
from app.modules.empresas.routes import router as empresas_router
from app.modules.produtos.routes import router as produtos_router
from app.modules.logistica.routes import router as logistica_router

api_router = APIRouter()
api_router.include_router(root_router)
api_router.include_router(health_router)
api_router.include_router(thingspeak_router)
api_router.include_router(auth_router)
api_router.include_router(usuarios_router)
api_router.include_router(empresas_router)
api_router.include_router(produtos_router)
api_router.include_router(logistica_router)
