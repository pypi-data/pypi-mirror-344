# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "VerificationCaseInputRequestDataParam",
    "Relationships",
    "RelationshipsCase",
    "RelationshipsCaseData",
    "RelationshipsAddress",
    "RelationshipsAddressData",
    "Attributes",
]


class RelationshipsCaseData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["VerificationCase"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCase(TypedDict, total=False):
    data: Required[RelationshipsCaseData]


class RelationshipsAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAddress(TypedDict, total=False):
    data: Required[RelationshipsAddressData]


class Relationships(TypedDict, total=False):
    case: Required[RelationshipsCase]
    """The identifier of the related object."""

    address: Optional[RelationshipsAddress]
    """The identifier of the related object."""


class Attributes(TypedDict, total=False):
    carrier: Optional[str]

    effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    email: Optional[str]
    """We may contact you for verification needs."""

    expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    first_name: Optional[str]
    """First and last name as written on your policy."""

    last_name: Optional[str]

    liability_coverage_amount: Optional[str]

    phone_number: Optional[str]

    policy_number: Optional[str]


class VerificationCaseInputRequestDataParam(TypedDict, total=False):
    relationships: Required[Relationships]

    type: Required[Literal["VerificationCaseInput"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Attributes
