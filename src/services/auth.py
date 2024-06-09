from typing import Union
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from core.exceptions import credentials_exception
from db.repository.auth import AuthRepository
from schemas.auth import TokenData, Token, UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, auth_repository: AuthRepository = Depends()):
        self._auth_repository = auth_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserSchema:
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = await self._auth_repository.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(secret=plain_password, hash=hashed_password)

    async def get_token(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self._auth_repository.get_user(form_data.username)
        if not self.verify_password(plain_password=form_data.password, hashed_password=user.hashed_password) or not user:
            raise credentials_exception

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    async def register_user(self, username: str, password: str) -> None:
        hashed_password = self._pwd_context.hash(secret=password)
        await self._auth_repository.register_user(username=username, hashed_password=hashed_password)
