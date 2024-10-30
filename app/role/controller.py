from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page

# Schemas
from app.role.schema import RoleCreateSchema, RoleBaseSchema, RoleUpdateSchema

# Services
from app.role.service import create_role, get_all_role, get_role_by_id, update_role, delete_role



router = APIRouter(tags=["Role"], prefix="/role")


@router.get("/all", response_model= Page[RoleBaseSchema])
def get_all_role_controller(db: SessionDep, params: Params = Depends()):
    return get_all_role(db=db, params=params)

@router.post("", response_model=RoleBaseSchema)
def create_role_controller(db: SessionDep, role: RoleCreateSchema):
    return create_role(db=db, role=role)

@router.get("/{id}", response_model=RoleBaseSchema)
def get_role_by_id_controller(db: SessionDep, id: int):
    return get_role_by_id(db=db, id=id)

@router.put("/{id}", response_model=RoleBaseSchema)
def update_state_role_controller(db: SessionDep, role: RoleUpdateSchema):
    return update_role(db=db, role=role)

@router.delete("/{id}")
def delete_role_controller(db: SessionDep, id: int):
    return delete_role(db=db, id=id)