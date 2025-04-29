import os
import time
import base64

from sureverify import Verify
from sureverify.types import (
    VerificationCaseRequestDataParam,
    PresignedAttachmentRequestDataParam,
    VerificationCaseInputRequestDataParam,
)
from sureverify.lib.auth import generate_jwt_bearer_token
from sureverify.lib.file_upload import upload_file_to_presigned_url


def main() -> None:
    """Example workflow for advanced verification case management using the Verify SDK.

    This example demonstrates:
    1. Creating a verification case
    2. Adding structured verification input
    3. Uploading insurance documents
    4. Processing the verification
    5. Retrieving verification results
    6. Managing the verification lifecycle
    """
    # Step 0: Initialize the client with authentication using JWT token generation

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
        key_id=key_id,
        user_id=user_id,
        private_key_pem_format=private_key,
        issuer=issuer,
    )

    # Initialize client with generated token
    client: Verify = Verify(bearer_token=bearer_token, base_url="http://host.docker.internal:8000")

    # Get existing property manager, resident, community, and unit

    residents = client.residents.list()
    if not residents.data:
        raise ValueError("No residents found. Please run the community_data_setup.py example first.")

    resident = residents.data[0]

    if (
        not resident.relationships
        or not resident.relationships.community
        or not resident.relationships.unit
        or not resident.relationships.community.data
        or not resident.relationships.unit.data
    ):
        raise ValueError("Resident relationships not found")

    community_id = resident.relationships.community.data.id
    unit_id = resident.relationships.unit.data.id
    resident_id = resident.id
    community = client.communities.retrieve(id=community_id)

    if (
        not community.data.relationships
        or not community.data.relationships.property_manager
        or not community.data.relationships.property_manager.data
    ):
        raise ValueError("Community relationships not found")

    property_manager_id = community.data.relationships.property_manager.data.id

    print(f"Using community ID: {community_id}")
    print(f"Using unit ID: {unit_id}")
    print(f"Using resident ID: {resident_id}")

    # Step 1: Create a Verification Case
    due_date = "2023-12-31"  # Set appropriate due date

    verification_case_data = VerificationCaseRequestDataParam(
        type="VerificationCase",
        attributes={
            "due_at": due_date,
            "notes": "Example verification case created via SDK",
        },
        relationships={
            "property_manager": {"data": {"id": property_manager_id, "type": "PropertyManager"}},
            "resident": {"data": {"id": resident_id, "type": "Resident"}},
            "community": {"data": {"id": community_id, "type": "Community"}},
            "unit": {"data": {"id": unit_id, "type": "Unit"}},
        },
    )

    verification_case = client.verification_cases.create(data=verification_case_data)
    case_id = verification_case.data.id
    print(f"Created verification case with ID: {case_id}")

    # Step 2: Create Verification Input (structured policy information)
    verification_input_data = VerificationCaseInputRequestDataParam(
        type="VerificationCaseInput",
        attributes={
            "policy_number": "HO3-1234567",
            "carrier": "State Farm",
            "effective_date": "2023-01-01",
            "expiration_date": "2024-01-01",
            "liability_coverage_amount": "300000",
            "first_name": "John",
            "last_name": "Doe",
        },
        relationships={"case": {"data": {"id": case_id, "type": "VerificationCase"}}},
    )

    verification_input = client.verification_case_inputs.create(data=verification_input_data)
    input_id = verification_input.data.id
    print(f"Created verification input with ID: {input_id}")

    # Step 3: Upload insurance documents (this is a two-step process)

    # Step 3a: Create an attachment record
    attachment_data = PresignedAttachmentRequestDataParam(
        type="Attachment",
        attributes={
            "name": "insurance_certificate.pdf",
            "content_type": "application/pdf",
        },
    )

    attachment = client.attachments.create(data=attachment_data)
    attachment_id = attachment.data.id
    if not attachment.data.attributes or not attachment.data.attributes.presigned_upload_url:
        raise ValueError("Presigned upload URL not found in attachment")

    presigned_upload_url = attachment.data.attributes.presigned_upload_url

    print(f"Created attachment with ID: {attachment_id}")
    print(f"Received presigned upload URL: {presigned_upload_url}")

    # Step 3b: Upload the file to the presigned URL
    # Here we're just uploading a sample PDF file using the upload url
    # In a real application, you would use this URL to upload the actual file
    PDF_SAMPLE = b"JVBERi0xLjEKJcKlwrHDqwoKMSAwIG9iagogIDw8IC9UeXBlIC9DYXRhbG9nCiAgICAgL1BhZ2VzIDIgMCBSCiAgPj4KZW5kb2JqCgoyIDAgb2JqCiAgPDwgL1R5cGUgL1BhZ2VzCiAgICAgL0tpZHMgWzMgMCBSXQogICAgIC9Db3VudCAxCiAgICAgL01lZGlhQm94IFswIDAgMzAwIDE0NF0KICA+PgplbmRvYmoKCjMgMCBvYmoKICA8PCAgL1R5cGUgL1BhZ2UKICAgICAgL1BhcmVudCAyIDAgUgogICAgICAvUmVzb3VyY2VzCiAgICAgICA8PCAvRm9udAogICAgICAgICAgIDw8IC9GMQogICAgICAgICAgICAgICA8PCAvVHlwZSAvRm9udAogICAgICAgICAgICAgICAgICAvU3VidHlwZSAvVHlwZTEKICAgICAgICAgICAgICAgICAgL0Jhc2VGb250IC9UaW1lcy1Sb21hbgogICAgICAgICAgICAgICA+PgogICAgICAgICAgID4+CiAgICAgICA+PgogICAgICAvQ29udGVudHMgNCAwIFIKICA+PgplbmRvYmoKCjQgMCBvYmoKICA8PCAvTGVuZ3RoIDU1ID4+CnN0cmVhbQogIEJUCiAgICAvRjEgMTggVGYKICAgIDAgMCBUZAogICAgKERlbW8vVGVzdCBQREYpIFRqCiAgRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDUKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDE4IDAwMDAwIG4gCjAwMDAwMDAwNzcgMDAwMDAgbiAKMDAwMDAwMDE3OCAwMDAwMCBuIAowMDAwMDAwNDU3IDAwMDAwIG4gCnRyYWlsZXIKICA8PCAgL1Jvb3QgMSAwIFIKICAgICAgL1NpemUgNQogID4+CnN0YXJ0eHJlZgo1NjUKJSVFT0YK"
    file_content = base64.b64decode(PDF_SAMPLE)

    upload_file_to_presigned_url(
        presigned_upload_url=presigned_upload_url, file_content=file_content, content_type="application/pdf"
    )

    # Step 4: Process the verification

    client.verification_cases.enqueue_processing(id=case_id)
    print("Verification case enqueued for processing")

    # Step 5: Retrieve verification results (normally you would use webhooks)
    # For this example, we'll poll the case status a few times
    # In a real application, you would use webhooks instead of polling
    print("Waiting for verification processing to complete...")
    for _ in range(3):
        time.sleep(60)  # Wait a minute between checks
        case = client.verification_cases.retrieve(id=case_id)
        if not case.data.attributes:
            raise ValueError("Verification case attributes not found")

        status = case.data.attributes.status

        print(f"Current status: {status}")

        # Check if verification is complete
        if status in ["completed", "failed"]:
            break

    # Step 6: Get final verification results
    case = client.verification_cases.retrieve(id=case_id)

    if not case.data.attributes:
        raise ValueError("Verification case attributes not found")

    status = case.data.attributes.status
    decision = case.data.attributes.decision
    decision_reason = case.data.attributes.decision_reason

    print("\nVerification Results:")
    print(f"Status: {status}")
    print(f"Decision: {decision}")
    print(f"Decision Reason: {decision_reason}")

    print("\nAdvanced verification workflow completed!")


if __name__ == "__main__":
    main()
