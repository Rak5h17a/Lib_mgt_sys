from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings

ALGORITHM = "HS256"

#this hash tool uses bcrypt
_pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, role: str) -> str:
    #creates signed jwt containing user id and role.
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    #verify jwt signature and expiry
    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None