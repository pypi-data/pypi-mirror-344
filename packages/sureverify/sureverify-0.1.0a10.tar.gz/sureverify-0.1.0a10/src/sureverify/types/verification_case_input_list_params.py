# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationCaseInputListParams"]


class VerificationCaseInputListParams(TypedDict, total=False):
    fields_verification_case_input: Annotated[
        List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[VerificationCaseInput]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_case_community_id: Annotated[Optional[str], PropertyInfo(alias="filter[case__community_id]")]
    """The property or apartment complex where this verification case originated."""

    filter_case_property_manager_id: Annotated[str, PropertyInfo(alias="filter[case__property_manager_id]")]
    """The property management company handling this verification."""

    filter_case_id: Annotated[str, PropertyInfo(alias="filter[case_id]")]

    include: List[Literal["address", "case"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
