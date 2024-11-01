from sqlmodel import  Field, Column, String, Relationship
from datetime import datetime
from sqlalchemy import  Numeric, Text
from typing import Optional
from decimal import Decimal

from app.core.db import BaseModel
from app.operation.model import OperationEntity


class TransactionEntity(BaseModel, table=True):
    __tablename__ = "transactions"

    amount: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    transaction_date: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(sa_column=Column(Text, nullable=False))
    
    operations: OperationEntity = Relationship(back_populates="transactions")
    operation_id: int = Field(foreign_key="operations.id")

    created_by: str = Field(sa_column=Column(String, nullable=False))
    updated_by: Optional[str] = Field(default=None, nullable=True)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated:  Optional[datetime] = Field(default=None, nullable=True)