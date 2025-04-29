# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date, datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "VerificationCase",
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


class RelationshipsPropertyManagerData(BaseModel):
    id: str

    type: Literal["PropertyManager"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPropertyManager(BaseModel):
    data: Optional[RelationshipsPropertyManagerData] = None


class RelationshipsAttachmentsData(BaseModel):
    id: str
    """The identifier of the related object."""

    type: Literal["Attachment"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAttachments(BaseModel):
    data: Optional[List[RelationshipsAttachmentsData]] = None


class RelationshipsCommunityData(BaseModel):
    id: str

    type: Literal["Community"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCommunity(BaseModel):
    data: Optional[RelationshipsCommunityData] = None


class RelationshipsPolicyData(BaseModel):
    id: str

    type: Literal["Policy"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPolicy(BaseModel):
    data: Optional[RelationshipsPolicyData] = None


class RelationshipsPortalData(BaseModel):
    id: str

    type: Literal["VerificationPortal"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPortal(BaseModel):
    data: Optional[RelationshipsPortalData] = None


class RelationshipsResidentData(BaseModel):
    id: str

    type: Literal["Resident"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsResident(BaseModel):
    data: Optional[RelationshipsResidentData] = None


class RelationshipsUnitData(BaseModel):
    id: str

    type: Literal["Unit"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsUnit(BaseModel):
    data: Optional[RelationshipsUnitData] = None


class Relationships(BaseModel):
    property_manager: RelationshipsPropertyManager
    """The identifier of the related object."""

    attachments: Optional[RelationshipsAttachments] = None
    """A related resource object from type Attachment"""

    community: Optional[RelationshipsCommunity] = None
    """The identifier of the related object."""

    policy: Optional[RelationshipsPolicy] = None
    """The identifier of the related object."""

    portal: Optional[RelationshipsPortal] = None
    """The identifier of the related object."""

    resident: Optional[RelationshipsResident] = None
    """The identifier of the related object."""

    unit: Optional[RelationshipsUnit] = None
    """The identifier of the related object."""


class Attributes(BaseModel):
    created_at: Optional[datetime] = None

    decision: Optional[Literal["compliant", "non_compliant"]] = None
    """
    - `compliant` - Compliant
    - `non_compliant` - Non-Compliant
    """

    decision_reason: Optional[str] = None

    due_at: Optional[date] = None
    """The deadline for this verification case to be completed."""

    external_reference: Optional[str] = None
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    notes: Optional[str] = None
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    receipt_reference: Optional[str] = None

    source: Optional[Literal["PORTAL", "MAIL", "EMAIL", "PURCHASE_FLOW", "API"]] = None
    """
    - `PORTAL` - Portal
    - `MAIL` - Mail
    - `EMAIL` - Email
    - `PURCHASE_FLOW` - Purchase Flow
    - `API` - Api
    """

    status: Optional[
        Literal[
            "draft", "new", "enqueued", "in_progress", "further_review_required", "completed", "failed", "cancelled"
        ]
    ] = None
    """
    - `draft` - Draft
    - `new` - New
    - `enqueued` - Enqueued
    - `in_progress` - In Progress
    - `further_review_required` - Further Review Required
    - `completed` - Completed
    - `failed` - Failed
    - `cancelled` - Cancelled
    """

    submitted_at: Optional[datetime] = None
    """When this verification case was submitted for review."""

    updated_at: Optional[datetime] = None


class VerificationCase(BaseModel):
    id: str

    relationships: Relationships

    type: Literal["VerificationCase"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Optional[Attributes] = None
