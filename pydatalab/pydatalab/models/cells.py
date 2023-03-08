from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, validator

from pydatalab.models.entries import EntryReference
from pydatalab.models.items import Item
from pydatalab.models.samples import Constituent

# from pydatalab.logger import LOGGER


class CellFormat(str, Enum):

    coin = "coin"
    pouch = "pouch"
    in_situ_xrd = "in situ (XRD)"
    in_situ_nmr = "in situ (NMR)"
    in_situ_squid = "in situ (SQUID)"
    swagelok = "swagelok"
    cylindrical = "cylindrical"
    other = "other"


class InlineSubstance(BaseModel):
    name: str
    formula: str


class CellComponent(Constituent):
    """A constituent of a sample."""

    item: Union[EntryReference, InlineSubstance] = Field(...)
    """A reference to item (sample or starting material) entry for the constituent substance."""


class Cell(Item):
    """A model for representing electrochemical cells."""

    type: str = Field("cells", const="cells", pattern="^cells$")

    cell_format: Optional[CellFormat] = Field(
        description="The form factor of the cell, e.g., coin, pouch, in situ or otherwise.",
    )

    cell_format_description: Optional[str] = Field(
        description="Additional human-readable description of the cell form factor, e.g., 18650, AMPIX, CAMPIX"
    )

    cell_preparation_description: Optional[str] = Field()

    characteristic_mass: Optional[float] = Field(
        description="The characteristic mass of the cell in milligrams. Can be used to normalize capacities."
    )

    characteristic_chemical_formula: Optional[str] = Field(
        description="The chemical formula of the active material. Can be used to calculated molar mass in g/mol for normalizing capacities."
    )

    characteristic_molar_mass: Optional[float] = Field(
        description="The molar mass of the active material, in g/mol. Will be inferred from the chemical formula, or can be supplied if it cannot be supplied"
    )

    positive_electrode: List[CellComponent] = Field([])

    negative_electrode: List[CellComponent] = Field([])

    electrolyte: List[CellComponent] = Field([])

    active_ion_charge: float = Field(1)

    @validator("cell_format", "cell_format_description")
    def check_descriptions_for_ambiguous_formats(cls, v, values):
        if (
            values.get("cell_format") == CellFormat.other
            and values.get("cell_format_description") is None
        ):
            raise ValueError("cell_format_description must be set if cell_format is 'other'")

        return v

    @validator("characteristic_molar_mass", always=True, pre=True)
    def set_molar_mass(cls, v, values):
        from periodictable import formula

        if not v:
            chemical_formula = values.get("characteristic_chemical_formula")

            if chemical_formula:
                try:
                    return formula(chemical_formula).mass
                except Exception:
                    return None

        return v