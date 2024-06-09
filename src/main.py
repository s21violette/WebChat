import uvicorn
from fastapi import FastAPI

from api.router import routes
from core.config import settings
from core.middlewares import middleware

app = FastAPI(
    title="web-chat",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
    routes=routes,
    middleware=middleware,
)


if __name__ == "__main__":
    uvicorn.run(app, host=settings().SERVER_HOST, port=settings().SERVER_PORT)
