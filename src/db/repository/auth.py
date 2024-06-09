from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc, insert, select

from core.exceptions import credentials_exception, insert_user_exception, lost_connection_exception
from db.models.user import User
from db.repository.base import BaseDatabaseRepository
from schemas.auth import UserSchema


class AuthRepository(BaseDatabaseRepository):
    async def get_user(self, username: str) -> UserSchema:
        try:
            query = select(User).where(User.username == username)
            query_result = await self._session.execute(query)
            model_result = query_result.scalar()
            if not model_result:
                raise credentials_exception
        except ConnectionRefusedError:
            raise lost_connection_exception

        return UserSchema.model_validate(jsonable_encoder(model_result))

    async def register_user(self, username: str, hashed_password: str):
        try:
            query = insert(User).values(username=username, hashed_password=hashed_password)
            await self._session.execute(query)
            await self._session.commit()
        except exc.IntegrityError:
            raise insert_user_exception
        except ConnectionRefusedError:
            raise lost_connection_exception
