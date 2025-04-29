import os
from typing import Any, List

from sureverify import Verify
from sureverify.lib.auth import generate_jwt_bearer_token
from sureverify.types.unit_request_data_param import UnitRequestDataParam
from sureverify.types.address_request_data_param import AddressRequestDataParam
from sureverify.types.resident_request_data_param import ResidentRequestDataParam
from sureverify.types.community_request_data_param import CommunityRequestDataParam
from sureverify.types.property_manager_request_data_param import PropertyManagerRequestDataParam
from sureverify.types.verification_portal_request_data_param import VerificationPortalRequestDataParam


def main() -> None:
    """Example workflow for community data setup using the Verify SDK."""
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
        key_id=key_id, user_id=user_id, private_key_pem_format=private_key, issuer=issuer
    )

    # Initialize client with generated token
    client: Verify = Verify(bearer_token=bearer_token, base_url="http://host.docker.internal:8000")

    # Step 1: Create or retrieve a Property Manager
    property_manager_name = "Parkside Properties"

    # Check if the property manager exists by listing and filtering
    property_managers = client.property_managers.list()
    property_manager: Any = None

    for pm in property_managers.data:
        if getattr(pm, "name", "") == property_manager_name:
            property_manager = pm
            print(f"Found existing property manager: {property_manager_name}")
            break

    if not property_manager:
        # Create a new property manager
        property_manager_data = PropertyManagerRequestDataParam(
            type="PropertyManager",
            attributes={
                "name": property_manager_name,
                "contact_email_address": "contact@parksideproperties.com",
                "contact_phone_number": "4246402000",
            },
        )
        property_manager = client.property_managers.create(data=property_manager_data)
        print(f"Created new property manager: {property_manager_name}")

        # Step 2: Create a Verification Portal
        verification_portal_data = VerificationPortalRequestDataParam(
            type="VerificationPortal",
            attributes={
                "title": "Parkside",
            },
            relationships={"property_manager": {"data": {"id": property_manager.data.id, "type": "PropertyManager"}}},
        )
        verification_portal = client.verification_portals.create(data=verification_portal_data)
        print(f"Created new verification portal: {verification_portal.data.id}")

    property_manager_id: str = property_manager.data.id
    print(f"Property Manager ID: {property_manager_id}")

    # Step 2: Create an Address for the Community
    address_data = AddressRequestDataParam(
        type="Address",
        attributes={"line1": "123 Main Street", "city": "San Francisco", "state_code": "CA", "postal": "94105"},
    )
    address: Any = client.addresses.create(data=address_data)
    address_id: str = address.data.id
    print(f"Created address with ID: {address_id}")

    # Step 3: Create a Community
    community_name = "Parkside Heights"
    community_data = CommunityRequestDataParam(
        type="Community",
        attributes={"name": community_name},
        relationships={
            "property_manager": {"data": {"id": property_manager_id, "type": "PropertyManager"}},
            "address": {"data": {"id": address_id, "type": "Address"}},
        },
    )
    community: Any = client.communities.create(data=community_data)
    community_id: str = community.data.id
    print(f"Created community '{community_name}' with ID: {community_id}")

    # Step 4: Create Units in the Community
    unit_numbers = ["101", "102", "103", "201", "202", "203"]
    unit_ids: List[str] = []

    for unit_number in unit_numbers:
        unit_data = UnitRequestDataParam(
            type="Unit",
            attributes={"unit_number": unit_number},
            relationships={"community": {"data": {"id": community_id, "type": "Community"}}},
        )
        unit: Any = client.units.create(data=unit_data)
        unit_id: str = unit.data.id
        unit_ids.append(unit_id)
        print(f"Created unit {unit_number} with ID: {unit_id}")

    # Step 5: Create Residents
    residents_data = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "4246402000",
            "unit_id": unit_ids[0],
            "lease_start": "2023-01-01",
            "lease_end": "2024-01-01",
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "4246402000",
            "unit_id": unit_ids[1],
            "lease_start": "2023-02-15",
            "lease_end": "2024-02-15",
        },
    ]

    for res_data in residents_data:
        resident_data = ResidentRequestDataParam(
            type="Resident",
            attributes={
                "first_name": res_data["first_name"],
                "last_name": res_data["last_name"],
                "email": res_data["email"],
                "phone_number": res_data["phone"],
                "lease_start_date": res_data["lease_start"],
                "lease_end_date": res_data["lease_end"],
            },
            relationships={
                "community": {"data": {"id": community_id, "type": "Community"}},
                "unit": {"data": {"id": res_data["unit_id"], "type": "Unit"}},
            },
        )
        resident: Any = client.residents.create(data=resident_data)
        resident_id: str = resident.data.id
        print(f"Created resident {res_data['first_name']} {res_data['last_name']} with ID: {resident_id}")

    print("\nCommunity data setup completed successfully!")


if __name__ == "__main__":
    main()
