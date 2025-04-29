# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .community_request_data_param import CommunityRequestDataParam

__all__ = ["CommunityCreateParams"]


class CommunityCreateParams(TypedDict, total=False):
    data: Required[CommunityRequestDataParam]
