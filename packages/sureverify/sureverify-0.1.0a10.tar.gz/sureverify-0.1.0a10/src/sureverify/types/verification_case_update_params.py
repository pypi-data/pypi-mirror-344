# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date, datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "VerificationCaseUpdateParams",
    "Data",
    "DataRelationships",
    "DataRelationshipsPropertyManager",
    "DataRelationshipsPropertyManagerData",
    "DataRelationshipsAttachments",
    "DataRelationshipsAttachmentsData",
    "DataRelationshipsCommunity",
    "DataRelationshipsCommunityData",
    "DataRelationshipsPolicy",
    "DataRelationshipsPolicyData",
    "DataRelationshipsPortal",
    "DataRelationshipsPortalData",
    "DataRelationshipsResident",
    "DataRelationshipsResidentData",
    "DataRelationshipsUnit",
    "DataRelationshipsUnitData",
    "DataAttributes",
]


class VerificationCaseUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataRelationshipsPropertyManagerData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["PropertyManager"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsPropertyManager(TypedDict, total=False):
    data: Required[DataRelationshipsPropertyManagerData]


class DataRelationshipsAttachmentsData(TypedDict, total=False):
    id: Required[str]
    """The identifier of the related object."""

    type: Required[Literal["Attachment"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsAttachments(TypedDict, total=False):
    data: Required[Iterable[DataRelationshipsAttachmentsData]]


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


class DataRelationshipsPolicyData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Policy"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsPolicy(TypedDict, total=False):
    data: Required[DataRelationshipsPolicyData]


class DataRelationshipsPortalData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["VerificationPortal"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsPortal(TypedDict, total=False):
    data: Required[DataRelationshipsPortalData]


class DataRelationshipsResidentData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Resident"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsResident(TypedDict, total=False):
    data: Required[DataRelationshipsResidentData]


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


class DataRelationships(TypedDict, total=False):
    property_manager: Required[DataRelationshipsPropertyManager]
    """The identifier of the related object."""

    attachments: DataRelationshipsAttachments
    """A related resource object from type Attachment"""

    community: Optional[DataRelationshipsCommunity]
    """The identifier of the related object."""

    policy: Optional[DataRelationshipsPolicy]
    """The identifier of the related object."""

    portal: Optional[DataRelationshipsPortal]
    """The identifier of the related object."""

    resident: Optional[DataRelationshipsResident]
    """The identifier of the related object."""

    unit: Optional[DataRelationshipsUnit]
    """The identifier of the related object."""


class DataAttributes(TypedDict, total=False):
    due_at: Annotated[Union[str, date], PropertyInfo(format="iso8601")]
    """The deadline for this verification case to be completed."""

    external_reference: Optional[str]
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    submitted_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """When this verification case was submitted for review."""


class Data(TypedDict, total=False):
    id: Required[str]

    relationships: Required[DataRelationships]

    type: Required[Literal["VerificationCase"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: DataAttributes
