# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "CommunityRequestDataParam",
    "Attributes",
    "Relationships",
    "RelationshipsAddress",
    "RelationshipsAddressData",
    "RelationshipsPropertyManager",
    "RelationshipsPropertyManagerData",
    "RelationshipsContactAddress",
    "RelationshipsContactAddressData",
]


class Attributes(TypedDict, total=False):
    name: Required[str]
    """Name of the community to identify it"""

    contact_email_address: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    contact_name: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    contact_phone_number: Optional[str]
    """Displayed to residents for any inquiries or support.

    If left blank, defaults to the property manager's setting.
    """

    external_ref: Optional[str]
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    is_active: bool

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    slug: str
    """URL-friendly name. Only lowercase letters, numbers, and hyphens are allowed."""


class RelationshipsAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAddress(TypedDict, total=False):
    data: Required[RelationshipsAddressData]


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


class RelationshipsContactAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsContactAddress(TypedDict, total=False):
    data: Required[RelationshipsContactAddressData]


class Relationships(TypedDict, total=False):
    address: Required[RelationshipsAddress]
    """The identifier of the related object."""

    property_manager: Required[RelationshipsPropertyManager]
    """The identifier of the related object."""

    contact_address: Optional[RelationshipsContactAddress]
    """The identifier of the related object."""


class CommunityRequestDataParam(TypedDict, total=False):
    attributes: Required[Attributes]

    relationships: Required[Relationships]

    type: Required[Literal["Community"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
