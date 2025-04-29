# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ResidentListParams"]


class ResidentListParams(TypedDict, total=False):
    fields_resident: Annotated[
        List[
            Literal[
                "community",
                "unit",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "lease_start_date",
                "lease_end_date",
                "in_compliance_since",
                "out_of_compliance_since",
                "last_notified_at",
                "notes",
                "external_ref",
                "current_policy",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[Resident]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_community_property_manager_id: Annotated[str, PropertyInfo(alias="filter[community__property_manager_id]")]

    filter_community_id: Annotated[str, PropertyInfo(alias="filter[community_id]")]
    """The property or apartment complex where the resident lives."""

    filter_unit_id: Annotated[str, PropertyInfo(alias="filter[unit_id]")]
    """The specific apartment or unit number assigned to this resident."""

    include: List[Literal["community", "unit"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
