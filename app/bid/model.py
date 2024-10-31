from sqlmodel import  Field, Column, String, Relationship
from datetime import datetime
from sqlalchemy import  Numeric
from typing import Optional
from decimal import Decimal

from app.core.db import BaseModel
from app.user.model import UserEntity
from app.operation.model import OperationEntity


class BidEntity(BaseModel, table=True):
    __tablename__ = "bids"
   
    amount: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    interest_rate: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    
    investor_id: int = Field(foreign_key="users.id")
    operation_id: int = Field(foreign_key="operations.id")

    investor: UserEntity = Relationship(back_populates="bids")
    operations: OperationEntity = Relationship(back_populates="bids")

    created_by: str = Field(sa_column=Column(String, nullable=False))
    updated_by: Optional[str] = Field(default=None, nullable=True)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated:  Optional[datetime] = Field(default=None, nullable=True)


