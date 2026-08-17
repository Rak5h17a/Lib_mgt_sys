from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_database
from app.core.security import hash_password, verify_password, create_access_token
from app.domain.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse

router =  APIRouter(prefix="/auth", tags=["auth"])

def get_user_repository() -> UserRepository:
    return UserRepository(get_database())

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, repo: UserRepository = Depends(get_user_repository)):
    # not allowing duplicate username
    existing = await repo.get_by_username(payload.username)
    if existing is not None:
        raise HTTPException(status_code=400, detail = "Username already taken")

    hashed= hash_password(payload.password)
    user =  User(payload.username, hashed, payload.role)
    user_id=await repo.create(user.to_dict())

    return UserResponse(id=user_id, username=user.username, role=user.role)

@router.post("/login")
async def login(payload: UserLogin, repo: UserRepository = Depends(get_user_repository)):
    # find user
    user_data= await repo.get_by_username(payload.username)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    #verify password
    if not verify_password(payload.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # if correct issue a token containing their id and role
    token=create_access_token(user_id=user_data["id"], role=user_data["role"])
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
async def login_for_token(
    form_data: OAuth2PasswordRequestForm =Depends(),
    repo: UserRepository= Depends(get_user_repository),
):
    user_data= await repo.get_by_username(form_data.username)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token =create_access_token(user_id=user_data["id"], role=user_data["role"])
    return {"access_token": token, "token_type": "bearer"}    