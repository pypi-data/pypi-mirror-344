import os

from sureverify import Verify
from sureverify.types import WebhookEndpointRequestDataParam
from sureverify.lib.auth import generate_jwt_bearer_token


def init_client() -> Verify:
    """Initialize the Verify SDK client with JWT authentication."""
    # Read private key from file
    if private_key_var := os.environ.get("VERIFY_PRIVATE_KEY"):
        private_key = private_key_var.encode("utf-8")
    else:
        private_key_path = os.environ.get("VERIFY_PRIVATE_KEY_PATH", "private.pem")
        with open(private_key_path, "rb") as key_file:
            private_key = key_file.read()

    # Get authentication parameters from environment
    key_id = os.environ.get("VERIFY_KEY_ID")
    user_id = os.environ.get("VERIFY_USER_ID")
    issuer = os.environ.get("VERIFY_ISSUER", "YOUR_ORG_NAME")

    if not key_id or not user_id:
        raise ValueError("VERIFY_KEY_ID and VERIFY_USER_ID environment variables must be set")

    # Generate JWT token
    bearer_token = generate_jwt_bearer_token(
        key_id=key_id, user_id=user_id, private_key_pem_format=private_key, issuer=issuer
    )

    # Initialize client with generated token
    return Verify(bearer_token=bearer_token)


def main() -> None:
    """Example workflow for setting up and handling webhooks."""

    # Initialize the client
    client = init_client()

    # In a real application, set this to your publicly accessible URL
    # For testing, you can use a service like ngrok (https://ngrok.com/)
    webhook_url = "https://example.com/webhooks/verify"

    # Define webhook events to subscribe to
    webhook_data = WebhookEndpointRequestDataParam(
        type="WebhookEndpoint",
        attributes={
            "name": "Verification status webhook",
            "url": webhook_url,
            "subscribed_events": [
                {
                    "key": "case.compliant",
                },
            ],
            "headers": [
                {
                    "key": "Authorization",
                    "value": "optional_value",
                }
            ],
        },
    )

    # Create the webhook subscription
    webhook_response = client.webhook_endpoints.create(data=webhook_data)

    webhook_id = webhook_response.data.id

    print(f"Created webhook subscription with ID: {webhook_id}")
    print("Keep this secret secure! It's used to verify webhook signatures.")


if __name__ == "__main__":
    main()
