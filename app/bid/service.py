from sqlmodel import Session, select, func
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params

from app.user.service import get_user_by_id
from app.operation.service import get_operation_by_id

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
    
    investor = get_user_by_id(db=db, user_id=bid.investor_id)
    
    if investor.role.name in [RoleEnum.OPERATOR.value, RoleEnum.ADMIN.value]:
        raise ResponseHandler.is_not_investor("User", investor.username)
    
    operation = get_operation_by_id(db=db, bid_id=bid.operation_id)
    
    db_bid = BidEntity.model_validate(bid, update={"created_by": investor.email})
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

def update_bid(db: Session, bid_id: int, bid: BidCreateSchema):
    
    investor = get_user_by_id(db=db, user_id=bid.investor_id)
    
    if investor.role.name in [RoleEnum.OPERATOR.value, RoleEnum.ADMIN.value]:
        raise ResponseHandler.is_not_investor("User", investor.username)
    
    operation = get_operation_by_id(db=db, bid_id=bid.operation_id)
    
    db_bid = get_bid_by_id(db=db, bid_id=bid_id)
    
    if bid.amount: 
        db_bid.amount = bid.amount

    if bid.interest_rate:    
        db_bid.interest_rate = bid.interest_rate

    db_bid.updated_by = investor.email
    db_bid.time_updated = func.now()
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

def delete_bid(db: Session, bid_id: int):
    
    db_bid = get_bid_by_id(db=db, bid_id=bid_id)
    db.delete(db_bid)
    db.commit()
    return ResponseHandler.delete_success("Bid", bid_id, db_bid)