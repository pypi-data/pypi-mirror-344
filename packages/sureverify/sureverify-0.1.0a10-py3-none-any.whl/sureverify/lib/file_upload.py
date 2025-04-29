from typing import Union, BinaryIO

import httpx


def upload_file_to_presigned_url(
    presigned_upload_url: str,
    file_content: Union[bytes, BinaryIO],
    content_type: str,
) -> httpx.Response:
    """
    Upload a file to a presigned URL using httpx.

    This function uploads file contents to the provided presigned URL using a PUT request.
    Presigned URLs are commonly used for secure, temporary access to upload files to
    cloud storage services like AWS S3 or Google Cloud Storage.

    Args:
        presigned_upload_url: The presigned URL where the file should be uploaded
        file_content: The file content as bytes or a file-like object (open in binary mode)
        content_type: The MIME type of the file being uploaded (e.g., "application/pdf", "image/jpeg")

    Returns:
        httpx.Response: The response from the PUT request

    Raises:
        ValueError: If any required parameters are missing or invalid
        httpx.HTTPError: If there's an HTTP-related error during the upload

    Example:
        >>> # Using bytes
        >>> with open("path/to/insurance_certificate.pdf", "rb") as f:
        ...     file_bytes = f.read()
        >>> response = upload_file_to_presigned_url(
        ...     presigned_upload_url="https://bucket.s3.amazonaws.com/path/to/file?signature=...",
        ...     file_content=file_bytes,
        ...     content_type="application/pdf",
        ... )
        >>> print(f"Upload successful with status code: {response.status_code}")
        >>>
        >>> # Or using a file object directly
        >>> with open("path/to/insurance_certificate.pdf", "rb") as f:
        ...     response = upload_file_to_presigned_url(
        ...         presigned_upload_url="https://bucket.s3.amazonaws.com/path/to/file?signature=...",
        ...         file_content=f,
        ...         content_type="application/pdf",
        ...     )
        >>> # The function will raise an exception if the upload fails
        >>> # Otherwise, you can access the response properties:
        >>> print(f"Response headers: {response.headers}")
    """
    # Input validation
    if not presigned_upload_url:
        raise ValueError("Presigned upload URL cannot be empty and must be a string")

    if not content_type:
        raise ValueError("Content type cannot be empty")

    # Prepare the content based on the input type
    content: bytes

    if isinstance(file_content, bytes):
        content = file_content
    elif hasattr(file_content, "read"):
        # If it's a file-like object, read its contents
        content = file_content.read()
    else:
        raise ValueError("File content must be either bytes or a file-like object with a read method")

    # Upload the file using httpx
    response = httpx.put(presigned_upload_url, content=content, headers={"Content-Type": content_type})

    response.raise_for_status()

    return response
