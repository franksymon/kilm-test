from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page

# Schemas
from app.bid.schema import BidCreateSchema, BidBaseSchema

# Services
from app.bid.service import (
    get_all_bids_by_user_investor,
    get_all_bids,
    get_bids_by_operation,
    get_bid_by_id,
    create_bid,
    update_bid,
    delete_bid,
)


router = APIRouter(tags=["bids"], prefix="/bids")


@router.get("/all/user/{user_id}", response_model=Page[BidBaseSchema])
def get_all_bids_by_user_investor_controller(
    db: SessionDep,
    user_id: int,
    params: Params = Depends(),
):
    return get_all_bids_by_user_investor(db=db, params=params, user_id=user_id)


@router.get("/all", response_model=Page[BidBaseSchema])
def get_all_bids_controller(db: SessionDep, params: Params = Depends()):
    return get_all_bids(db=db, params=params)


@router.get("/operation/{operation_id}", response_model=Page[BidBaseSchema])
def get_bids_by_operation_controller(db: SessionDep, operation_id: int, params: Params = Depends()):
    return get_bids_by_operation(db=db, params=params, operation_id=operation_id)


@router.get("/{id}", response_model=BidBaseSchema)
def get_bid_by_id_controller(db: SessionDep, id: int):
    return get_bid_by_id(db=db, bid_id=id)


@router.post("", response_model=BidBaseSchema)
def create_bid_controller(db: SessionDep, bid: BidCreateSchema,):
    return create_bid(db=db, bid=bid)


@router.put("/{id}", response_model=BidBaseSchema)
def update_bid_controller(db: SessionDep, id: int, bid: BidCreateSchema):
    return update_bid(db=db, bid_id=id, bid=bid)


@router.delete("/{id}")
def delete_bid_controller(db: SessionDep, id: int):
    return delete_bid(db=db, bid_id=id)
