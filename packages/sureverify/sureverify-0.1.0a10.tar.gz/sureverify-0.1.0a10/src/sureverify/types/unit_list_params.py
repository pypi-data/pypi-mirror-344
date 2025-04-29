# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UnitListParams"]


class UnitListParams(TypedDict, total=False):
    fields_unit: Annotated[
        List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ],
        PropertyInfo(alias="fields[Unit]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_community_property_manager_id: Annotated[str, PropertyInfo(alias="filter[community__property_manager_id]")]

    filter_community_id: Annotated[str, PropertyInfo(alias="filter[community_id]")]

    include: List[Literal["community", "address"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
