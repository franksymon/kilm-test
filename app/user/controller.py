from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params

# Config
from app.core.security import SessionDep, CurrentUser, RoleChecker

# Utils
from app.utils.dependences import CustomPagePagination as Page
from app.utils.enum.enum_role import RoleEnum

# Schemas
from app.user.schema import UserCreateSchema, UserBaseSchema, GetUserSchema

# Services
import app.user.service as UserService


role_checker = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value]))
router = APIRouter(tags=["User"], prefix="/user", dependencies=[role_checker])


@router.get("/all", response_model=Page[GetUserSchema])
def get_all_users(db: SessionDep, _: CurrentUser, params: Params = Depends()):
    return UserService.get_all_user(db=db, params=params)


@router.get("/{user_id}", response_model=GetUserSchema)
def get_a_user(db: SessionDep, user_id: int):
    return UserService.get_user_by_id(db=db, user_id=user_id)


@router.delete("/{user_id}")
def delete_a_user(db: SessionDep, user_id: int):
    return UserService.delete_user(db=db, user_id=user_id)



