from sqlmodel import Field, Relationship, Column, String
from sqlalchemy import Text, Numeric
from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.core.db import BaseModel
from app.user.model import UserEntity
#from app.bid.model import BidEntity 


class OperationEntity(BaseModel, table=True):
    __tablename__ = "operations"
    
    amount_required: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    title: str = Field(nullable=False, max_length=255)
    description: str = Field(sa_column=Column(Text, nullable=False))
    annual_interest: Decimal = Field(sa_column=Column(Numeric(3, 2), nullable=False))
    deadline: Optional[datetime] = Field(nullable=True)
    is_closed: bool = Field(default=False)
    operator_id: int = Field(foreign_key="users.id")
    status_id: int = Field(foreign_key="operations_status.id")

    operator: UserEntity = Relationship(back_populates="operations")
    status: lambda: OperationStatus = Relationship(back_populates="operations")
    #bids: list["BidEntity"] = Relationship(back_populates="operations")
    #transactions: list["TransactionEntity"] = Relationship(back_populates="operations")

    created_by: str = Field(sa_column=Column(String, nullable=False))
    updated_by: Optional[str] = Field(default=None, nullable=True)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated:  Optional[datetime] = Field(default=None, nullable=True)

class OperationStatus(BaseModel, table=True):
    __tablename__ = "operations_status"
    
    name: str = Field(nullable=False, max_length=255, unique=True, index=True)
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))

    operations: list["OperationEntity"] = Relationship(back_populates="status")

    created_by: str = Field(sa_column=Column(String, nullable=False))
    updated_by: Optional[str] = Field(default=None, nullable=True)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated: Optional[datetime] = Field(default=None, nullable=True)
