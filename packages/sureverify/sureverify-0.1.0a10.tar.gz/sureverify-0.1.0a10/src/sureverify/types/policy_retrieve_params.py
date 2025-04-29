# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PolicyRetrieveParams"]


class PolicyRetrieveParams(TypedDict, total=False):
    fields_policy: Annotated[
        List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ],
        PropertyInfo(alias="fields[Policy]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """

    include: List[Literal["lease_address", "interested_party_address", "resident"]]
    """
    include query parameter to allow the client to customize which related resources
    should be returned.
    """
