from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_database
from app.core.security import decode_access_token
from app.domain.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRole

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="auth/token")

def _get_user_repository() -> UserRepository:
    return UserRepository(get_database())

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        repo: UserRepository = Depends(_get_user_repository),) -> User:

    #read the bearer token ,verify it and return the logged in user, reject with 401 if token missing , invalid or expired
    credentials_error= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    #decode and verify token
    payload= decode_access_token(token)
    if payload is None:
        raise credentials_error

    #pull userid out of token's payload
    user_id= payload.get("sub")
    if user_id is None:
        raise credentials_error

    #look the user up in db
    user_data= await repo.get_by_id(user_id)
    if user_data is None:
        raise credentials_error

    #rebuild and return the user object
    return User(
        username=user_data["username"],
        hashed_password=user_data["hashed_password"],
        role=UserRole(user_data["role"]),
    )

async def require_admin(current_user:User=Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
