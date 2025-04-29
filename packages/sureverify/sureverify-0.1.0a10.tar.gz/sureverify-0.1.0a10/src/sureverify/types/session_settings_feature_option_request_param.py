# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .session_section_settings_request_param import SessionSectionSettingsRequestParam

__all__ = ["SessionSettingsFeatureOptionRequestParam", "DetailsPage", "InstructionsPage"]


class DetailsPage(TypedDict, total=False):
    enabled: bool
    """Whether this page is enabled"""


class InstructionsPage(TypedDict, total=False):
    coverage_requirements_section: SessionSectionSettingsRequestParam
    """Configuration for coverage requirements section"""

    enabled: bool
    """Whether this page is enabled"""

    evidence_requirements_section: SessionSectionSettingsRequestParam
    """Configuration for documentation/evidence requirements section"""

    explainer_section: SessionSectionSettingsRequestParam
    """Configuration for explainer video section"""

    interested_party_section: SessionSectionSettingsRequestParam
    """Configuration for interested party section"""


class SessionSettingsFeatureOptionRequestParam(TypedDict, total=False):
    details_page: DetailsPage
    """Configuration for details page"""

    enabled: bool
    """Whether this feature is enabled"""

    instructions_page: InstructionsPage
    """Configuration for instructions page"""
