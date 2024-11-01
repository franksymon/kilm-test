from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params

from app.transaction.service import TransactionService

# Schemas
from app.transaction.schema import (
    TransactionCreateSchema,
    TransactionSchema,
    TransactionByUserSchema,
    TransactionByOperationSchema,
)

# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page

router = APIRouter(tags=["Transaction"], prefix="/transaction")
service = TransactionService()

# @router.get("/all/by_operation/{operation_id}", response_model=Page[TransactionByOperationSchema])
# def get_all_transactions_by_operation(db: SessionDep, operation_id: int, params: Params = Depends()):
#     return service.get_all_transactions_by_operation(db=db, operation_id=operation_id, params=params)

@router.get("/all/by_user/{user_id}", response_model=Page[TransactionByUserSchema])
def get_all_transactions_by_user(db: SessionDep, user_id: int, params: Params = Depends()):
    return service.get_all_transactions_by_user(db=db, user_id=user_id, params=params)

# @router.post("/create/by_operation", response_model=TransactionSchema)
# def create_transaction(db: SessionDep, transaction: TransactionCreateSchema):
#     return service.create_transaction(db=db, transaction=transaction)

@router.post("/create_by_user/{user_id}", response_model=TransactionSchema)
def create_transaction_by_user(db: SessionDep,  transaction: TransactionCreateSchema, user_id: int,):
    return service.create_transaction_by_user(db=db, transaction=transaction, user_id=user_id)
