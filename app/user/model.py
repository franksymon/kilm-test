from app.core.db import BaseModel
from pydantic import EmailStr
from sqlmodel import  Field, Column, String, Boolean, Relationship, func, DateTime
from datetime import datetime
from typing import Optional, TYPE_CHECKING

# Models
if TYPE_CHECKING:
    from app.role.model import RoleEntity
    from app.operation.model import OperationEntity
    from app.bid.model import BidEntity

class UserEntity(BaseModel, table=True):
    __tablename__ = "users"
    
    email: EmailStr = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    username: str = Field(sa_column=Column(String, nullable=False, unique=True, index=True))
    full_name: str = Field(sa_column=Column(String, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    role : Optional["RoleEntity"] = Relationship(back_populates="users")
    
    operations: list["OperationEntity"] = Relationship(back_populates="operator", sa_relationship_kwargs={"lazy": "selectin"})
    bids: list["BidEntity"] = Relationship(back_populates="investor", sa_relationship_kwargs={"lazy": "selectin"})

    created_by: str | None = Field(sa_column=Column(String, nullable=False))
    updated_by: str | None = Field(default=None, nullable=True)
    time_created: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, server_default=func.now()))
    time_updated: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, server_default=func.now()))

    def __str__(self):
        return {
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "role": self.role
        }

