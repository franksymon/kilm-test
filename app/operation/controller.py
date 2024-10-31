from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page

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
from app.operation.service import (
    create_operation,
    get_all_operation,
    get_operation_by_id,
    update_operation,
    delete_operation,
    create_state_operation,
    get_all_state_operation,
    get_state_operation_by_id,
    update_state_operation,
    delete_state_operation
)


router = APIRouter(tags=["Operation"], prefix="/operation")


@router.get("/all", response_model=Page[OperationBaseSchema])
def get_all_operations_controller(db: SessionDep, params: Params = Depends()):
    return get_all_operation(db=db, params=params)

@router.get("/{id}", response_model=OperationBaseSchema)
def get_operation_by_id_controller(db: SessionDep, id: int):
    return get_operation_by_id(db=db, id=id)

@router.post("", response_model=OperationBaseSchema)
def create_operation_controller(db: SessionDep, operation: OperationCreateSchema):
    return create_operation(db=db, operation=operation)

@router.put("", response_model=OperationBaseSchema)
def update_operation_controller(db: SessionDep, operation: UpdateOperationSchema):
    return update_operation(db=db, operation=operation)

@router.delete("/{id}")
def delete_operation_controller(db: SessionDep, id: int):
    return delete_operation(db=db, id=id)

# State Operation
@router.get("/state/all", response_model=Page[StateOperationBaseSchema])
def get_all_state_operations_controller(db: SessionDep, params: Params = Depends()):
    return get_all_state_operation(db=db, params=params)

@router.get("/state/{id}", response_model=StateOperationBaseSchema)
def get_state_operation_by_id_controller(db: SessionDep, id: int):
    return get_state_operation_by_id(db=db, id=id)

@router.post("/state", response_model=StateOperationBaseSchema)
def create_state_operation_controller(db: SessionDep, state_operation: StateOperationCreateSchema):
    return create_state_operation(db=db, state_operation=state_operation)

@router.put("/state/{id}")
def update_state_operation_controller(db: SessionDep, state_operation: StateOperationUpdateSchema):
    return update_state_operation(db=db, state_operation=state_operation)

@router.delete("/state/{id}")
def delete_state_operation_controller(db: SessionDep, id: int):
    return delete_state_operation(db=db, id=id)