from datetime import datetime, timedelta, timezone
from typing import Any, Annotated
from fastapi import Depends
from sqlmodel import Session
from jwt import exceptions, encode, decode
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from passlib.context import CryptContext

# Config
from config.config import settings
from app.core.db import get_session

# Utils
from app.utils.responses import ResponseHandler

# Models
from app.user.model import UserEntity

# Schemas
from app.auth.schema import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TokenDep = Annotated[str, Depends(reusable_oauth2)]
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[UserEntity, Depends(lambda: get_current_user)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(db: SessionDep, token: TokenDep) -> UserEntity:
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (exceptions.InvalidTokenError, ValidationError):
        raise ResponseHandler.invalid_token('access')
    
    user = db.get(UserEntity, token_data.sub)
    if not user:
        raise ResponseHandler.not_found_error("User")
    if not user.is_active:
        raise ResponseHandler.is_not_active(f" User {user.username}")
    return user


def create_access_token(user: UserEntity | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.name,
    }
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_active_user(
    current_user: CurrentUser,
):
    if not current_user.is_active:
        raise ResponseHandler.is_not_active(f" User {current_user.username}")
    return current_user


# class RoleChecker:
#     def __init__(self, allowed_roles: List[str]) -> None:
#         self.allowed_roles = allowed_roles

#     def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
#         if not current_user.is_verified:
#             raise AccountNotVerified()
#         if current_user.role in self.allowed_roles:
#             return True

#         raise InsufficientPermission()


