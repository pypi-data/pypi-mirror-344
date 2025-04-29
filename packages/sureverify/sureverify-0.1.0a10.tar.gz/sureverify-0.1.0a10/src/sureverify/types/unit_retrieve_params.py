# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UnitRetrieveParams"]


class UnitRetrieveParams(TypedDict, total=False):
    fields_unit: Annotated[
        List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ],
        PropertyInfo(alias="fields[Unit]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["community", "address"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """
