# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Community",
    "Attributes",
    "Relationships",
    "RelationshipsAddress",
    "RelationshipsAddressData",
    "RelationshipsPropertyManager",
    "RelationshipsPropertyManagerData",
    "RelationshipsContactAddress",
    "RelationshipsContactAddressData",
]


class Attributes(BaseModel):
    name: str
    """Name of the community to identify it"""

    contact_email_address: Optional[str] = None
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    contact_name: Optional[str] = None
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    contact_phone_number: Optional[str] = None
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    created_at: Optional[datetime] = None

    external_ref: Optional[str] = None
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    is_active: Optional[bool] = None

    notes: Optional[str] = None
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    slug: Optional[str] = None
    """URL-friendly name. Only lowercase letters, numbers, and hyphens are allowed."""

    updated_at: Optional[datetime] = None


class RelationshipsAddressData(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAddress(BaseModel):
    data: Optional[RelationshipsAddressData] = None


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


class RelationshipsContactAddressData(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsContactAddress(BaseModel):
    data: Optional[RelationshipsContactAddressData] = None


class Relationships(BaseModel):
    address: RelationshipsAddress
    """The identifier of the related object."""

    property_manager: RelationshipsPropertyManager
    """The identifier of the related object."""

    contact_address: Optional[RelationshipsContactAddress] = None
    """The identifier of the related object."""


class Community(BaseModel):
    id: str

    attributes: Attributes

    relationships: Relationships

    type: Literal["Community"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
