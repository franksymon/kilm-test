from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params

# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page


# Schemas
from app.user.schema import UserCreateSchema, UserBaseSchema

# Services
from app.user.service import (
    create_user,
    get_user_by_email,
    get_all_user,
    delete_user,
    update_password,
)

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/all", response_model=Page[UserBaseSchema])
def get_all_users(db: SessionDep, params: Params = Depends()):
    return get_all_user(db=db, params=params)


@router.get("/email/{email}", response_model=UserBaseSchema)
def get_a_user(db: SessionDep, email: EmailStr):
    return get_user_by_email(de=db, email=email)


@router.post("", response_model=UserBaseSchema)
def create_a_user(db: SessionDep, user: UserCreateSchema):
    return create_user(db=db, user=user)


@router.delete("/email/{email}")
def delete_a_user(db: SessionDep, email: EmailStr):
    return delete_user(db=db, email=email) 


