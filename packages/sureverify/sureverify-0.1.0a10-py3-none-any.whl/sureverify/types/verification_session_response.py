# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .verification_session import VerificationSession

__all__ = ["VerificationSessionResponse"]


class VerificationSessionResponse(BaseModel):
    data: VerificationSession
