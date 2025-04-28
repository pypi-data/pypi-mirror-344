# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["Meta", "Pagination"]


class Pagination(BaseModel):
    count: Optional[int] = None

    next_page: Optional[int] = FieldInfo(alias="nextPage", default=None)

    page_number: Optional[int] = FieldInfo(alias="pageNumber", default=None)

    page_size: Optional[int] = FieldInfo(alias="pageSize", default=None)

    total_pages: Optional[int] = FieldInfo(alias="totalPages", default=None)


class Meta(BaseModel):
    pagination: Optional[Pagination] = None
