# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["PresignedAttachmentRequestDataParam", "Attributes"]


class Attributes(TypedDict, total=False):
    content_type: Required[Literal["application/pdf", "image/gif", "image/jpeg", "image/png"]]
    """
    - `application/pdf` - application/pdf
    - `image/gif` - image/gif
    - `image/jpeg` - image/jpeg
    - `image/png` - image/png
    """

    name: Required[str]


class PresignedAttachmentRequestDataParam(TypedDict, total=False):
    attributes: Required[Attributes]

    type: Required[Literal["Attachment"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
