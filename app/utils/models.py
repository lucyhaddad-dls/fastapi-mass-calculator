from pydantic import BaseModel
from enum import Enum
from typing import Optional

class SampleChemistryProps(str, Enum):
    formula = 'formula'
    absorber = 'absorber'
    edge = 'edge'

class SamplePhysicalProps(str, Enum):
    density = "density"
    surface_density = "surface_density"
    mass = "mass"
    area = "area"
    thickness = "thickness"
    mu_total = "mu_total"

class SampleUnitProps(str, Enum):
    mass_unit = "mass_unit"
    length_unit = "length_unit"
    energy_unit = "energy_unit"

class SampleAbsorptionProps(str, Enum):
    mass_absorption= "mass_absorption"
    mass_abs_step = "mass_abs_step"
    mass_abs_max = "mass_abs_max"
    mass_abs_min = "mass_abs_min"

class SampleMeasurement(BaseModel):
    value: Optional[str|list] = None
    name: str

class SampleElementProps(str, Enum):
    Z = "Z"
    A = "A"
    N = "N"
    massFraction = "massFraction"
    mass_absorption = "mass_absorption"