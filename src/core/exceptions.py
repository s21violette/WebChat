from fastapi import HTTPException, status

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)

insert_user_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User with such nickname already exists"
)

lost_connection_exception = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Connection to database lost"
)
