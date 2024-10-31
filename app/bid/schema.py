from sqlmodel import Field, SQLModel
from datetime import datetime, date
from typing import Optional

from app.user.schema import InvestorSchema
from app.operation.schema import OperationBidSchema

class BidBaseSchema(SQLModel):
    id: int
    amount: float
    interest_rate: float
    investor : Optional[InvestorSchema]
    #operations: Optional[OperationBidSchema]


class GetBidByUserSchema(SQLModel):
    id: int
    amount: float
    interest_rate: float
    operations: Optional[OperationBidSchema]

class BidCreateSchema(SQLModel):
    amount: float
    interest_rate: float
    investor_id: int
    operation_id: int
   
class BidUpdateSchema(BidCreateSchema):
    id: int