# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .address_request_data_param import AddressRequestDataParam

__all__ = ["AddressRequestParam"]


class AddressRequestParam(TypedDict, total=False):
    data: Required[AddressRequestDataParam]
