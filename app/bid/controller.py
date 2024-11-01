from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, CurrentUser, RoleChecker

# Utils
from app.utils.dependences import CustomPagePagination as Page
from app.utils.enum.enum_role import RoleEnum

# Schemas
from app.bid.schema import BidCreateSchema, BidBaseSchema, GetBidByUserSchema, BidUpdateSchema

# Services
import app.bid.service as BidService

role_checker = Depends(RoleChecker(allowed_roles=[RoleEnum.ADMIN.value, RoleEnum.INVESTOR.value]))
router = APIRouter(tags=["bids"], prefix="/bids", dependencies=[role_checker])


@router.get("/all/by_user/{user_id}", response_model=Page[GetBidByUserSchema])
def get_all_bids_by_user_investor_controller(
    db: SessionDep,
    user_id: int,
    params: Params = Depends(),
):
    return BidService.get_all_bids_by_user_investor(db=db, params=params, user_id=user_id)


@router.get("/all", response_model=Page[BidBaseSchema])
def get_all_bids_controller(db: SessionDep, params: Params = Depends()):
    return BidService.get_all_bids(db=db, params=params)


@router.get("/by_operation/{operation_id}/details", response_model=Page[BidBaseSchema])
def get_bids_by_operation_controller(db: SessionDep, operation_id: int, params: Params = Depends()):
    return BidService.get_bids_by_operation(db=db, params=params, operation_id=operation_id)


@router.get("/{bid_id}", response_model=BidBaseSchema)
def get_bid_by_id_controller(db: SessionDep, bid_id: int):
    return BidService.get_bid_by_id(db=db, bid_id=bid_id)


@router.post("", response_model=BidBaseSchema)
def create_bid_controller(db: SessionDep, bid: BidCreateSchema,):
    return BidService.create_bid(db=db, bid=bid)


@router.put("", response_model=BidUpdateSchema)
def update_bid_controller(db: SessionDep, bid: BidCreateSchema):
    return BidService.update_bid(db=db, bid=bid)


@router.delete("/{bid_id}", response_model=BidBaseSchema)
def delete_bid_controller(db: SessionDep, bid_id: int):
    return BidService.delete_bid(db=db, bid_id=bid_id)
