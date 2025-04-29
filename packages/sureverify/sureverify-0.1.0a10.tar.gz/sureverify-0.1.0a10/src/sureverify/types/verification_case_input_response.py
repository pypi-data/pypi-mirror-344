# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .verification_case_input import VerificationCaseInput

__all__ = ["VerificationCaseInputResponse"]


class VerificationCaseInputResponse(BaseModel):
    data: VerificationCaseInput
