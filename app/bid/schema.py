from sqlmodel import Field, SQLModel
from datetime import datetime, date
from typing import Optional

from app.user.schema import InvestorSchema
from app.operation.schema import OperationSchema

class BidBaseSchema(SQLModel):
    amount: float
    interest_rate: float
    investor : Optional[InvestorSchema]
    operation: str
   