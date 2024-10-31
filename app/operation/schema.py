from sqlmodel import Field, SQLModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from pydantic import field_validator
from app.user.schema import OperatorSchema

class StateOperationBaseSchema(SQLModel):
    id: int
    name: str
    description: Optional[str]

class OperationBaseSchema(SQLModel):
    id: int
    amount_required: float
    title: str
    description: str
    annual_interest: float
    deadline: Optional[datetime]
    is_closed: bool
    
    operator: Optional["OperatorSchema"]
    status: Optional[StateOperationBaseSchema]

class UpdateOperationSchema(SQLModel):
    id: int
    amount_required: float | None = None
    title: str | None = None
    description: str | None = None
    annual_interest: float | None = None
    deadline: Optional[date] | None = None
    is_closed: bool | None = None

class OperationCreateSchema(SQLModel):
    amount_required: float
    title: str
    description: str
    annual_interest: float
    deadline: Optional[date]
    is_closed: bool = Field(default=False)
    operator_id: int
    status_id: int

class OperationBidSchema(SQLModel):
    id: int
    amount_required: float
    title: str
    description: str
    annual_interest: float
    deadline: Optional[datetime]
    is_closed: bool  
    
    status: Optional[StateOperationBaseSchema]


# State Operation

class StateOperationCreateSchema(SQLModel):
    name: str
    description: Optional[str]

    @field_validator('name', mode='before')
    def set_name_uppercase(cls, v):
        return v.upper() if v else v
    
class StateOperationUpdateSchema(StateOperationCreateSchema):
    id: int

