# Addresses

Types:

```python
from sureverify.types import Address, AddressRequest, AddressRequestData, AddressResponse
```

Methods:

- <code title="post /api/v1/addresses">client.addresses.<a href="./src/sureverify/resources/addresses.py">create</a>(\*\*<a href="src/sureverify/types/address_create_params.py">params</a>) -> <a href="./src/sureverify/types/address_response.py">AddressResponse</a></code>
- <code title="get /api/v1/addresses/{id}">client.addresses.<a href="./src/sureverify/resources/addresses.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/address_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/address_response.py">AddressResponse</a></code>
- <code title="patch /api/v1/addresses/{id}">client.addresses.<a href="./src/sureverify/resources/addresses.py">update</a>(id, \*\*<a href="src/sureverify/types/address_update_params.py">params</a>) -> <a href="./src/sureverify/types/address_response.py">AddressResponse</a></code>
- <code title="get /api/v1/addresses">client.addresses.<a href="./src/sureverify/resources/addresses.py">list</a>(\*\*<a href="src/sureverify/types/address_list_params.py">params</a>) -> <a href="./src/sureverify/types/address.py">SyncCursorPagination[Address]</a></code>

# Communities

Types:

```python
from sureverify.types import Community, CommunityRequest, CommunityRequestData, CommunityResponse
```

Methods:

- <code title="post /api/v1/communities">client.communities.<a href="./src/sureverify/resources/communities.py">create</a>(\*\*<a href="src/sureverify/types/community_create_params.py">params</a>) -> <a href="./src/sureverify/types/community_response.py">CommunityResponse</a></code>
- <code title="get /api/v1/communities/{id}">client.communities.<a href="./src/sureverify/resources/communities.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/community_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/community_response.py">CommunityResponse</a></code>
- <code title="patch /api/v1/communities/{id}">client.communities.<a href="./src/sureverify/resources/communities.py">update</a>(id, \*\*<a href="src/sureverify/types/community_update_params.py">params</a>) -> <a href="./src/sureverify/types/community_response.py">CommunityResponse</a></code>
- <code title="get /api/v1/communities">client.communities.<a href="./src/sureverify/resources/communities.py">list</a>(\*\*<a href="src/sureverify/types/community_list_params.py">params</a>) -> <a href="./src/sureverify/types/community.py">SyncCursorPagination[Community]</a></code>

# Policies

Types:

```python
from sureverify.types import (
    Policy,
    PolicyCoverageRequest,
    PolicyRequest,
    PolicyRequestData,
    PolicyResponse,
)
```

Methods:

- <code title="post /api/v1/policies">client.policies.<a href="./src/sureverify/resources/policies.py">create</a>(\*\*<a href="src/sureverify/types/policy_create_params.py">params</a>) -> <a href="./src/sureverify/types/policy_response.py">PolicyResponse</a></code>
- <code title="get /api/v1/policies/{id}">client.policies.<a href="./src/sureverify/resources/policies.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/policy_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/policy_response.py">PolicyResponse</a></code>
- <code title="patch /api/v1/policies/{id}">client.policies.<a href="./src/sureverify/resources/policies.py">update</a>(id, \*\*<a href="src/sureverify/types/policy_update_params.py">params</a>) -> <a href="./src/sureverify/types/policy_response.py">PolicyResponse</a></code>
- <code title="get /api/v1/policies">client.policies.<a href="./src/sureverify/resources/policies.py">list</a>(\*\*<a href="src/sureverify/types/policy_list_params.py">params</a>) -> <a href="./src/sureverify/types/policy.py">SyncCursorPagination[Policy]</a></code>

# PropertyManagers

Types:

```python
from sureverify.types import (
    MailboxRequest,
    PropertyManager,
    PropertyManagerRequest,
    PropertyManagerRequestData,
    PropertyManagerResponse,
)
```

Methods:

- <code title="post /api/v1/property-managers">client.property_managers.<a href="./src/sureverify/resources/property_managers.py">create</a>(\*\*<a href="src/sureverify/types/property_manager_create_params.py">params</a>) -> <a href="./src/sureverify/types/property_manager_response.py">PropertyManagerResponse</a></code>
- <code title="get /api/v1/property-managers/{id}">client.property_managers.<a href="./src/sureverify/resources/property_managers.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/property_manager_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/property_manager_response.py">PropertyManagerResponse</a></code>
- <code title="patch /api/v1/property-managers/{id}">client.property_managers.<a href="./src/sureverify/resources/property_managers.py">update</a>(id, \*\*<a href="src/sureverify/types/property_manager_update_params.py">params</a>) -> <a href="./src/sureverify/types/property_manager_response.py">PropertyManagerResponse</a></code>
- <code title="get /api/v1/property-managers">client.property_managers.<a href="./src/sureverify/resources/property_managers.py">list</a>(\*\*<a href="src/sureverify/types/property_manager_list_params.py">params</a>) -> <a href="./src/sureverify/types/property_manager.py">SyncCursorPagination[PropertyManager]</a></code>

