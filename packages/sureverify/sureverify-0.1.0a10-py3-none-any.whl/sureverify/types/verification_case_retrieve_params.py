# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationCaseRetrieveParams"]


class VerificationCaseRetrieveParams(TypedDict, total=False):
    fields_verification_case: Annotated[
        List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[VerificationCase]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """
