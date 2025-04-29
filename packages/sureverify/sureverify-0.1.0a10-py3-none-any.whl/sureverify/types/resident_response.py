# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .resident import Resident

__all__ = ["ResidentResponse"]


class ResidentResponse(BaseModel):
    data: Resident
