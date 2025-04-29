# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AddressRequestDataParam", "Attributes"]


class Attributes(TypedDict, total=False):
    city: Optional[str]

    line1: Optional[str]

    line2: Optional[str]

    postal: Optional[str]

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
    ]
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


class AddressRequestDataParam(TypedDict, total=False):
    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Attributes
