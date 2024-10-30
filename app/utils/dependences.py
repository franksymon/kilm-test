from typing import TypeVar
from fastapi import Query
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.customization import CustomizedPage, UseParamsFields


T = TypeVar("T")


CustomPagePagination = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(5, ge=1, le=100),
        page=Query(1, ge=1),
    ),
]
