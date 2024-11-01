from sqlmodel import Session, select, func
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params
from decimal import Decimal
from datetime import datetime, date

from app.utils.enum.enum_operation_state import OperationState
from app.utils.enum.enum_role import RoleEnum

# Config
from app.core.security import get_current_active_user, get_current_user

# Utils
from app.utils.responses import ResponseHandler

# Models
from app.user.model import UserEntity
from app.operation.model import OperationEntity
from app.bid.model import BidEntity
from app.transaction.model import TransactionEntity

# Schemas
from app.transaction.schema import TransactionCreateSchema, TransactionByUserSchema

# Services
import app.user.service as UserService
import app.operation.service as OperationService


class TransactionService:

    def get_all_transactions_by_user(self, db: Session, user_id: int, params: Params):

        user = UserService.get_user_by_id(db, user_id=user_id)

        query = (
            select(TransactionEntity).distinct()
            .outerjoin(OperationEntity, OperationEntity.id == TransactionEntity.id)
            .outerjoin(BidEntity, BidEntity.operation_id == OperationEntity.id)
            .outerjoin(UserEntity, UserEntity.id == BidEntity.investor_id)
            .where((UserEntity.id == 4) | (UserEntity.id == None))
        )

        return paginate(db, query, params)

    def get_all_transactions_by_operation(self, db: Session, operation_id: int, params: Params):
        ...

    def create_transaction_by_operation(self, db: Session, transaction: TransactionCreateSchema):

        operation = OperationService.get_operation_by_id(db, operation_id=transaction.operation_id)
        if not operation:
            raise ResponseHandler.not_found_error("Operation", transaction.operation_id)

        if not operation.status == OperationState.COMPLETED.value or operation.is_closed:
            raise ResponseHandler.bad_request(f"Operation {operation.title} status is not completed")

        ...

    def create_transaction_by_user(self, db: Session, transaction: TransactionCreateSchema, user_id: int):

        user = UserService.get_user_by_id(db, user_id=user_id)

        if not user.role.name == RoleEnum.INVESTOR.value:
            raise ResponseHandler.is_not_investor(f" User Id {user.id}")

        operation = OperationService.get_operation_by_id(db, operation_id=transaction.operation_id)

        if operation.status.name != OperationState.COMPLETED.value and not operation.is_closed:
            raise ResponseHandler.bad_request(f"Operation {operation.title} status is not completed")

        if not operation.bids:
            raise ResponseHandler.bad_request(f"Operation {operation.title} has no bids")

        amounts_transactions = [
            calculate_interest(x.amount, operation.annual_interest, operation.time_created, operation.deadline)
            for x in operation.bids
            if x.investor_id == user_id
        ]

        total_capital = sum(x.amount for x in operation.bids if x.investor_id == user_id)
        total_interest = sum(amounts_transactions)
        transaction_amount = total_capital + total_interest

        db_transaction = TransactionEntity.model_validate(
            transaction,
            update={
                "created_by": user.email,
                "amount": transaction_amount,
                "transaction_date": date.today(),
            },
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction


def calculate_interest(amount, interest_rate, creation_date, deadline):
    # Calcular el número de días entre la fecha de creación y el deadline
    days_invested = (deadline - creation_date).days
    
    # Calcular el interés anual
    annual_interest = amount * (interest_rate / 100)
    
    # Calcular el interés proporcional al periodo de inversión
    interest = (annual_interest * Decimal(days_invested) / Decimal(365)).quantize(Decimal('0.01'))
    
    return interest
