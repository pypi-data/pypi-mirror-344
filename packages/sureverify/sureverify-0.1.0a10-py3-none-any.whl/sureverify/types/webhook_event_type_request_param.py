# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebhookEventTypeRequestParam"]


class WebhookEventTypeRequestParam(TypedDict, total=False):
    key: Required[
        Literal[
            "case.submitted",
            "case.compliant",
            "case.non_compliant",
            "resident.expiring_soon",
            "resident.becoming_non_compliant",
            "policy.new",
            "policy.updated",
        ]
    ]
    """
    - `case.submitted` - Portal Case Submitted
    - `case.compliant` - Portal Case Compliant
    - `case.non_compliant` - Portal Case Non-Compliant
    - `resident.expiring_soon` - Compliance Expiring Soon
    - `resident.becoming_non_compliant` - Becoming Non-Compliant
    - `policy.new` - New Policy Added
    - `policy.updated` - Policy Updated
    """