# Residents

Types:

```python
from sureverify.types import Resident, ResidentRequest, ResidentRequestData, ResidentResponse
```

Methods:

- <code title="post /api/v1/residents">client.residents.<a href="./src/sureverify/resources/residents.py">create</a>(\*\*<a href="src/sureverify/types/resident_create_params.py">params</a>) -> <a href="./src/sureverify/types/resident_response.py">ResidentResponse</a></code>
- <code title="get /api/v1/residents/{id}">client.residents.<a href="./src/sureverify/resources/residents.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/resident_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/resident_response.py">ResidentResponse</a></code>
- <code title="patch /api/v1/residents/{id}">client.residents.<a href="./src/sureverify/resources/residents.py">update</a>(id, \*\*<a href="src/sureverify/types/resident_update_params.py">params</a>) -> <a href="./src/sureverify/types/resident_response.py">ResidentResponse</a></code>
- <code title="get /api/v1/residents">client.residents.<a href="./src/sureverify/resources/residents.py">list</a>(\*\*<a href="src/sureverify/types/resident_list_params.py">params</a>) -> <a href="./src/sureverify/types/resident.py">SyncCursorPagination[Resident]</a></code>

# Units

Types:

```python
from sureverify.types import Unit, UnitRequest, UnitRequestData, UnitResponse
```

Methods:

- <code title="post /api/v1/units">client.units.<a href="./src/sureverify/resources/units.py">create</a>(\*\*<a href="src/sureverify/types/unit_create_params.py">params</a>) -> <a href="./src/sureverify/types/unit_response.py">UnitResponse</a></code>
- <code title="get /api/v1/units/{id}">client.units.<a href="./src/sureverify/resources/units.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/unit_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/unit_response.py">UnitResponse</a></code>
- <code title="patch /api/v1/units/{id}">client.units.<a href="./src/sureverify/resources/units.py">update</a>(id, \*\*<a href="src/sureverify/types/unit_update_params.py">params</a>) -> <a href="./src/sureverify/types/unit_response.py">UnitResponse</a></code>
- <code title="get /api/v1/units">client.units.<a href="./src/sureverify/resources/units.py">list</a>(\*\*<a href="src/sureverify/types/unit_list_params.py">params</a>) -> <a href="./src/sureverify/types/unit.py">SyncCursorPagination[Unit]</a></code>

# VerificationCaseInputs

Types:

```python
from sureverify.types import (
    VerificationCaseInput,
    VerificationCaseInputRequest,
    VerificationCaseInputRequestData,
    VerificationCaseInputResponse,
)
```

Methods:

