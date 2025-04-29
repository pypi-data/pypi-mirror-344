# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .property_manager import PropertyManager

__all__ = ["PropertyManagerResponse"]


class PropertyManagerResponse(BaseModel):
    data: PropertyManager
