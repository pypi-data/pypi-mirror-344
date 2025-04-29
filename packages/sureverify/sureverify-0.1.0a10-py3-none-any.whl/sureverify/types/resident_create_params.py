# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .resident_request_data_param import ResidentRequestDataParam

__all__ = ["ResidentCreateParams"]


class ResidentCreateParams(TypedDict, total=False):
    data: Required[ResidentRequestDataParam]
