# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .verification_portal_link import VerificationPortalLink

__all__ = ["VerificationPortalLinkResponse"]


class VerificationPortalLinkResponse(BaseModel):
    data: VerificationPortalLink
