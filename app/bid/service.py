from sqlmodel import Session, select, func
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params

# Config
from app.core.security import verify_password, hash_password

# Utils
from app.utils.responses import ResponseHandler
from app.utils.enum_role import RoleEnum

# Schemas
from app.bid.schema import BidCreateSchema, BidBaseSchema

# Models
from app.user.model import UserEntity
from app.bid.model import BidEntity



def get_all_bids_by_user_investor(db: Session, user_id: int, params: Params):

    user = db.get(UserEntity, user_id)
    if not user:
        raise ResponseHandler.not_found_error("User", user_id)
    
    if not user.is_active:
        raise ResponseHandler.is_not_active(f" User {user.username}")
    
    if not user.role.name == RoleEnum.INVESTOR.value:
        raise ResponseHandler.is_not_investor(f" User {user.username}")

    query = select(BidEntity).where(BidEntity.investor_id == user_id)
    return paginate(db, query, params)


def get_all_bids(db: Session, params: Params):
    query = select(BidEntity)
    return paginate(db, query, params)

def get_bid_by_id(db: Session, bid_id: int):
    bid = db.get(BidEntity, bid_id)
    if not bid:
        raise ResponseHandler.not_found_error("Bid", bid_id)
    return bid

def get_bids_by_operation(db: Session, operation_id: int):
    query = select(BidEntity).where(BidEntity.operation_id == operation_id)
    return paginate(db, query)

def create_bid(db: Session, bid: BidCreateSchema):
    ...

def update_bid(db: Session, bid_id: int, bid: BidCreateSchema):
    ...

def delete_bid(db: Session, bid_id: int):
    ...