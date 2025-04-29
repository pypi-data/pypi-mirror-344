# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["UpdateStatusCompletedParams", "Data", "DataAttributes"]


class UpdateStatusCompletedParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
    is_compliant: Required[bool]

    decision_reason: str

    notes: str


class Data(TypedDict, total=False):
    attributes: Required[DataAttributes]

    type: Required[Literal["UpdateComplianceAction"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