- <code title="post /api/v1/verification-case-inputs">client.verification_case_inputs.<a href="./src/sureverify/resources/verification_case_inputs.py">create</a>(\*\*<a href="src/sureverify/types/verification_case_input_create_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_input_response.py">VerificationCaseInputResponse</a></code>
- <code title="get /api/v1/verification-case-inputs/{id}">client.verification_case_inputs.<a href="./src/sureverify/resources/verification_case_inputs.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/verification_case_input_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_input_response.py">VerificationCaseInputResponse</a></code>
- <code title="patch /api/v1/verification-case-inputs/{id}">client.verification_case_inputs.<a href="./src/sureverify/resources/verification_case_inputs.py">update</a>(id, \*\*<a href="src/sureverify/types/verification_case_input_update_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_input_response.py">VerificationCaseInputResponse</a></code>
- <code title="get /api/v1/verification-case-inputs">client.verification_case_inputs.<a href="./src/sureverify/resources/verification_case_inputs.py">list</a>(\*\*<a href="src/sureverify/types/verification_case_input_list_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_input.py">SyncCursorPagination[VerificationCaseInput]</a></code>

# VerificationCases

Types:

```python
from sureverify.types import (
    VerificationCase,
    VerificationCaseRequest,
    VerificationCaseRequestData,
    VerificationCaseResponse,
)
```

Methods:

- <code title="post /api/v1/verification-cases">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">create</a>(\*\*<a href="src/sureverify/types/verification_case_create_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_response.py">VerificationCaseResponse</a></code>
- <code title="get /api/v1/verification-cases/{id}">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/verification_case_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_response.py">VerificationCaseResponse</a></code>
- <code title="patch /api/v1/verification-cases/{id}">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">update</a>(id, \*\*<a href="src/sureverify/types/verification_case_update_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case_response.py">VerificationCaseResponse</a></code>
- <code title="get /api/v1/verification-cases">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">list</a>(\*\*<a href="src/sureverify/types/verification_case_list_params.py">params</a>) -> <a href="./src/sureverify/types/verification_case.py">SyncCursorPagination[VerificationCase]</a></code>
- <code title="post /api/v1/verification-cases/{id}/enqueue-processing">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">enqueue_processing</a>(id) -> None</code>
- <code title="post /api/v1/verification-cases/{id}/reset-checks">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">reset_checks</a>(id) -> None</code>
- <code title="post /api/v1/verification-cases/{id}/send-reminder-email">client.verification_cases.<a href="./src/sureverify/resources/verification_cases/verification_cases.py">send_reminder_email</a>(id) -> None</code>

## UpdateStatus

Methods:

- <code title="post /api/v1/verification-cases/{id}/update-status/cancelled">client.verification_cases.update_status.<a href="./src/sureverify/resources/verification_cases/update_status.py">cancelled</a>(id) -> None</code>
- <code title="post /api/v1/verification-cases/{id}/update-status/completed">client.verification_cases.update_status.<a href="./src/sureverify/resources/verification_cases/update_status.py">completed</a>(id, \*\*<a href="src/sureverify/types/verification_cases/update_status_completed_params.py">params</a>) -> None</code>
- <code title="post /api/v1/verification-cases/{id}/update-status/draft">client.verification_cases.update_status.<a href="./src/sureverify/resources/verification_cases/update_status.py">draft</a>(id) -> None</code>
- <code title="post /api/v1/verification-cases/{id}/update-status/further-review-required">client.verification_cases.update_status.<a href="./src/sureverify/resources/verification_cases/update_status.py">further_review_required</a>(id) -> None</code>

# VerificationPortalLinks

Types:

```python
from sureverify.types import (
    VerificationPortalLink,
    VerificationPortalLinkRequest,
    VerificationPortalLinkRequestData,
    VerificationPortalLinkResponse,
)
```

Methods:

- <code title="post /api/v1/verification-portal-links">client.verification_portal_links.<a href="./src/sureverify/resources/verification_portal_links.py">create</a>(\*\*<a href="src/sureverify/types/verification_portal_link_create_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_link_response.py">VerificationPortalLinkResponse</a></code>
- <code title="get /api/v1/verification-portal-links/{id}">client.verification_portal_links.<a href="./src/sureverify/resources/verification_portal_links.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/verification_portal_link_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_link_response.py">VerificationPortalLinkResponse</a></code>
- <code title="patch /api/v1/verification-portal-links/{id}">client.verification_portal_links.<a href="./src/sureverify/resources/verification_portal_links.py">update</a>(id, \*\*<a href="src/sureverify/types/verification_portal_link_update_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_link_response.py">VerificationPortalLinkResponse</a></code>
- <code title="get /api/v1/verification-portal-links">client.verification_portal_links.<a href="./src/sureverify/resources/verification_portal_links.py">list</a>(\*\*<a href="src/sureverify/types/verification_portal_link_list_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_link.py">SyncCursorPagination[VerificationPortalLink]</a></code>
- <code title="delete /api/v1/verification-portal-links/{id}">client.verification_portal_links.<a href="./src/sureverify/resources/verification_portal_links.py">delete</a>(id) -> None</code>

# VerificationPortals

Types:

```python
from sureverify.types import (
    VerificationPortal,
    VerificationPortalRequest,
    VerificationPortalRequestData,
    VerificationPortalResponse,
)
```

Methods:

- <code title="post /api/v1/verification-portals">client.verification_portals.<a href="./src/sureverify/resources/verification_portals.py">create</a>(\*\*<a href="src/sureverify/types/verification_portal_create_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_response.py">VerificationPortalResponse</a></code>
- <code title="get /api/v1/verification-portals/{id}">client.verification_portals.<a href="./src/sureverify/resources/verification_portals.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/verification_portal_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_response.py">VerificationPortalResponse</a></code>
- <code title="patch /api/v1/verification-portals/{id}">client.verification_portals.<a href="./src/sureverify/resources/verification_portals.py">update</a>(id, \*\*<a href="src/sureverify/types/verification_portal_update_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal_response.py">VerificationPortalResponse</a></code>
- <code title="get /api/v1/verification-portals">client.verification_portals.<a href="./src/sureverify/resources/verification_portals.py">list</a>(\*\*<a href="src/sureverify/types/verification_portal_list_params.py">params</a>) -> <a href="./src/sureverify/types/verification_portal.py">SyncCursorPagination[VerificationPortal]</a></code>

# VerificationSessions

Types:

```python
from sureverify.types import (
    CoverageKindEnum,
    EditableFieldsEnum,
    SessionRelatedRecordTypeEnum,
    SessionSectionSettings,
    SessionSectionSettingsRequest,
    SessionSettingsBrandColor,
    SessionSettingsBrandColorRequest,
    SessionSettingsFeatureOption,
    SessionSettingsFeatureOptionRequest,
    SessionSettingsModeHostedLink,
    SessionSettingsModeHostedLinkRequest,
    SessionSettingsOnCompletionAction,
    SessionSettingsOnCompletionActionRequest,
    VerificationSession,
    VerificationSessionRequest,
    VerificationSessionRequestData,
    VerificationSessionResponse,
)
```

Methods:

- <code title="post /api/v1/verification-sessions">client.verification_sessions.<a href="./src/sureverify/resources/verification_sessions.py">create</a>(\*\*<a href="src/sureverify/types/verification_session_create_params.py">params</a>) -> <a href="./src/sureverify/types/verification_session_response.py">VerificationSessionResponse</a></code>
- <code title="get /api/v1/verification-sessions/{id}">client.verification_sessions.<a href="./src/sureverify/resources/verification_sessions.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/verification_session_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/verification_session_response.py">VerificationSessionResponse</a></code>
- <code title="delete /api/v1/verification-sessions/{id}">client.verification_sessions.<a href="./src/sureverify/resources/verification_sessions.py">delete</a>(id) -> None</code>

# WebhookEndpoints

Types:

```python
from sureverify.types import (
    WebhookEndpoint,
    WebhookEndpointRequest,
    WebhookEndpointRequestData,
    WebhookEndpointResponse,
    WebhookEventTypeRequest,
    WebhookHeaderRequest,
)
```

Methods:

- <code title="post /api/v1/webhook-endpoints">client.webhook_endpoints.<a href="./src/sureverify/resources/webhook_endpoints.py">create</a>(\*\*<a href="src/sureverify/types/webhook_endpoint_create_params.py">params</a>) -> <a href="./src/sureverify/types/webhook_endpoint_response.py">WebhookEndpointResponse</a></code>
- <code title="get /api/v1/webhook-endpoints/{id}">client.webhook_endpoints.<a href="./src/sureverify/resources/webhook_endpoints.py">retrieve</a>(id, \*\*<a href="src/sureverify/types/webhook_endpoint_retrieve_params.py">params</a>) -> <a href="./src/sureverify/types/webhook_endpoint_response.py">WebhookEndpointResponse</a></code>
- <code title="patch /api/v1/webhook-endpoints/{id}">client.webhook_endpoints.<a href="./src/sureverify/resources/webhook_endpoints.py">update</a>(id, \*\*<a href="src/sureverify/types/webhook_endpoint_update_params.py">params</a>) -> <a href="./src/sureverify/types/webhook_endpoint_response.py">WebhookEndpointResponse</a></code>
- <code title="get /api/v1/webhook-endpoints">client.webhook_endpoints.<a href="./src/sureverify/resources/webhook_endpoints.py">list</a>(\*\*<a href="src/sureverify/types/webhook_endpoint_list_params.py">params</a>) -> <a href="./src/sureverify/types/webhook_endpoint.py">SyncCursorPagination[WebhookEndpoint]</a></code>
- <code title="delete /api/v1/webhook-endpoints/{id}">client.webhook_endpoints.<a href="./src/sureverify/resources/webhook_endpoints.py">delete</a>(id) -> None</code>

# Attachments

Types:

```python
from sureverify.types import (
    PresignedAttachmentRequest,
    PresignedAttachmentRequestData,
    AttachmentCreateResponse,
)
```

Methods:

- <code title="post /api/v1/attachments">client.attachments.<a href="./src/sureverify/resources/attachments.py">create</a>(\*\*<a href="src/sureverify/types/attachment_create_params.py">params</a>) -> <a href="./src/sureverify/types/attachment_create_response.py">AttachmentCreateResponse</a></code>
