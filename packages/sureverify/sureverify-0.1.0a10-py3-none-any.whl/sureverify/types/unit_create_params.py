# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .unit_request_data_param import UnitRequestDataParam

__all__ = ["UnitCreateParams"]


class UnitCreateParams(TypedDict, total=False):
    data: Required[UnitRequestDataParam]
