# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .address_request_param import AddressRequestParam

__all__ = ["MailboxRequestParam", "Data", "DataAttributes"]


class DataAttributes(TypedDict, total=False):
    address: Required[AddressRequestParam]


class Data(TypedDict, total=False):
    attributes: Required[DataAttributes]

    type: Required[Literal["Mailbox"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class MailboxRequestParam(TypedDict, total=False):
    data: Required[Data]
