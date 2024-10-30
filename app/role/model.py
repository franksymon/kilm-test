from app.core.db import BaseModel
from sqlmodel import  Field, Relationship, func, Column, String, DateTime
from datetime import datetime
from typing import Optional

class RoleEntity(BaseModel, table=True):
    __tablename__ = "roles"
    
    name : str = Field(nullable=False, index=True, unique=True)
    is_active : bool = Field(nullable=False, default=True)
    users : list["UserEntity"] = Relationship(back_populates="role")
    
    created_by: str | None = Field(sa_column=Column(String, nullable=False))
    updated_by: str | None = Field(default=None, nullable=True)
    time_created: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, server_default=func.now()))
    time_updated:  Optional[datetime] = Field(default=None, nullable=True)

    def __str__(self):
        return {
            "name": self.name,
            "is_active": self.is_active
        }
