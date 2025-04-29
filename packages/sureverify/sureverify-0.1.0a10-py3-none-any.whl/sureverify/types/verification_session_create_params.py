# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .verification_session_request_data_param import VerificationSessionRequestDataParam

__all__ = ["VerificationSessionCreateParams"]


class VerificationSessionCreateParams(TypedDict, total=False):
    data: Required[VerificationSessionRequestDataParam]
