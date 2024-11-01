from sqlmodel import SQLModel
from datetime import datetime, date
from typing import Optional
from app.operation.schema import OperationTransactionSchema
from app.user.schema import TransactionUserSchema


class TransactionBaseSchema(SQLModel):
    amount: float
    transaction_date: date
    description: str

class TransactionSchema(TransactionBaseSchema):
    id: int
    ...


class TransactionCreateSchema(SQLModel):
    operation_id: int
    description: str | None = None


class TransactionUpdateSchema(SQLModel):
    amount: float | None = None
    transaction_date: datetime | None = None
    description: str | None = None
    operation_id: int 


class TransactionByUserSchema(TransactionBaseSchema):
    id: int
    #operation: Optional[OperationTransactionSchema]

    class Config:
        orm_mode = True

class TransactionByOperationSchema(TransactionBaseSchema):
    id: int
    