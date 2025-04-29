# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["EditableFieldsEnum"]

EditableFieldsEnum: TypeAlias = Literal[
    "address.line1",
    "address.line2",
    "address.city",
    "address.state_code",
    "address.postal",
    "carrier",
    "policy_number",
    "effective_date",
    "expiration_date",
    "liability_coverage_amount",
    "first_name",
    "last_name",
    "email",
    "phone_number",
]
