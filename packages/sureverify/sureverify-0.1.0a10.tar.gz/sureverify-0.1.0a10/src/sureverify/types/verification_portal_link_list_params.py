# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationPortalLinkListParams"]


class VerificationPortalLinkListParams(TypedDict, total=False):
    fields_verification_portal_link: Annotated[
        List[Literal["portal", "title", "url", "weight", "location"]],
        PropertyInfo(alias="fields[VerificationPortalLink]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_portal_property_manager_id: Annotated[str, PropertyInfo(alias="filter[portal__property_manager_id]")]

    filter_portal_id: Annotated[str, PropertyInfo(alias="filter[portal_id]")]

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
