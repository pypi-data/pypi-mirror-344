# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .session_section_settings import SessionSectionSettings

__all__ = ["SessionSettingsFeatureOption", "DetailsPage", "InstructionsPage"]


class DetailsPage(BaseModel):
    enabled: Optional[bool] = None
    """Whether this page is enabled"""


class InstructionsPage(BaseModel):
    coverage_requirements_section: Optional[SessionSectionSettings] = None
    """Configuration for coverage requirements section"""

    enabled: Optional[bool] = None
    """Whether this page is enabled"""

    evidence_requirements_section: Optional[SessionSectionSettings] = None
    """Configuration for documentation/evidence requirements section"""

    explainer_section: Optional[SessionSectionSettings] = None
    """Configuration for explainer video section"""

    interested_party_section: Optional[SessionSectionSettings] = None
    """Configuration for interested party section"""


class SessionSettingsFeatureOption(BaseModel):
    details_page: Optional[DetailsPage] = None
    """Configuration for details page"""

    enabled: Optional[bool] = None
    """Whether this feature is enabled"""

    instructions_page: Optional[InstructionsPage] = None
    """Configuration for instructions page"""
