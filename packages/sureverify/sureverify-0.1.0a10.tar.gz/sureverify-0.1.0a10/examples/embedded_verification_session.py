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


def create_embedded_verification_session(client: Verify, resident_id: str) -> VerificationSessionResponse:
    """
    Create an embedded verification session for a resident.

    Args:
        client: The Verify SDK client
        resident_id: ID of the resident to verify

    Returns:
        The created verification session with embedded token
    """
    # Set expiration date to 7 days from now (using timezone-aware datetime)
    expires_at = (datetime.datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    # Create verification session with embedded mode
    attributes: Dict[str, Any] = {
        "expires_at": expires_at,
        "request": {
            "input": {
                "carrier": "Test Insurance",
                "policy_number": "POL123",
                "effective_date": "2024-01-01",
                "expiration_date": "2025-01-01",
                "liability_coverage_amount": "100000",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+14246452600",
                "lease_start_date": "2024-01-01",
                "lease_end_date": "2025-01-01",
            },
            "related_record": {"type": "resident", "id": resident_id},
            "settings": {
                "mode": {"embedded": {"enabled": True}},
                "features": {"upload": {"enabled": True}, "purchase": {"enabled": True}},
            },
        },
    }

    session_data = VerificationSessionRequestDataParam(
        type="VerificationSession",
        attributes=cast(Any, attributes),  # Use cast to bypass type checking
    )

    # Create the verification session
    return client.verification_sessions.create(data=session_data)


def generate_embedded_html(embedded_token: str) -> str:
    """
    Generate HTML code for embedding the verification component.

    Args:
        embedded_token: The embedded token from a verification session

    Returns:
        HTML code for the embedded verification component
    """
    html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Insurance Verification</title>
        <script src="https://cdn.sureverify.com/sdk/v1/verify-sdk.latest.min.js"></script>
        <style>
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .verification-wrapper {{
                height: 600px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Insurance Verification</h1>
            <p>Please complete your insurance verification below:</p>

            <div class="verification-wrapper">
                <verify-verification embedded-token="{embedded_token}"></verify-verification>
            </div>
        </div>
    </body>
</html>
"""
    return html


def check_verification_status(client: Verify, session_id: str) -> Any:
    """
    Check the status of a verification session.

    Args:
        client: The Verify SDK client
        session_id: ID of the verification session

    Returns:
        The verification session with status information
    """
    # Get the verification session
    session_response: Any = client.verification_sessions.retrieve(id=session_id)
    return session_response


def main() -> None:
    """Example workflow for using embedded verification sessions."""

    # Initialize the client
    client = init_client()

    residents = client.residents.list()
    resident_id = residents.data[0].id

    # Create an embedded verification session
    print("\nCreating an embedded verification session...")
    embedded_session = create_embedded_verification_session(client, resident_id)
    embedded_session_id = embedded_session.data.id

    if not embedded_session.data or not embedded_session.data.attributes:
        raise ValueError("Failed to create embedded verification session")

    embedded_token = embedded_session.data.attributes.embedded_token

    if not embedded_token:
        raise ValueError("Failed to create embedded token")

    print(f"Embedded session created with ID: {embedded_session_id}")
    print(f"Embedded token: {embedded_token}")

    # Generate HTML for embedding
    embedded_html = generate_embedded_html(embedded_token)

    # Save the HTML to a file for demonstration purposes
    with open("embedded_verification.html", "w") as f:
        f.write(embedded_html)
    print("Generated HTML file 'embedded_verification.html' with the embedded component")

    # In a real application, you would serve this HTML to the user
    # or include the verification component in your existing web pages

    # To simulate a user who completed the verification, we'll check the status
    print("\nChecking verification status (this would typically be done after the user completes the flow)...")

    embedded_status = check_verification_status(client, embedded_session_id)

    print(embedded_status)

    print("\nEmbedded verification session example completed!")
    print("\nImplementation steps:")
    print("1. Create the verification session with embedded mode")
    print("2. Include the Verify SDK script in your HTML")
    print("3. Add the verification component to your page with the embedded token")
    print("4. Check the verification status using webhooks or API calls")


if __name__ == "__main__":
    main()
