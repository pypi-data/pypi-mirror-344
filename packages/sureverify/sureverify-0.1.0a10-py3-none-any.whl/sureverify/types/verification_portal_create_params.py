# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .verification_portal_request_data_param import VerificationPortalRequestDataParam

__all__ = ["VerificationPortalCreateParams"]


class VerificationPortalCreateParams(TypedDict, total=False):
    data: Required[VerificationPortalRequestDataParam]
