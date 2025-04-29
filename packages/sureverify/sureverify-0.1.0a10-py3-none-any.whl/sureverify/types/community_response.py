# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .community import Community

__all__ = ["CommunityResponse"]


class CommunityResponse(BaseModel):
    data: Community
