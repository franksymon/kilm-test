import secrets

from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   
    PROJECT_NAME: str = "Prueba Tecnica FastAPI - Klimb"
    API_V1_STR: str = "/api/v1"
    ALGORITHM : str = "HS256"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


    
    SQLITE_DB: str = "sqlite:///./database.db"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.SQLITE_DB


settings = Settings()