# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import date, datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .coverage_kind_enum import CoverageKindEnum
from .editable_fields_enum import EditableFieldsEnum
from .session_related_record_type_enum import SessionRelatedRecordTypeEnum
from .session_settings_brand_color_request_param import SessionSettingsBrandColorRequestParam
from .session_settings_feature_option_request_param import SessionSettingsFeatureOptionRequestParam
from .session_settings_mode_hosted_link_request_param import SessionSettingsModeHostedLinkRequestParam
from .session_settings_on_completion_action_request_param import SessionSettingsOnCompletionActionRequestParam

__all__ = [
    "VerificationSessionRequestDataParam",
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
]


class AttributesRequestRelatedRecord(TypedDict, total=False):
    id: Required[str]
    """Unique identifier of the related record"""

    type: Required[SessionRelatedRecordTypeEnum]
    """
    - `property_manager` - property_manager
    - `community` - community
    - `unit` - unit
    - `resident` - resident
    """


class AttributesRequestSettingsFeatures(TypedDict, total=False):
    purchase: SessionSettingsFeatureOptionRequestParam
    """Configuration for insurance purchase feature"""

    upload: SessionSettingsFeatureOptionRequestParam
    """Configuration for document upload feature"""


class AttributesRequestSettingsModeEmbedded(TypedDict, total=False):
    analytics_enabled: bool
    """Configuration for analytics feature"""

    background_color: str
    """Background color of the embedded page"""

    enabled: bool
    """Whether embedded mode is enabled"""


class AttributesRequestSettingsModeHostedFooter(TypedDict, total=False):
    links: Iterable[SessionSettingsModeHostedLinkRequestParam]
    """Links to display in the footer"""

    text: Optional[str]
    """Text to display in the footer"""


class AttributesRequestSettingsModeHostedHeader(TypedDict, total=False):
    links: Iterable[SessionSettingsModeHostedLinkRequestParam]
    """Navigation links to display in the header"""


class AttributesRequestSettingsModeHosted(TypedDict, total=False):
    analytics_enabled: bool
    """Configuration for analytics feature"""

    enabled: bool
    """Whether hosted mode is enabled"""

    favicon_bgcolor: str
    """Background color of a default-generated favicon if favicon_url is not provided"""

    favicon_url: Optional[str]
    """URL of the favicon to use for the hosted page"""

    footer: Optional[AttributesRequestSettingsModeHostedFooter]
    """Footer configuration for hosted mode"""

    header: Optional[AttributesRequestSettingsModeHostedHeader]
    """Header configuration for hosted mode"""

    return_url: Optional[str]
    """URL to redirect to after verification completion"""

    support_chat_enabled: bool
    """Configuration for support chat feature"""

    user_survey_enabled: bool
    """Configuration for user surveys feature"""


class AttributesRequestSettingsMode(TypedDict, total=False):
    embedded: Optional[AttributesRequestSettingsModeEmbedded]
    """Configuration for embedded mode"""

    hosted: Optional[AttributesRequestSettingsModeHosted]
    """Configuration for hosted mode"""


class AttributesRequestSettingsBrandColors(TypedDict, total=False):
    muted: Optional[SessionSettingsBrandColorRequestParam]
    """Muted brand color"""

    primary: Optional[SessionSettingsBrandColorRequestParam]
    """Primary brand color"""

    secondary: Optional[SessionSettingsBrandColorRequestParam]
    """Secondary brand color"""


class AttributesRequestSettingsBrandStyle(TypedDict, total=False):
    enabled: bool
    """Whether the elements should be styled"""


class AttributesRequestSettingsBrand(TypedDict, total=False):
    colors: AttributesRequestSettingsBrandColors
    """Color scheme configuration for the brand"""

    logo_url: Optional[str]
    """URL of the logo to display in the header"""

    style: AttributesRequestSettingsBrandStyle
    """Style configuration for the brand"""

    title: Optional[str]
    """Title of the brand to display"""


class AttributesRequestSettingsOnCompletion(TypedDict, total=False):
    when_compliant: Optional[SessionSettingsOnCompletionActionRequestParam]
    """Action to take when verification is compliant"""

    when_noncompliant: Optional[SessionSettingsOnCompletionActionRequestParam]
    """Action to take when verification is non-compliant"""

    when_submitted: Optional[SessionSettingsOnCompletionActionRequestParam]
    """Action to take when verification is submitted"""


class AttributesRequestSettingsRestrictionsCoverageRequirement(TypedDict, total=False):
    coverage_kind: Required[CoverageKindEnum]
    """
    - `personal_property` - personal_property
    - `liability` - liability
    - `medical_payments` - medical_payments
    - `loss_of_use` - loss_of_use
    - `water_backup` - water_backup
    - `deductible` - deductible
    - `other` - other
    """

    coverage_minimum: Required[Optional[str]]
    """Required coverage minimum amount"""


class AttributesRequestSettingsRestrictions(TypedDict, total=False):
    coverage_requirements: Iterable[AttributesRequestSettingsRestrictionsCoverageRequirement]
    """List of coverage requirements that must be met"""

    editable_fields: List[EditableFieldsEnum]
    """List of fields that can be edited by the user"""

    max_effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Maximum effective date for the insurance policy"""

    max_expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Maximum expiration date for the insurance policy"""

    min_effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Minimum effective date for the insurance policy"""

    min_expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Minimum expiration date for the insurance policy"""


class AttributesRequestSettings(TypedDict, total=False):
    features: Required[AttributesRequestSettingsFeatures]
    """Feature toggles and configuration"""

    mode: Required[AttributesRequestSettingsMode]
    """Configuration for how the verification session is displayed"""

    brand: AttributesRequestSettingsBrand
    """Branding configuration for the session"""

    external_ref: Optional[str]
    """Developer-provided external reference ID for this session"""

    on_completion: Optional[AttributesRequestSettingsOnCompletion]
    """Actions to take on different completion states"""

    restrictions: Optional[AttributesRequestSettingsRestrictions]
    """Coverage requirements and other restrictions"""


class AttributesRequestInputAddress(TypedDict, total=False):
    city: Optional[str]

    line1: Optional[str]

    line2: Optional[str]

    postal: Optional[str]

    state_code: Optional[str]
    """Two-letter state code"""


class AttributesRequestInput(TypedDict, total=False):
    address: Optional[AttributesRequestInputAddress]
    """Complete address information"""

    carrier: Optional[str]
    """Insurance carrier name"""

    effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """When the insurance policy becomes effective"""

    email: Optional[str]
    """Email address of the insured party"""

    expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """When the insurance policy expires"""

    first_name: Optional[str]
    """First name of the insured party"""

    last_name: Optional[str]
    """Last name of the insured party"""

    lease_end_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """End date of the lease"""

    lease_start_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Start date of the lease"""

    liability_coverage_amount: Optional[int]
    """Amount of liability coverage"""

    phone_number: Optional[str]
    """Phone number of the insured party"""

    policy_number: Optional[str]
    """Insurance policy number"""


class AttributesRequest(TypedDict, total=False):
    related_record: Required[AttributesRequestRelatedRecord]
    """The record this verification is associated with"""

    settings: Required[AttributesRequestSettings]
    """Configuration settings for the session"""

    input: Optional[AttributesRequestInput]
    """Input fields for the verification session"""


class Attributes(TypedDict, total=False):
    expires_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """When this verification session expires"""

    request: Required[AttributesRequest]


class Relationships(TypedDict, total=False):
    pass


class VerificationSessionRequestDataParam(TypedDict, total=False):
    attributes: Required[Attributes]

    type: Required[Literal["VerificationSession"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: Relationships
