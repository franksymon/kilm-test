from sqlmodel import Field, SQLModel


class TokenSchema(SQLModel):

    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: int
    exp: int
    email: str
    role: str

class NewPassword(SQLModel):

    token: str
    new_password: str