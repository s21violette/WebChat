from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from core.exceptions import credentials_exception
from core.config import settings
from db.repository.auth import AuthRepository
from schemas.auth import Token


class AuthService:
    def __init__(self, auth_repository: AuthRepository = Depends()):
        self._auth_repository = auth_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict[str, str], expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": str(expire)})
        encoded_jwt = jwt.encode(to_encode, settings().SECRET_KEY, algorithm=settings().ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(secret=plain_password, hash=hashed_password)

    async def get_token(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self._auth_repository.get_user(form_data.username)
        if (
            not user
            or not self.verify_password(plain_password=form_data.password, hashed_password=user.hashed_password)
        ):
            raise credentials_exception

        access_token_expires = timedelta(minutes=settings().ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        return Token(access_token=access_token, token_type="bearer")

    async def register_user(self, username: str, password: str) -> None:
        hashed_password = self._pwd_context.hash(secret=password)
        await self._auth_repository.register_user(username=username, hashed_password=hashed_password)
