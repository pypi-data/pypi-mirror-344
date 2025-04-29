import time
import uuid
from typing import Union

import jwt


def generate_jwt_bearer_token(
    key_id: str,
    user_id: str,
    private_key_pem_format: Union[str, bytes],
    issuer: str,
    ttl_seconds: int = 36000,
) -> str:
    """
    Generate a secure JWT token signed with your private key for authenticating with the Verify API.

    This function creates a JWT token with required headers and claims as specified in the Verify API
    documentation. The token is signed using the RS256 algorithm with your private key. The Verify API
    will validate the token's signature using your registered public key.

    Before using this function, you need to:
        1. Generate a public/private key pair
        2. Register your public key with Verify
        3. Obtain your key ID and user ID

        For detailed instructions on generating keys, registering your public key, and obtaining
        your key ID and user ID, please refer to the official documentation:
        https://www.sureverify.com/docs/using-the-api/authentication

    We recommend that you cache the token on your end and reuse it for multiple requests during its TTL
    period rather than generating a new token for each request.

    Args:
        key_id: The key ID (kid) provided when you registered your public key with Verify
        user_id: Your user ID in the Verify system, used as the 'sub' claim
        private_key_pem_format: Your private key in PEM format as a string or bytes
        issuer: Short name of your organization to identify the token issuer
        ttl_seconds: Token time-to-live in seconds (default: 10 hours, recommended between 1-12 hours)

    Returns:
        A signed JWT token as a string to be used in the Authorization header

    Raises:
        ValueError: If any required parameters are missing or invalid

    Example:
        >>> with open("private.pem", "rb") as key_file:
        ...     private_key = key_file.read()
        >>> bearer_token = generate_jwt_bearer_token(
        ...     key_id="your-key-id", user_id="your-user-id", private_key_pem_format=private_key, issuer="YOUR_ORG_NAME"
        ... )
        >>> client = Verify(bearer_token=bearer_token)
        >>> page = client.addresses.list()
        >>> print(page.data)
    """
    # Input validation
    if not key_id or not isinstance(key_id, str):  # pyright: ignore
        raise ValueError("Key ID cannot be empty and must be a string")

    if not user_id or not isinstance(user_id, str):  # pyright: ignore
        raise ValueError("User ID cannot be empty and must be a string")

    if not issuer or not isinstance(issuer, str):  # pyright: ignore
        raise ValueError("Issuer cannot be empty and must be a string")

    # The API recommends tokens between 60 minutes and 12 hours
    min_ttl = 60 * 60  # 1 hour in seconds
    max_ttl = 60 * 60 * 12  # 12 hours in seconds
    if not isinstance(ttl_seconds, int) or not (min_ttl <= ttl_seconds <= max_ttl):  # pyright: ignore
        raise ValueError(f"TTL must be between {min_ttl} seconds (1 hour) and {max_ttl} seconds (12 hours)")

    if not private_key_pem_format:
        raise ValueError("Private key cannot be empty")

    # Convert string private key to bytes if needed
    if isinstance(private_key_pem_format, str):
        private_key_pem_format = private_key_pem_format.encode("utf-8")
    elif not isinstance(private_key_pem_format, bytes):  # pyright: ignore
        raise ValueError("Private key must be a string or bytes")

    # Get current timestamp
    issued_at = int(time.time())

    # Define standard claims as required by Verify API
    claims = {
        "iss": issuer,  # Issuer (organization name)
        "iat": issued_at,  # Issued at time
        "jti": str(uuid.uuid4()),  # JWT ID (unique identifier to prevent token reuse)
        "sub": user_id,  # Subject (your user ID in the Verify system)
        "exp": issued_at + ttl_seconds,  # Expiration time
    }

    # JWT headers including key ID (kid) for public key identification
    headers = {
        "typ": "JWT",
        "kid": key_id,
    }

    # Encode and sign the token with RS256 algorithm
    return jwt.encode(
        payload=claims,
        key=private_key_pem_format,
        algorithm="RS256",  # RSA with SHA-256 as required by Verify API
        headers=headers,
    )
