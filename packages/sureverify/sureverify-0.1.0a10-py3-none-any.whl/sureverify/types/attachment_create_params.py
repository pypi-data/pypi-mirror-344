# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .presigned_attachment_request_data_param import PresignedAttachmentRequestDataParam

__all__ = ["AttachmentCreateParams"]


class AttachmentCreateParams(TypedDict, total=False):
    data: Required[PresignedAttachmentRequestDataParam]
