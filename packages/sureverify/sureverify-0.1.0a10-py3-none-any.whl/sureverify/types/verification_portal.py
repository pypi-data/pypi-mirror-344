# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "VerificationPortal",
    "Relationships",
    "RelationshipsPropertyManager",
    "RelationshipsPropertyManagerData",
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


class Relationships(BaseModel):
    property_manager: RelationshipsPropertyManager
    """The identifier of the related object."""


class Attributes(BaseModel):
    logo: Optional[str] = None
    """
    Your company or property logo that will be displayed next to the title to
    residents on the portal.
    """

    muted_color: Optional[str] = None
    """
    Using the primary brand color as a base, but a bit lighter for background
    colors.
    """

    only_docs_form: Optional[bool] = None
    """
    If enabled, the user will only be able to upload documents and skip the policy
    data input.
    """

    primary_color: Optional[str] = None
    """
    The main brand color used throughout the portal interface, specified in
    hexadecimal format (e.g. #4F46E5).
    """

    secondary_color: Optional[str] = None
    """Using the primary brand color as a base, but a bit lighter for highlights."""

    show_purchase_flow: Optional[bool] = None
    """
    If enabled, the user will be able to purchase renters insurance through the
    portal, as long as there is a Sure Connect partner account configured.
    """

    slug: Optional[str] = None
    """A unique, URL-friendly name that will be part of the link to the portal.

    Only lowercase letters, numbers, and hyphens are allowed.
    """

    title: Optional[str] = None
    """The name displayed at the top of the portal.

    If you want no title, leave this field blank and select a logo. If no title and
    no logo are provided, then the property manager name will be used.
    """


class VerificationPortal(BaseModel):
    id: str

    relationships: Relationships

    type: Literal["VerificationPortal"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Optional[Attributes] = None
