# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Address", "Attributes"]


class Attributes(BaseModel):
    city: Optional[str] = None

    created_at: Optional[datetime] = None

    line1: Optional[str] = None

    line2: Optional[str] = None

    postal: Optional[str] = None

    state_code: Optional[
        Literal[
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "DC",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
            "",
        ]
    ] = None
    """
    - `AL` - Alabama
    - `AK` - Alaska
    - `AZ` - Arizona
    - `AR` - Arkansas
    - `CA` - California
    - `CO` - Colorado
    - `CT` - Connecticut
    - `DE` - Delaware
    - `DC` - District of Columbia
    - `FL` - Florida
    - `GA` - Georgia
    - `HI` - Hawaii
    - `ID` - Idaho
    - `IL` - Illinois
    - `IN` - Indiana
    - `IA` - Iowa
    - `KS` - Kansas
    - `KY` - Kentucky
    - `LA` - Louisiana
    - `ME` - Maine
    - `MD` - Maryland
    - `MA` - Massachusetts
    - `MI` - Michigan
    - `MN` - Minnesota
    - `MS` - Mississippi
    - `MO` - Missouri
    - `MT` - Montana
    - `NE` - Nebraska
    - `NV` - Nevada
    - `NH` - New Hampshire
    - `NJ` - New Jersey
    - `NM` - New Mexico
    - `NY` - New York
    - `NC` - North Carolina
    - `ND` - North Dakota
    - `OH` - Ohio
    - `OK` - Oklahoma
    - `OR` - Oregon
    - `PA` - Pennsylvania
    - `RI` - Rhode Island
    - `SC` - South Carolina
    - `SD` - South Dakota
    - `TN` - Tennessee
    - `TX` - Texas
    - `UT` - Utah
    - `VT` - Vermont
    - `VA` - Virginia
    - `WA` - Washington
    - `WV` - West Virginia
    - `WI` - Wisconsin
    - `WY` - Wyoming
    """

    updated_at: Optional[datetime] = None


class Address(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Optional[Attributes] = None
