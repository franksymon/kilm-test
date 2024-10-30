from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import field_validator

class RoleBaseSchema(SQLModel):
    id: int
    name: str
    is_active: bool
    #created_by: str | None
    #updated_by: str | None
    #time_created: datetime | None
    #time_updated: datetime | None


class RoleCreateSchema(SQLModel):
    name: str = Field(min_length=1, max_length=255)

    @field_validator('name', mode='before')
    def set_name_uppercase(cls, v):
        return v.upper() if v else v


class RoleUpdateSchema(SQLModel):
    id: int
    is_active: bool


class RolePublicSchema(RoleBaseSchema):
    ...





