# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SessionSettingsModeHostedLink"]


class SessionSettingsModeHostedLink(BaseModel):
    title: str
    """Display text for the link"""

    url: str
    """URL the link points to"""
