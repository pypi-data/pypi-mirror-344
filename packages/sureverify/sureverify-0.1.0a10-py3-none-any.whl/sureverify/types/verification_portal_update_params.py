# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import FileTypes

__all__ = [
    "VerificationPortalUpdateParams",
    "Data",
    "DataRelationships",
    "DataRelationshipsPropertyManager",
    "DataRelationshipsPropertyManagerData",
    "DataAttributes",
]


class VerificationPortalUpdateParams(TypedDict, total=False):
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


class DataRelationships(TypedDict, total=False):
    property_manager: Required[DataRelationshipsPropertyManager]
    """The identifier of the related object."""


class DataAttributes(TypedDict, total=False):
    logo: Optional[FileTypes]
    """
    Your company or property logo that will be displayed next to the title to
    residents on the portal.
    """

    muted_color: Optional[str]
    """
    Using the primary brand color as a base, but a bit lighter for background
    colors.
    """

    only_docs_form: bool
    """
    If enabled, the user will only be able to upload documents and skip the policy
    data input.
    """

    primary_color: Optional[str]
    """
    The main brand color used throughout the portal interface, specified in
    hexadecimal format (e.g. #4F46E5).
    """

    secondary_color: Optional[str]
    """Using the primary brand color as a base, but a bit lighter for highlights."""

    show_purchase_flow: bool
    """
    If enabled, the user will be able to purchase renters insurance through the
    portal, as long as there is a Sure Connect partner account configured.
    """

    slug: str
    """A unique, URL-friendly name that will be part of the link to the portal.

    Only lowercase letters, numbers, and hyphens are allowed.
    """

    title: Optional[str]
    """The name displayed at the top of the portal.

    If you want no title, leave this field blank and select a logo. If no title and
    no logo are provided, then the property manager name will be used.
    """


class Data(TypedDict, total=False):
    id: Required[str]

    relationships: Required[DataRelationships]

    type: Required[Literal["VerificationPortal"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: DataAttributes
