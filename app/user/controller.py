from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params

# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page


# Schemas
from app.user.schema import UserCreateSchema, UserBaseSchema, GetUserSchema

# Services
from app.user.service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_all_user,
    delete_user,
    update_password,
)

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/all", response_model=Page[GetUserSchema])
def get_all_users(db: SessionDep, params: Params = Depends()):
    return get_all_user(db=db, params=params)


@router.get("/{user_id}", response_model=GetUserSchema)
def get_a_user(db: SessionDep, user_id: int):
    return get_user_by_id(db=db, user_id=user_id)


@router.post("", response_model=GetUserSchema)
def create_a_user(db: SessionDep, user: UserCreateSchema):
    return create_user(db=db, user=user)


@router.delete("/{user_id}")
def delete_a_user(db: SessionDep, user_id: int):
    return delete_user(db=db, user_id=user_id)



