from fastapi import APIRouter

from api.healthcheck import router as healthcheck_router
from api.v1.auth import router as auth_router
from api.v1.chat import router as chat_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(chat_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
api_router.include_router(healthcheck_router)

routes = api_router.routes
