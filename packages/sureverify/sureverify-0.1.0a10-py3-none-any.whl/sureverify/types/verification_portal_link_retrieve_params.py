# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VerificationPortalLinkRetrieveParams"]


class VerificationPortalLinkRetrieveParams(TypedDict, total=False):
    fields_verification_portal_link: Annotated[
        List[Literal["portal", "title", "url", "weight", "location"]],
        PropertyInfo(alias="fields[VerificationPortalLink]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """
