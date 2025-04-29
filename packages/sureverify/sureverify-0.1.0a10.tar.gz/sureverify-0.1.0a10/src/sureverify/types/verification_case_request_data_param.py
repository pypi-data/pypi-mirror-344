# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date, datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "VerificationCaseRequestDataParam",
    "Relationships",
    "RelationshipsPropertyManager",
    "RelationshipsPropertyManagerData",
    "RelationshipsAttachments",
    "RelationshipsAttachmentsData",
    "RelationshipsCommunity",
    "RelationshipsCommunityData",
    "RelationshipsPolicy",
    "RelationshipsPolicyData",
    "RelationshipsPortal",
    "RelationshipsPortalData",
    "RelationshipsResident",
    "RelationshipsResidentData",
    "RelationshipsUnit",
    "RelationshipsUnitData",
    "Attributes",
]


class RelationshipsPropertyManagerData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["PropertyManager"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPropertyManager(TypedDict, total=False):
    data: Required[RelationshipsPropertyManagerData]


class RelationshipsAttachmentsData(TypedDict, total=False):
    id: Required[str]
    """The identifier of the related object."""

    type: Required[Literal["Attachment"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAttachments(TypedDict, total=False):
    data: Required[Iterable[RelationshipsAttachmentsData]]


class RelationshipsCommunityData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Community"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCommunity(TypedDict, total=False):
    data: Required[RelationshipsCommunityData]


class RelationshipsPolicyData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Policy"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPolicy(TypedDict, total=False):
    data: Required[RelationshipsPolicyData]


class RelationshipsPortalData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["VerificationPortal"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPortal(TypedDict, total=False):
    data: Required[RelationshipsPortalData]


class RelationshipsResidentData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Resident"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsResident(TypedDict, total=False):
    data: Required[RelationshipsResidentData]


class RelationshipsUnitData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Unit"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsUnit(TypedDict, total=False):
    data: Required[RelationshipsUnitData]


class Relationships(TypedDict, total=False):
    property_manager: Required[RelationshipsPropertyManager]
    """The identifier of the related object."""

    attachments: RelationshipsAttachments
    """A related resource object from type Attachment"""

    community: Optional[RelationshipsCommunity]
    """The identifier of the related object."""

    policy: Optional[RelationshipsPolicy]
    """The identifier of the related object."""

    portal: Optional[RelationshipsPortal]
    """The identifier of the related object."""

    resident: Optional[RelationshipsResident]
    """The identifier of the related object."""

    unit: Optional[RelationshipsUnit]
    """The identifier of the related object."""


class Attributes(TypedDict, total=False):
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


class VerificationCaseRequestDataParam(TypedDict, total=False):
    relationships: Required[Relationships]

    type: Required[Literal["VerificationCase"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Attributes
