# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationCaseListParams"]


class VerificationCaseListParams(TypedDict, total=False):
    fields_verification_case: Annotated[
        List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[VerificationCase]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_community_id: Annotated[Optional[str], PropertyInfo(alias="filter[community_id]")]
    """The property or apartment complex where this verification case originated."""

    filter_property_manager_id: Annotated[str, PropertyInfo(alias="filter[property_manager_id]")]
    """The property management company handling this verification."""

    filter_resident_id: Annotated[Optional[str], PropertyInfo(alias="filter[resident_id]")]
    """The resident whose insurance is being verified."""

    include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
