# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .verification_case_input_request_data_param import VerificationCaseInputRequestDataParam

__all__ = ["VerificationCaseInputCreateParams"]


class VerificationCaseInputCreateParams(TypedDict, total=False):
    data: Required[VerificationCaseInputRequestDataParam]
