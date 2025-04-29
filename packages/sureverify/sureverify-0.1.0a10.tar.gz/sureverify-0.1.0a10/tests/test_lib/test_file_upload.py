import io
from typing import Any, Dict, BinaryIO
from unittest.mock import patch

import httpx
import pytest

from sureverify.lib.file_upload import upload_file_to_presigned_url


@pytest.fixture
def mock_file_content() -> bytes:
    """Provide test file content as bytes."""
    return b"This is test file content"


@pytest.fixture
def mock_file_object(mock_file_content: bytes) -> BinaryIO:
    """Provide a file-like object with test content."""
    return io.BytesIO(mock_file_content)


@pytest.fixture
def valid_upload_params() -> Dict[str, Any]:
    """Provide valid parameters for the upload function."""
    return {
        "presigned_upload_url": "https://bucket.s3.amazonaws.com/path/to/file?signature=abc123",
        "content_type": "application/pdf",
    }


@pytest.fixture
def mock_response(valid_upload_params: Dict[str, Any]) -> httpx.Response:
    """Create a mock successful httpx response with a request attached."""
    url = valid_upload_params["presigned_upload_url"]
    mock_request = httpx.Request("PUT", url)
    mock = httpx.Response(200, request=mock_request)
    return mock


def test_upload_with_bytes_success(
    mock_file_content: bytes, valid_upload_params: Dict[str, Any], mock_response: httpx.Response
) -> None:
    """Test successful upload using bytes content."""
    with patch("httpx.put", return_value=mock_response) as mock_put:
        response = upload_file_to_presigned_url(file_content=mock_file_content, **valid_upload_params)

        # Verify httpx.put was called with the right arguments
        mock_put.assert_called_once_with(
            valid_upload_params["presigned_upload_url"],
            content=mock_file_content,
            headers={"Content-Type": valid_upload_params["content_type"]},
        )

        # Verify response is returned correctly
        assert response == mock_response


def test_upload_with_file_object_success(
    mock_file_object: BinaryIO,
    mock_file_content: bytes,
    valid_upload_params: Dict[str, Any],
    mock_response: httpx.Response,
) -> None:
    """Test successful upload using a file-like object."""
    with patch("httpx.put", return_value=mock_response) as mock_put:
        response = upload_file_to_presigned_url(file_content=mock_file_object, **valid_upload_params)

        # Verify httpx.put was called with the right arguments
        mock_put.assert_called_once_with(
            valid_upload_params["presigned_upload_url"],
            content=mock_file_content,
            headers={"Content-Type": valid_upload_params["content_type"]},
        )

        # Verify response is returned correctly
        assert response == mock_response


def test_upload_http_error(mock_file_content: bytes, valid_upload_params: Dict[str, Any]) -> None:
    """Test that HTTP errors are properly raised."""
    # Create a response that will raise an HTTPStatusError when raise_for_status is called
    error_response = httpx.Response(400, request=httpx.Request("PUT", "https://example.com"))

    with patch("httpx.put", return_value=error_response):
        with pytest.raises(httpx.HTTPStatusError):
            upload_file_to_presigned_url(file_content=mock_file_content, **valid_upload_params)


def test_upload_connection_error(mock_file_content: bytes, valid_upload_params: Dict[str, Any]) -> None:
    """Test that connection errors are properly raised."""
    with patch("httpx.put", side_effect=httpx.ConnectError("Connection failed")):
        with pytest.raises(httpx.ConnectError):
            upload_file_to_presigned_url(file_content=mock_file_content, **valid_upload_params)


@pytest.mark.parametrize("url", ["", None])
def test_invalid_url(mock_file_content: bytes, valid_upload_params: Dict[str, Any], url: Any) -> None:
    """Test that invalid URL values raise ValueError."""
    params = valid_upload_params.copy()
    params["presigned_upload_url"] = url

    with pytest.raises(ValueError, match="Presigned upload URL cannot be empty"):
        upload_file_to_presigned_url(file_content=mock_file_content, **params)


@pytest.mark.parametrize("content_type", ["", None])
def test_invalid_content_type(mock_file_content: bytes, valid_upload_params: Dict[str, Any], content_type: Any) -> None:
    """Test that invalid content type values raise ValueError."""
    params = valid_upload_params.copy()
    params["content_type"] = content_type

    with pytest.raises(ValueError, match="Content type cannot be empty"):
        upload_file_to_presigned_url(file_content=mock_file_content, **params)


def test_invalid_file_content(valid_upload_params: Dict[str, Any]) -> None:
    """Test that invalid file content raises ValueError."""
    # Use Any to bypass type checking for this test
    invalid_content: Any = "not bytes or file-like"

    with pytest.raises(ValueError, match="File content must be either bytes or a file-like object"):
        upload_file_to_presigned_url(file_content=invalid_content, **valid_upload_params)


def test_headers_correctly_set(mock_file_content: bytes, valid_upload_params: Dict[str, Any]) -> None:
    """Test that headers are correctly set in the request."""
    custom_content_type = "application/custom+json"
    params = valid_upload_params.copy()
    params["content_type"] = custom_content_type

    # Create a mock response with a request
    url = params["presigned_upload_url"]
    mock_request = httpx.Request("PUT", url)
    mock_response = httpx.Response(200, request=mock_request)

    with patch("httpx.put") as mock_put:
        mock_put.return_value = mock_response
        upload_file_to_presigned_url(file_content=mock_file_content, **params)

        # Verify Content-Type header is set correctly
        called_kwargs = mock_put.call_args[1]
        assert called_kwargs["headers"]["Content-Type"] == custom_content_type
