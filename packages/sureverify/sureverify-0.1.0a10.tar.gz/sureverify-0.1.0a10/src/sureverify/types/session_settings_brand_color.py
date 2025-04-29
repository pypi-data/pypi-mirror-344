# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SessionSettingsBrandColor"]


class SessionSettingsBrandColor(BaseModel):
    hex: str
    """Hex color code (e.g., #FF0000)"""
