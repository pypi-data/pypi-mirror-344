# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationPortalRetrieveParams"]


class VerificationPortalRetrieveParams(TypedDict, total=False):
    fields_verification_portal: Annotated[
        List[
            Literal[
                "property_manager",
                "title",
                "slug",
                "logo",
                "primary_color",
                "secondary_color",
                "muted_color",
                "show_purchase_flow",
                "only_docs_form",
            ]
        ],
        PropertyInfo(alias="fields[VerificationPortal]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["property_manager"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """
