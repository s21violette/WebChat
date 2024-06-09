from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services.auth import AuthService
from schemas.auth import Token, UserSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 auth_service: AuthService = Depends()) -> Token:
    token = await auth_service.get_token(form_data=form_data)

    return token


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()) -> UserSchema:
    current_user = await auth_service.get_current_user(token=token)

    return current_user


@router.get("/users/me/items/")
async def read_own_items(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()):
    current_user = await auth_service.get_current_user(token=token)

    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/register")
async def register_user(username: str, password: str, auth_service: AuthService = Depends()) -> None:
    await auth_service.register_user(username=username, password=password)
