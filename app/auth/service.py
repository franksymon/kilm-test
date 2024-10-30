from sqlmodel import Session



# Models
from app.user.model import UserEntity

# Services
from app.user.service import get_user_by_email
from app.core.security import verify_password





def authenticate(db: Session, email: str, password: str) -> UserEntity | None:
    db_user = get_user_by_email(db=db, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user