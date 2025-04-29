# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["SessionSettingsOnCompletionAction"]


class SessionSettingsOnCompletionAction(BaseModel):
    custom_event_name: Optional[str] = None
    """Name of the custom browser event to dispatch"""

    message: Optional[str] = None
    """Message to display to the user"""

    redirect: Optional[str] = None
    """URL to redirect the user to"""
