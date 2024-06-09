from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import Token
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()
) -> Token:
    return await auth_service.get_token(form_data=form_data)


@router.post("/register")
async def register_user(username: str, password: str, auth_service: AuthService = Depends()) -> None:
    await auth_service.register_user(username=username, password=password)
