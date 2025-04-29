# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SessionSettingsModeHostedLinkRequestParam"]


class SessionSettingsModeHostedLinkRequestParam(TypedDict, total=False):
    title: Required[str]
    """Display text for the link"""

    url: Required[str]
    """URL the link points to"""
