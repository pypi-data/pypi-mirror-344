import time
from typing import Any, Dict, Union

import jwt
import pytest

from sureverify.lib.auth import generate_jwt_bearer_token


@pytest.fixture
def mock_private_key() -> bytes:
    """Provide a test RSA private key."""
    return b"""-----BEGIN PRIVATE KEY-----
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
nlJNNZfoM1759fSH/YWTtzVN5S3hhg==
-----END PRIVATE KEY-----
"""


@pytest.fixture
def valid_token_params() -> Dict[str, Any]:
    return {
        "key_id": "test-key-id",
        "user_id": "test-user-id",
        "issuer": "TEST_ORG",
        "ttl_seconds": 3600,  # 1 hour
    }


def test_generate_jwt_bearer_token_success(mock_private_key: bytes, valid_token_params: Dict[str, Any]) -> None:
    """Test successful JWT token generation with valid parameters."""
    token = generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **valid_token_params)

    # Verify token is a string
    assert isinstance(token, str)

    # Decode the token to verify its contents
    decoded = jwt.decode(
        token,
        options={"verify_signature": False},  # Skip signature verification for testing
    )

    # Verify claims
    assert decoded["iss"] == valid_token_params["issuer"]
    assert decoded["sub"] == valid_token_params["user_id"]

    # Verify expiration
    now = int(time.time())
    assert decoded["iat"] <= now
    assert decoded["exp"] > now
    assert decoded["exp"] - decoded["iat"] == valid_token_params["ttl_seconds"]

    # Verify JWT ID exists
    assert "jti" in decoded

    # Verify headers
    headers = jwt.get_unverified_header(token)
    assert headers["typ"] == "JWT"
    assert headers["kid"] == valid_token_params["key_id"]
    assert headers["alg"] == "RS256"


def test_private_key_as_string(mock_private_key: bytes, valid_token_params: Dict[str, Any]) -> None:
    """Test that the private key works as a string."""
    # Convert bytes to string
    private_key_str: str = mock_private_key.decode("utf-8")

    token = generate_jwt_bearer_token(private_key_pem_format=private_key_str, **valid_token_params)
    assert isinstance(token, str)


def test_private_key_as_bytes(mock_private_key: bytes, valid_token_params: Dict[str, Any]) -> None:
    """Test that the private key works as bytes."""
    # Already bytes, no conversion needed
    token = generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **valid_token_params)
    assert isinstance(token, str)


def test_token_expiration(mock_private_key: bytes, valid_token_params: Dict[str, Any]) -> None:
    """Test token expiration timing is correct."""
    # Test with different TTL values
    test_ttl = 7200  # 2 hours

    params = valid_token_params.copy()
    params["ttl_seconds"] = test_ttl
    token = generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **params)

    decoded = jwt.decode(token, options={"verify_signature": False})

    assert decoded["exp"] - decoded["iat"] == test_ttl


@pytest.mark.parametrize("key_id", ["", None, 123])
def test_invalid_key_id(
    mock_private_key: bytes, valid_token_params: Dict[str, Any], key_id: Union[str, None, int]
) -> None:
    """Test that invalid key_id values raise ValueError."""
    params = valid_token_params.copy()
    params["key_id"] = key_id

    with pytest.raises(ValueError, match="Key ID cannot be empty and must be a string"):
        generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **params)


@pytest.mark.parametrize("user_id", ["", None, 123])
def test_invalid_user_id(
    mock_private_key: bytes, valid_token_params: Dict[str, Any], user_id: Union[str, None, int]
) -> None:
    """Test that invalid user_id values raise ValueError."""
    params = valid_token_params.copy()
    params["user_id"] = user_id

    with pytest.raises(ValueError, match="User ID cannot be empty and must be a string"):
        generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **params)


@pytest.mark.parametrize("issuer", ["", None, 123])
def test_invalid_issuer(
    mock_private_key: bytes, valid_token_params: Dict[str, Any], issuer: Union[str, None, int]
) -> None:
    """Test that invalid issuer values raise ValueError."""
    params = valid_token_params.copy()
    params["issuer"] = issuer

    with pytest.raises(ValueError, match="Issuer cannot be empty and must be a string"):
        generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **params)


@pytest.mark.parametrize(
    "ttl_seconds",
    [
        None,  # None type
        "3600",  # String instead of int
        59 * 60,  # Below minimum (1 hour)
        13 * 60 * 60,  # Above maximum (12 hours)
    ],
)
def test_invalid_ttl(
    mock_private_key: bytes, valid_token_params: Dict[str, Any], ttl_seconds: Union[int, str, None]
) -> None:
    """Test that invalid TTL values raise ValueError."""
    params = valid_token_params.copy()
    params["ttl_seconds"] = ttl_seconds

    with pytest.raises(ValueError, match="TTL must be between"):
        generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **params)


@pytest.mark.parametrize("private_key", [None, "", 123, []])
def test_invalid_private_key(valid_token_params: Dict[str, Any], private_key: Any) -> None:
    """Test that invalid private key values raise ValueError."""
    with pytest.raises(ValueError):
        generate_jwt_bearer_token(private_key_pem_format=private_key, **valid_token_params)


def test_unique_jwt_id(mock_private_key: bytes, valid_token_params: Dict[str, Any]) -> None:
    """Test that each generated token has a unique JWT ID."""
    token1 = generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **valid_token_params)

    token2 = generate_jwt_bearer_token(private_key_pem_format=mock_private_key, **valid_token_params)

    decoded1 = jwt.decode(token1, options={"verify_signature": False})

    decoded2 = jwt.decode(token2, options={"verify_signature": False})

    # JWT IDs should be different for each token
    assert decoded1["jti"] != decoded2["jti"]
