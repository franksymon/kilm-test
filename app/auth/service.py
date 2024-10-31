from sqlmodel import Session



# Models
from app.user.model import UserEntity

# Services
from app.user.service import get_user_by_email, get_user_by_username
from app.core.security import verify_password





def authenticate(db: Session, username: str, password: str) -> UserEntity | None:
    db_user = get_user_by_username(db=db, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user