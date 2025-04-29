# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "VerificationPortalLinkUpdateParams",
    "Data",
    "DataAttributes",
    "DataRelationships",
    "DataRelationshipsPortal",
    "DataRelationshipsPortalData",
]


class VerificationPortalLinkUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
    location: Required[Literal["header", "footer"]]
    """Location of the link

    - `header` - Header
    - `footer` - Footer
    """

    title: Required[str]
    """Title of the link"""

    url: Required[str]
    """URL for the link"""

    weight: int
    """Order in which the link appears, lower numbers appear first"""


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


class DataRelationships(TypedDict, total=False):
    portal: Required[DataRelationshipsPortal]
    """The identifier of the related object."""


class Data(TypedDict, total=False):
    id: Required[str]

    attributes: Required[DataAttributes]

    relationships: Required[DataRelationships]

    type: Required[Literal["VerificationPortalLink"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
