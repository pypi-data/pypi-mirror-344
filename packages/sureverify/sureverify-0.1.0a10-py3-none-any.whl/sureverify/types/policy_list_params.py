# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PolicyListParams"]


class PolicyListParams(TypedDict, total=False):
    fields_policy: Annotated[
        List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[Policy]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    filter_resident_community_property_manager_id: Annotated[
        str, PropertyInfo(alias="filter[resident__community__property_manager_id]")
    ]

    filter_resident_community_id: Annotated[str, PropertyInfo(alias="filter[resident__community_id]")]
    """The property or apartment complex where the resident lives."""

    filter_resident_id: Annotated[str, PropertyInfo(alias="filter[resident_id]")]

    include: List[Literal["lease_address", "interested_party_address", "resident"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
