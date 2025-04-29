# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date, datetime
from typing_extensions import Literal

from .._models import BaseModel
from .coverage_kind_enum import CoverageKindEnum
from .editable_fields_enum import EditableFieldsEnum
from .session_settings_brand_color import SessionSettingsBrandColor
from .session_settings_feature_option import SessionSettingsFeatureOption
from .session_related_record_type_enum import SessionRelatedRecordTypeEnum
from .session_settings_mode_hosted_link import SessionSettingsModeHostedLink
from .session_settings_on_completion_action import SessionSettingsOnCompletionAction

__all__ = [
    "VerificationSession",
    "Attributes",
    "AttributesRequest",
    "AttributesRequestRelatedRecord",
    "AttributesRequestSettings",
    "AttributesRequestSettingsFeatures",
    "AttributesRequestSettingsMode",
    "AttributesRequestSettingsModeEmbedded",
    "AttributesRequestSettingsModeHosted",
    "AttributesRequestSettingsModeHostedFooter",
    "AttributesRequestSettingsModeHostedHeader",
    "AttributesRequestSettingsBrand",
    "AttributesRequestSettingsBrandColors",
    "AttributesRequestSettingsBrandStyle",
    "AttributesRequestSettingsOnCompletion",
    "AttributesRequestSettingsRestrictions",
    "AttributesRequestSettingsRestrictionsCoverageRequirement",
    "AttributesRequestInput",
    "AttributesRequestInputAddress",
    "Relationships",
    "RelationshipsCase",
    "RelationshipsCaseData",
    "RelationshipsCommunity",
    "RelationshipsCommunityData",
    "RelationshipsPropertyManager",
    "RelationshipsPropertyManagerData",
    "RelationshipsResident",
    "RelationshipsResidentData",
    "RelationshipsUnit",
    "RelationshipsUnitData",
]


class AttributesRequestRelatedRecord(BaseModel):
    id: str
    """Unique identifier of the related record"""

    type: SessionRelatedRecordTypeEnum
    """
    - `property_manager` - property_manager
    - `community` - community
    - `unit` - unit
    - `resident` - resident
    """


class AttributesRequestSettingsFeatures(BaseModel):
    purchase: Optional[SessionSettingsFeatureOption] = None
    """Configuration for insurance purchase feature"""

    upload: Optional[SessionSettingsFeatureOption] = None
    """Configuration for document upload feature"""


class AttributesRequestSettingsModeEmbedded(BaseModel):
    analytics_enabled: Optional[bool] = None
    """Configuration for analytics feature"""

    background_color: Optional[str] = None
    """Background color of the embedded page"""

    enabled: Optional[bool] = None
    """Whether embedded mode is enabled"""


class AttributesRequestSettingsModeHostedFooter(BaseModel):
    links: Optional[List[SessionSettingsModeHostedLink]] = None
    """Links to display in the footer"""

    text: Optional[str] = None
    """Text to display in the footer"""


class AttributesRequestSettingsModeHostedHeader(BaseModel):
    links: Optional[List[SessionSettingsModeHostedLink]] = None
    """Navigation links to display in the header"""


class AttributesRequestSettingsModeHosted(BaseModel):
    analytics_enabled: Optional[bool] = None
    """Configuration for analytics feature"""

    enabled: Optional[bool] = None
    """Whether hosted mode is enabled"""

    favicon_bgcolor: Optional[str] = None
    """Background color of a default-generated favicon if favicon_url is not provided"""

    favicon_url: Optional[str] = None
    """URL of the favicon to use for the hosted page"""

    footer: Optional[AttributesRequestSettingsModeHostedFooter] = None
    """Footer configuration for hosted mode"""

    header: Optional[AttributesRequestSettingsModeHostedHeader] = None
    """Header configuration for hosted mode"""

    return_url: Optional[str] = None
    """URL to redirect to after verification completion"""

    support_chat_enabled: Optional[bool] = None
    """Configuration for support chat feature"""

    user_survey_enabled: Optional[bool] = None
    """Configuration for user surveys feature"""


class AttributesRequestSettingsMode(BaseModel):
    embedded: Optional[AttributesRequestSettingsModeEmbedded] = None
    """Configuration for embedded mode"""

    hosted: Optional[AttributesRequestSettingsModeHosted] = None
    """Configuration for hosted mode"""


class AttributesRequestSettingsBrandColors(BaseModel):
    muted: Optional[SessionSettingsBrandColor] = None
    """Muted brand color"""

    primary: Optional[SessionSettingsBrandColor] = None
    """Primary brand color"""

    secondary: Optional[SessionSettingsBrandColor] = None
    """Secondary brand color"""


class AttributesRequestSettingsBrandStyle(BaseModel):
    enabled: Optional[bool] = None
    """Whether the elements should be styled"""


class AttributesRequestSettingsBrand(BaseModel):
    colors: Optional[AttributesRequestSettingsBrandColors] = None
    """Color scheme configuration for the brand"""

    logo_url: Optional[str] = None
    """URL of the logo to display in the header"""

    style: Optional[AttributesRequestSettingsBrandStyle] = None
    """Style configuration for the brand"""

    title: Optional[str] = None
    """Title of the brand to display"""


