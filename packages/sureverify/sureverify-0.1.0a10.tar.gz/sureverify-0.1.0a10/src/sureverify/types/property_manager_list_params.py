# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PropertyManagerListParams"]


class PropertyManagerListParams(TypedDict, total=False):
    fields_property_manager: Annotated[
        List[
            Literal[
                "name",
                "slug",
                "is_active",
                "notes",
                "interest_email_address",
                "interest_name",
                "interest_mailbox",
                "contact_name",
                "contact_email_address",
                "contact_address",
                "contact_phone_number",
                "admin_review_required",
                "admin_review_required_only_for_non_compliant",
                "allow_overriding",
                "force_admin_review_if_overridden",
                "allow_partial_name_and_unit_match",
                "allow_new_units",
                "allow_new_residents",
                "allow_new_policies_from_carriers",
                "allow_invalid_address",
                "force_coverage_term_to_overlap_with_lease",
                "force_extra_confirmation_on_verification_submission",
                "send_email_when_no_verification_started",
                "send_email_when_case_incomplete",
                "send_email_when_case_submitted",
                "send_email_when_case_compliant",
                "send_email_when_case_non_compliant",
                "send_email_when_compliance_is_expiring_soon",
                "send_email_when_becoming_non_compliant",
                "send_email_when_new_policy_is_added",
                "send_email_when_policy_updated",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[PropertyManager]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["interest_mailbox", "contact_address"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """

    page_cursor: Annotated[str, PropertyInfo(alias="page[cursor]")]
    """The pagination cursor value."""

    page_size: Annotated[int, PropertyInfo(alias="page[size]")]
    """Number of results to return per page."""
