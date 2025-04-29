# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .unit import Unit
from .._models import BaseModel

__all__ = ["UnitResponse"]


class UnitResponse(BaseModel):
    data: Unit
