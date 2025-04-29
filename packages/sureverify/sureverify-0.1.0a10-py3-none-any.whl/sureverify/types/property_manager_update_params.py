# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "PropertyManagerUpdateParams",
    "Data",
    "DataAttributes",
    "DataRelationships",
    "DataRelationshipsContactAddress",
    "DataRelationshipsContactAddressData",
]


class PropertyManagerUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
    name: Required[str]

    admin_review_required: bool
    """
    When enabled, all verification submissions will be placed in a queue for admin
    review before being approved or rejected. When disabled, verifications will be
    processed automatically based on the AI analysis results, unless other admin
    reviews settings are enabled.
    """

    admin_review_required_only_for_non_compliant: bool
    """
    When enabled, only non-compliant verifications will be placed in a queue for
    admin review before being approved or rejected. When disabled, verifications
    will be processed automatically based on the AI analysis results, unless other
    admin reviews settings are enabled.
    """

    allow_invalid_address: bool
    """
    When enabled, the system will accept addresses that cannot be validated against
    the USPS national address database. When disabled, only USPS verified,
    standardized addresses will be accepted.
    """

    allow_new_policies_from_carriers: bool
    """
    When enabled, the system will accept new policies from carriers that are not
    already in the system. When disabled, only policies that are already in the
    system will be accepted.
    """

    allow_new_residents: bool
    """
    When enabled, the system will create new residents for verification submissions
    that do not match any existing residents in the system. When disabled, only
    existing residents will be accepted.
    """

    allow_new_units: bool
    """
    When enabled, the system will create new units for verification submissions that
    do not match any existing units in the system. When disabled, only existing
    units will be accepted.
    """

    allow_overriding: bool
    """
    When enabled, submitters can update or modify existing unit/resident information
    during the verification process. When disabled, existing details about the unit
    or the resident cannot be changed. This is also applicable if a resident is
    trying to verify a unit with a different name or email
    """

    allow_partial_name_and_unit_match: bool
    """
    When enabled, the system will accept verification submissions that only
    partially match the unit or resident details in the system. When disabled, only
    exact matches will be accepted.
    """

    contact_email_address: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, no information will show, unless the community records has this
    information set.
    """

    contact_name: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, no information will show, unless the community records has this
    information set.
    """

    contact_phone_number: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, no information will show, unless the community records has this
    information set.
    """

    force_admin_review_if_overridden: bool
    """
    When enabled, any verification submission that has been overridden will be
    automatically placed in a queue for admin review. This is useful when you want
    to ensure that any changes made by the resident are reviewed before the
    verification is approved.
    """

    force_coverage_term_to_overlap_with_lease: bool
    """
    When enabled, the system will require the coverage term of the policy to overlap
    with the lease term of the resident. This is useful when you want to ensure that
    the resident has coverage for the entire duration of their lease. This only
    applies to new policies bought in the purchase flow. Otherwise refer to the
    requirements settings.
    """

    force_extra_confirmation_on_verification_submission: bool
    """
    When enabled, the system will require the resident to confirm the address of the
    interested party by entering the suite/unit number, and not just with a
    checkbox.
    """

    interest_name: Optional[str]
    """The resident will be required to put this name on their policy."""

    is_active: bool

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    send_email_when_becoming_non_compliant: bool
    """
    Send notifications to residents when we detect their insurance has become
    non-compliant based on carrier policy updates.
    """

    send_email_when_case_compliant: bool
    """Send notifications when verification documents are approved.

    Includes confirmation of compliance status and next review date.
    """

    send_email_when_case_incomplete: bool
    """
    Automatically send follow-up reminders to residents who started but haven't
    completed their verification submission. Helps reduce application abandonment
    rates.
    """

    send_email_when_case_non_compliant: bool
    """Send detailed notifications when verification documents are rejected.

    Includes specific reasons for non-compliance and instructions for resubmission.
    """

    send_email_when_case_submitted: bool
    """
    Send automatic confirmation emails to residents immediately after they submit
    verification documents through the portal. Includes submission reference number
    and estimated processing time.
    """

    send_email_when_compliance_is_expiring_soon: bool
    """Send advance notifications before a resident's compliance status expires.

    Includes instructions for maintaining compliance.
    """

    send_email_when_new_policy_is_added: bool
    """
    Send notifications to residents when their existing policy renews and remains
    compliant. These notifications are based on any updates we receive from the
    carrier.
    """

    send_email_when_no_verification_started: bool
    """
    Automatically send follow-up reminders to residents who haven't started a
    verification. Helps improve application completion rates.
    """

    send_email_when_policy_updated: bool
    """
    Send notifications to residents when their existing policy changes, excluding
    renewals, and remains compliant. These notifications are based on any updates we
    receive from the carrier.
    """


class DataRelationshipsContactAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsContactAddress(TypedDict, total=False):
    data: Required[DataRelationshipsContactAddressData]


class DataRelationships(TypedDict, total=False):
    contact_address: Optional[DataRelationshipsContactAddress]
    """The identifier of the related object."""


class Data(TypedDict, total=False):
    id: Required[str]

    attributes: Required[DataAttributes]

    type: Required[Literal["PropertyManager"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: DataRelationships
