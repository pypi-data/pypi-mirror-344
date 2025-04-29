# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["VerificationPortalLink", "Attributes", "Relationships", "RelationshipsPortal", "RelationshipsPortalData"]


class Attributes(BaseModel):
    location: Literal["header", "footer"]
    """Location of the link

    - `header` - Header
    - `footer` - Footer
    """

    title: str
    """Title of the link"""

    url: str
    """URL for the link"""

    weight: Optional[int] = None
    """Order in which the link appears, lower numbers appear first"""


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


class Relationships(BaseModel):
    portal: RelationshipsPortal
    """The identifier of the related object."""


class VerificationPortalLink(BaseModel):
    id: str

    attributes: Attributes

    relationships: Relationships

    type: Literal["VerificationPortalLink"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
