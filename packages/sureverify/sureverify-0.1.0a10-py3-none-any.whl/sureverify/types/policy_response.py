# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .policy import Policy
from .._models import BaseModel

__all__ = ["PolicyResponse"]


class PolicyResponse(BaseModel):
    data: Policy
