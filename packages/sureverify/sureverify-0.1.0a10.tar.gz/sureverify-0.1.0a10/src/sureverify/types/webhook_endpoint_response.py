# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .webhook_endpoint import WebhookEndpoint

__all__ = ["WebhookEndpointResponse"]


class WebhookEndpointResponse(BaseModel):
    data: WebhookEndpoint
