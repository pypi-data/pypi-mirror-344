# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .verification_portal_link_request_data_param import VerificationPortalLinkRequestDataParam

__all__ = ["VerificationPortalLinkCreateParams"]


class VerificationPortalLinkCreateParams(TypedDict, total=False):
    data: Required[VerificationPortalLinkRequestDataParam]
