from sqlmodel import Session, select, func
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlmodel import paginate

# Models
from app.role.model import RoleEntity

# Utils
from app.utils.responses import ResponseHandler

# Schemas
from app.role.schema import (
    RoleBaseSchema,
    RoleCreateSchema,
    RoleUpdateSchema,
)


def get_all_role(db: Session, params: Params):
    query = select(RoleEntity)
    return paginate(db, query, params)


def get_role_by_id(db: Session, id: int):
    role = db.get(RoleEntity, id)
    if not role:
        raise ResponseHandler.not_found_error("Role", id)
    return role


def create_role(db: Session, role: RoleCreateSchema):
    
    role_exists = db.exec(select(RoleEntity).where(RoleEntity.name == role.name)).first()
    if role_exists:
        raise ResponseHandler.duplicate_error("Role", role.name)
    
    db_role = RoleEntity.model_validate(role, update={"created_by": "user_test"})
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role: RoleUpdateSchema):
    db_role = db.get(RoleEntity, role.id)
    if not db_role:
        raise ResponseHandler.not_found_error("Role", role.id)

    db_role.is_active = role.is_active
    db_role.updated_by = "user_test"
    db_role.time_updated = func.now()

    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, id: int):
    db_role = db.get(RoleEntity, id)
    if not db_role:
        raise ResponseHandler.not_found_error("Role", id)
    db.delete(db_role)
    db.commit()
    return ResponseHandler.delete_success("Role", id, db_role)