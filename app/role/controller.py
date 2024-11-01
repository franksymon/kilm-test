from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, CurrentUser, RoleChecker

# Utils
from app.utils.dependences import CustomPagePagination as Page
from app.utils.enum.enum_role import RoleEnum

# Schemas
from app.role.schema import RoleCreateSchema, RoleBaseSchema, RoleUpdateSchema

# Services
from app.role.service import create_role, get_all_role, get_role_by_id, update_role, delete_role


role_checker = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value]))
router = APIRouter(tags=["Role"], prefix="/role")


@router.get("/all", response_model= Page[RoleBaseSchema])
def get_all_role_controller(db: SessionDep, params: Params = Depends()):
    return get_all_role(db=db, params=params)

@router.post("", response_model=RoleBaseSchema, dependencies=[role_checker])
def create_role_controller(db: SessionDep, role: RoleCreateSchema):
    return create_role(db=db, role=role)

@router.get("/{role_id}", response_model=RoleBaseSchema, dependencies=[role_checker])
def get_role_by_id_controller(db: SessionDep, role_id: int):
    return get_role_by_id(db=db, role_id=id)

@router.put("", response_model=RoleBaseSchema, dependencies=[role_checker])
def update_state_role_controller(db: SessionDep, role: RoleUpdateSchema):
    return update_role(db=db, role=role)

@router.delete("/{role_id}", dependencies=[role_checker])
def delete_role_controller(db: SessionDep, role_id: int):
    return delete_role(db=db, id=role_id)