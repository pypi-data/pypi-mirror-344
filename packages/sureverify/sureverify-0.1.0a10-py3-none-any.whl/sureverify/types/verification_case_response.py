# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .verification_case import VerificationCase

__all__ = ["VerificationCaseResponse"]


class VerificationCaseResponse(BaseModel):
    data: VerificationCase
