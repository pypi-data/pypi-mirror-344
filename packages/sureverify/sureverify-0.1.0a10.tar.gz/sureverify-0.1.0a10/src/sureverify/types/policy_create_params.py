# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .policy_request_data_param import PolicyRequestDataParam

__all__ = ["PolicyCreateParams"]


class PolicyCreateParams(TypedDict, total=False):
    data: Required[PolicyRequestDataParam]
