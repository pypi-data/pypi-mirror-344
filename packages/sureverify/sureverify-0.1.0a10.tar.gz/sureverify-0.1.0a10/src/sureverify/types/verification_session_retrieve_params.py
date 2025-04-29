# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationSessionRetrieveParams"]


class VerificationSessionRetrieveParams(TypedDict, total=False):
    fields_verification_session: Annotated[
        List[
            Literal[
                "case",
                "expires_at",
                "created_at",
                "request",
                "hosted_url",
                "embedded_token",
                "property_manager",
                "community",
                "unit",
                "resident",
            ]
        ],
        PropertyInfo(alias="fields[VerificationSession]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """
