# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .verification_portal import VerificationPortal

__all__ = ["VerificationPortalResponse"]


class VerificationPortalResponse(BaseModel):
    data: VerificationPortal
