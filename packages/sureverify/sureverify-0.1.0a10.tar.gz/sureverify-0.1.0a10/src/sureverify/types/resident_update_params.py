# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date, datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ResidentUpdateParams",
    "Data",
    "DataAttributes",
    "DataRelationships",
    "DataRelationshipsCommunity",
    "DataRelationshipsCommunityData",
    "DataRelationshipsUnit",
    "DataRelationshipsUnitData",
    "DataRelationshipsCurrentPolicy",
    "DataRelationshipsCurrentPolicyData",
]


class ResidentUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
    first_name: Required[str]
    """The resident's legal first name or given name."""

    last_name: Required[str]
    """The resident's legal last name or family name."""

    email: Optional[str]
    """
    Primary email address used for sending notifications and communications to the
    resident.
    """

    external_ref: Optional[str]
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    in_compliance_since: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when the resident's insurance coverage first met all requirements."""

    last_notified_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """The most recent date and time when any notification was sent to this resident."""

    lease_end_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when the resident's lease agreement expires."""

    lease_start_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when the resident's lease agreement begins."""

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    out_of_compliance_since: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when the resident's insurance coverage stopped meeting requirements."""

    phone_number: Optional[str]
    """Primary contact number for reaching the resident."""


class DataRelationshipsCommunityData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Community"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsCommunity(TypedDict, total=False):
    data: Required[DataRelationshipsCommunityData]


class DataRelationshipsUnitData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Unit"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsUnit(TypedDict, total=False):
    data: Required[DataRelationshipsUnitData]


class DataRelationshipsCurrentPolicyData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Policy"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsCurrentPolicy(TypedDict, total=False):
    data: Required[DataRelationshipsCurrentPolicyData]


class DataRelationships(TypedDict, total=False):
    community: Required[DataRelationshipsCommunity]
    """The identifier of the related object."""

    unit: Required[DataRelationshipsUnit]
    """The identifier of the related object."""

    current_policy: Optional[DataRelationshipsCurrentPolicy]
    """The identifier of the related object."""


class Data(TypedDict, total=False):
    id: Required[str]

    attributes: Required[DataAttributes]

    relationships: Required[DataRelationships]

    type: Required[Literal["Resident"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
