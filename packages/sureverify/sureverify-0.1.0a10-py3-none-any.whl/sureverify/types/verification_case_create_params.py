# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .verification_case_request_data_param import VerificationCaseRequestDataParam

__all__ = ["VerificationCaseCreateParams"]


class VerificationCaseCreateParams(TypedDict, total=False):
    data: Required[VerificationCaseRequestDataParam]
