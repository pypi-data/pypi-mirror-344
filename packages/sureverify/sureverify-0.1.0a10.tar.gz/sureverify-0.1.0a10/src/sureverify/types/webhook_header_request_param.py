# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WebhookHeaderRequestParam"]


class WebhookHeaderRequestParam(TypedDict, total=False):
    key: Required[str]
    """Header name (e.g. 'Authorization')"""

    value: Required[str]
    """Header value (e.g. 'Bearer token123')"""
