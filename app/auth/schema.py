from sqlmodel import Field, SQLModel


class Token(SQLModel):

    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str
    exp: int

class NewPassword(SQLModel):

    token: str
    new_password: str