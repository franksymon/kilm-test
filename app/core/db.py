# One line of FastAPI imports here later 👈
from sqlmodel import Field, Session, SQLModel, create_engine
from collections.abc import Generator
from config.config import settings


class BaseModel(SQLModel):
    id: int | None = Field(primary_key=True, index=True, default=None)
    



engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
