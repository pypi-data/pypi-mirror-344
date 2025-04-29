# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AttachmentCreateResponse", "Data", "DataAttributes"]


class DataAttributes(BaseModel):
    name: str

    file: Optional[str] = None

    presigned_upload_url: Optional[str] = None


class Data(BaseModel):
    id: str

    attributes: DataAttributes

    type: Literal["Attachment"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class AttachmentCreateResponse(BaseModel):
    data: Data
