import os
import datetime
from typing import Any, Dict, cast
from datetime import timezone, timedelta

from sureverify import Verify
from sureverify.lib.auth import generate_jwt_bearer_token
from sureverify.types.verification_session_response import VerificationSessionResponse
from sureverify.types.verification_session_request_data_param import VerificationSessionRequestDataParam


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


def create_hosted_verification_session(client: Verify, resident_id: str) -> VerificationSessionResponse:
    """
    Create a hosted verification session for a resident.

    Args:
        client: The Verify SDK client
        resident_id: ID of the resident to verify

    Returns:
        The created verification session
    """
    # Set expiration date to 7 days from now (using timezone-aware datetime)
    expires_at = (datetime.datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    # Create verification session with hosted mode
    attributes: Dict[str, Any] = {
        "expires_at": expires_at,
        "request": {
            "related_record": {"type": "resident", "id": resident_id},
            "settings": {
                "mode": {
                    "hosted": {
                        "enabled": True,
                        "return_url": "https://your-property-portal.com/verification-complete",
                        "header": {"links": [{"title": "Help", "url": "https://your-property-portal.com/help"}]},
                    }
                },
                "brand": {
                    "title": "Your Property Name",
                    "logo_url": "https://your-property-portal.com/logo.png",
                    "colors": {"primary": {"hex": "#4A90E2"}},
                },
                "features": {"upload": {"enabled": True}, "purchase": {"enabled": True}},
            },
        },
    }

    session_data = VerificationSessionRequestDataParam(
        type="VerificationSession",
        attributes=cast(Any, attributes),  # Use cast to bypass type checking
    )

    # Create the verification session
    session: VerificationSessionResponse = client.verification_sessions.create(data=session_data)
    return session


def main() -> None:
    """Example workflow for using hosted verification sessions."""

    # Initialize the client
    client = init_client()

    residents = client.residents.list()
    resident_id = residents.data[0].id

    # Create a hosted verification session
    print("\nCreating a hosted verification session...")
    hosted_session = create_hosted_verification_session(client, resident_id)

    if not hosted_session.data or not hosted_session.data.attributes:
        raise ValueError("Failed to create hosted verification session")

    hosted_session_id = hosted_session.data.id
    hosted_url = hosted_session.data.attributes.hosted_url

    print(f"Hosted session created with ID: {hosted_session_id}")
    print(f"Redirect your user to this URL: {hosted_url}")
    print("After completing verification, user will be redirected to your return_url")

    # In a real application, you would redirect the user to the hosted_url
    # and wait for them to complete the verification process

    # To simulate a user who completed the verification, we'll check the status
    print("\nChecking verification status (this would typically be done after the user completes the flow)...")

    hosted_status = client.verification_sessions.retrieve(id=hosted_session_id)

    print(hosted_status)

    print("\nHosted verification session example completed!")
    print("\nImplementation steps:")
    print("1. Create the verification session with hosted mode")
    print("2. Redirect the user to the hosted_url")
    print("3. Wait for the user to complete verification and return to your site")
    print("4. Check the verification status using webhooks or API calls")


if __name__ == "__main__":
    main()
