from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params

from app.transaction.service import TransactionService

# Config
from app.core.security import SessionDep, CurrentUser, RoleChecker

# Utils
from app.utils.dependences import CustomPagePagination as Page
from app.utils.enum.enum_role import RoleEnum

# Schemas
from app.transaction.schema import (
    TransactionCreateSchema,
    TransactionSchema,
    TransactionByUserSchema,
    TransactionByOperationSchema,
)



role_checker = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value, RoleEnum.OPERATOR.value, RoleEnum.INVESTOR.value]))
router = APIRouter(tags=["Transaction"], prefix="/transaction", dependencies=[role_checker])
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
