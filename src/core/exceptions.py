from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

insert_user_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with such nickname already exists"
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User with such nickname doesn't exist"
)

lost_connection_exception = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Connection to database lost"
)

database_initialization_exception = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT, detail="Not all needed tables are initialized"
)
