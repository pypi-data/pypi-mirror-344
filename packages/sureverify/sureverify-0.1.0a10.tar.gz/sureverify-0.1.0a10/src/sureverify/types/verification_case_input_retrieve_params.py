# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationCaseInputRetrieveParams"]


class VerificationCaseInputRetrieveParams(TypedDict, total=False):
    fields_verification_case_input: Annotated[
        List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[VerificationCaseInput]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["address", "case"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """
