# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .property_manager_request_data_param import PropertyManagerRequestDataParam

__all__ = ["PropertyManagerCreateParams"]


class PropertyManagerCreateParams(TypedDict, total=False):
    data: Required[PropertyManagerRequestDataParam]