class AttributesRequestSettingsOnCompletion(BaseModel):
    when_compliant: Optional[SessionSettingsOnCompletionAction] = None
    """Action to take when verification is compliant"""

    when_noncompliant: Optional[SessionSettingsOnCompletionAction] = None
    """Action to take when verification is non-compliant"""

    when_submitted: Optional[SessionSettingsOnCompletionAction] = None
    """Action to take when verification is submitted"""


class AttributesRequestSettingsRestrictionsCoverageRequirement(BaseModel):
    coverage_kind: CoverageKindEnum
    """
    - `personal_property` - personal_property
    - `liability` - liability
    - `medical_payments` - medical_payments
    - `loss_of_use` - loss_of_use
    - `water_backup` - water_backup
    - `deductible` - deductible
    - `other` - other
    """

    coverage_minimum: Optional[str] = None
    """Required coverage minimum amount"""


class AttributesRequestSettingsRestrictions(BaseModel):
    coverage_requirements: Optional[List[AttributesRequestSettingsRestrictionsCoverageRequirement]] = None
    """List of coverage requirements that must be met"""

    editable_fields: Optional[List[EditableFieldsEnum]] = None
    """List of fields that can be edited by the user"""

    max_effective_date: Optional[date] = None
    """Maximum effective date for the insurance policy"""

    max_expiration_date: Optional[date] = None
    """Maximum expiration date for the insurance policy"""

    min_effective_date: Optional[date] = None
    """Minimum effective date for the insurance policy"""

    min_expiration_date: Optional[date] = None
    """Minimum expiration date for the insurance policy"""


class AttributesRequestSettings(BaseModel):
    features: AttributesRequestSettingsFeatures
    """Feature toggles and configuration"""

    mode: AttributesRequestSettingsMode
    """Configuration for how the verification session is displayed"""

    brand: Optional[AttributesRequestSettingsBrand] = None
    """Branding configuration for the session"""

    external_ref: Optional[str] = None
    """Developer-provided external reference ID for this session"""

    on_completion: Optional[AttributesRequestSettingsOnCompletion] = None
    """Actions to take on different completion states"""

    restrictions: Optional[AttributesRequestSettingsRestrictions] = None
    """Coverage requirements and other restrictions"""


class AttributesRequestInputAddress(BaseModel):
    city: Optional[str] = None

    line1: Optional[str] = None

    line2: Optional[str] = None

    postal: Optional[str] = None

    state_code: Optional[str] = None
    """Two-letter state code"""


class AttributesRequestInput(BaseModel):
    address: Optional[AttributesRequestInputAddress] = None
    """Complete address information"""

    carrier: Optional[str] = None
    """Insurance carrier name"""

    effective_date: Optional[date] = None
    """When the insurance policy becomes effective"""

    email: Optional[str] = None
    """Email address of the insured party"""

    expiration_date: Optional[date] = None
    """When the insurance policy expires"""

    first_name: Optional[str] = None
    """First name of the insured party"""

    last_name: Optional[str] = None
    """Last name of the insured party"""

    lease_end_date: Optional[date] = None
    """End date of the lease"""

    lease_start_date: Optional[date] = None
    """Start date of the lease"""

    liability_coverage_amount: Optional[int] = None
    """Amount of liability coverage"""

    phone_number: Optional[str] = None
    """Phone number of the insured party"""

    policy_number: Optional[str] = None
    """Insurance policy number"""


class AttributesRequest(BaseModel):
    related_record: AttributesRequestRelatedRecord
    """The record this verification is associated with"""

    settings: AttributesRequestSettings
    """Configuration settings for the session"""

    input: Optional[AttributesRequestInput] = None
    """Input fields for the verification session"""


class Attributes(BaseModel):
    expires_at: datetime
    """When this verification session expires"""

    request: AttributesRequest

    created_at: Optional[datetime] = None

    embedded_token: Optional[str] = None
    """Client-side SDK token for embedded mode integration"""

    hosted_url: Optional[str] = None
    """URL to access the hosted verification flow (only available in hosted mode)"""


class RelationshipsCaseData(BaseModel):
    id: str

    type: Literal["VerificationCase"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCase(BaseModel):
    data: Optional[RelationshipsCaseData] = None


class RelationshipsCommunityData(BaseModel):
    id: str

    type: Literal["Community"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCommunity(BaseModel):
    data: Optional[RelationshipsCommunityData] = None


class RelationshipsPropertyManagerData(BaseModel):
    id: str

    type: Literal["PropertyManager"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPropertyManager(BaseModel):
    data: Optional[RelationshipsPropertyManagerData] = None


class RelationshipsResidentData(BaseModel):
    id: str

    type: Literal["Resident"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsResident(BaseModel):
    data: Optional[RelationshipsResidentData] = None


class RelationshipsUnitData(BaseModel):
    id: str

    type: Literal["Unit"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsUnit(BaseModel):
    data: Optional[RelationshipsUnitData] = None


class Relationships(BaseModel):
    case: Optional[RelationshipsCase] = None
    """The identifier of the related object."""

    community: Optional[RelationshipsCommunity] = None
    """The identifier of the related object."""

    property_manager: Optional[RelationshipsPropertyManager] = None
    """The identifier of the related object."""

    resident: Optional[RelationshipsResident] = None
    """The identifier of the related object."""

    unit: Optional[RelationshipsUnit] = None
    """The identifier of the related object."""


class VerificationSession(BaseModel):
    id: str

    attributes: Attributes

    type: Literal["VerificationSession"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: Optional[Relationships] = None
