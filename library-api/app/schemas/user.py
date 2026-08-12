from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.MEMBER #deafult

class UserLogin(BaseModel):
    username: str 
    password: str 

class UserResponse(BaseModel):
    id: str 
    username: str
    role: UserRole