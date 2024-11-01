from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, CurrentUser, RoleChecker

# Utils
from app.utils.dependences import CustomPagePagination as Page
from app.utils.enum.enum_role import RoleEnum

# Schemas
from app.operation.schema import (
    OperationCreateSchema,
    OperationBaseSchema,
    UpdateOperationSchema,
    StateOperationCreateSchema,
    StateOperationBaseSchema,
    StateOperationUpdateSchema
)

# Services
import app.operation.service as OperationService


role_checker_state = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value]))
role_checker_operator = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value, RoleEnum.OPERATOR.value]))

router = APIRouter(tags=["Operation"], prefix="/operation", dependencies=[role_checker_operator])
state_operation = APIRouter(tags=["Operation State"], prefix="/operation_state", dependencies=[role_checker_state])


@router.get("/all", response_model=Page[OperationBaseSchema])
def get_all_operations_controller(db: SessionDep, params: Params = Depends()):
    return OperationService.get_all_operation(db=db, params=params)

@router.get("/{operation_id}/details", response_model=OperationBaseSchema)
def get_operation_by_id_controller(db: SessionDep, operation_id: int):
    return OperationService.get_operation_by_id(db=db, operation_id=operation_id)

@router.post("", response_model=OperationBaseSchema)
def create_operation_controller(db: SessionDep, operation: OperationCreateSchema):
    return OperationService.create_operation(db=db, operation=operation)

@router.put("", response_model=OperationBaseSchema)
def update_operation_controller(db: SessionDep, operation: UpdateOperationSchema):
    return OperationService.update_operation(db=db, operation=operation)

@router.delete("/{operation_id}")
def delete_operation_controller(db: SessionDep, operation_id: int):
    return OperationService.delete_operation(db=db, id=operation_id)



# State Operation
@state_operation.get("/all", response_model=Page[StateOperationBaseSchema])
def get_all_state_operations_controller(db: SessionDep, params: Params = Depends()):
    return OperationService.get_all_state_operation(db=db, params=params)

@state_operation.get("/{state_operation_id}", response_model=StateOperationBaseSchema)
def get_state_operation_by_id_controller(db: SessionDep, state_operation_id: int):
    return OperationService.get_state_operation_by_id(db=db, id=state_operation_id)

@state_operation.post("", response_model=StateOperationBaseSchema)
def create_state_operation_controller(db: SessionDep, state_operation: StateOperationCreateSchema):
    return OperationService.create_state_operation(db=db, state_operation=state_operation)

@state_operation.put("")
def update_state_operation_controller(db: SessionDep, state_operation: StateOperationUpdateSchema):
    return OperationService.update_state_operation(db=db, state_operation=state_operation)

@state_operation.delete("/{state_operation_id}")
def delete_state_operation_controller(db: SessionDep, state_operation_id: int):
    return OperationService.delete_state_operation(db=db, id=state_operation_id)