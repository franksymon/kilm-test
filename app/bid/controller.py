from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi_pagination import Params


# Config
from app.core.security import SessionDep, get_current_active_user

# Utils
from app.utils.dependences import CustomPagePagination as Page



router = APIRouter(tags=["bids"], prefix="/bids")

@router.get("/all/user/{user_id}", response_model=Page[BidBaseSchema])
def get_all_bids_by_user_controller(db: SessionDep, params: Params = Depends()):
    ...

    