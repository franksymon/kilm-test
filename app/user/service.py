from sqlmodel import Session, select, func
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params


# Config
from app.core.security import verify_password, hash_password

# Utils
from app.utils.responses import ResponseHandler

# Models
from app.user.model import UserEntity
from app.role.model import RoleEntity

# Schemas
from app.user.schema import UserCreateSchema, UserBaseSchema

def create_user(db: Session, user: UserCreateSchema, ):
    
    user_exists = db.exec(select(UserEntity).where(UserEntity.email == user.email or UserEntity.username == user.username)).first()
    if user_exists:
        raise ResponseHandler.not_found_error("User", user.id)
    
    get_role = db.get(RoleEntity, user.role_id)
    if not get_role:
        raise ResponseHandler.not_found_error("Role", user.role_id)
    
    if not get_role.is_active:
        raise ResponseHandler.is_not_active("Role", get_role.name)

    db_user = UserEntity.model_validate(
        user, update={"hashed_password": hash_password(user.password), "created_by": "user_test"}
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str, ) -> UserBaseSchema | None:
    return db.exec(select(UserEntity).where(UserEntity.email == email)).first()

def get_all_user(db: Session, params: Params):
    query = select(UserEntity)
    return paginate(db, query, params)

def delete_user(db: Session, email: str):
    
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise ResponseHandler.not_found_error("User", email)
    
    db.delete(user)
    db.commit()
    return ResponseHandler.delete_success("User", user.id, user)

def update_password(db: Session, user: UserEntity, password: str, ):

    if not verify_password(password, user.hashed_password):
        raise ResponseHandler.not_found_error("User", user.id)

    user.hashed_password = hash_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
