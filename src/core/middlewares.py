from fastapi_keycloak_middleware import KeycloakMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

middleware = [
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings().CORS_ALLOW_ORIGIN_LIST,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

if settings().CHECK_KEYCLOAK_AUTH:
    middleware.append(
        Middleware(
            KeycloakMiddleware,
            keycloak_configuration=settings().keycloak_config,
            exclude_patterns=settings().KEYCLOAK_EXCLUDED_ROUTES,
        )
    )
