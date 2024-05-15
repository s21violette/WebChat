from fastapi import FastAPI

from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache

from redis import asyncio as aioredis

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from pages.router import router as router_pages
from chat.router import router as router_chat

app = FastAPI(
    title="test"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(router_pages)
app.include_router(router_chat)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
