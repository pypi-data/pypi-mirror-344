# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

import httpx

from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["CursorPaginationLinks", "SyncCursorPagination", "AsyncCursorPagination"]

_T = TypeVar("_T")


class CursorPaginationLinks(BaseModel):
    next: Optional[str] = None


class SyncCursorPagination(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    links: Optional[CursorPaginationLinks] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = None
        if self.links is not None:
            if self.links.next is not None:
                url = self.links.next
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))


class AsyncCursorPagination(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    links: Optional[CursorPaginationLinks] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = None
        if self.links is not None:
            if self.links.next is not None:
                url = self.links.next
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))
