# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["SessionSettingsOnCompletionActionRequestParam"]


class SessionSettingsOnCompletionActionRequestParam(TypedDict, total=False):
    custom_event_name: Optional[str]
    """Name of the custom browser event to dispatch"""

    message: Optional[str]
    """Message to display to the user"""

    redirect: Optional[str]
    """URL to redirect the user to"""
