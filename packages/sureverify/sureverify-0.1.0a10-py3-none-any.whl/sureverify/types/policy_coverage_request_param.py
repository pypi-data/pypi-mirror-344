# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["PolicyCoverageRequestParam", "Data", "DataAttributes"]


class DataAttributes(TypedDict, total=False):
    name: Required[str]

    included: Optional[bool]

    limit: Optional[float]

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """


class Data(TypedDict, total=False):
    attributes: Required[DataAttributes]

    type: Required[Literal["PolicyCoverage"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class PolicyCoverageRequestParam(TypedDict, total=False):
    data: Required[Data]
