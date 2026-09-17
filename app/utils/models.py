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

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "value": "FeS",
                "name": "formula"
            }, {
                "value": "10.2",
                "name": "density"
            }]
        }
    }

class SampleElementProps(str, Enum):
    Z = "Z"
    A = "A"
    N = "N"
    massFraction = "massFraction"
    mass_absorption = "mass_absorption"

class SampleInputData(BaseModel):
    input_data: list[SampleMeasurement]  = [{"name": f,
                                            "value": None}
                    for f in 
                   [ SampleChemistryProps._member_names_ 
                    + SamplePhysicalProps._member_names_ +
                    SampleUnitProps._member_names_]]
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "input_data":
                    [
                    {"name":"formula" ,"value":"FeS"},
                    {"name":"edge" , "value":"K"},
                    {"name":"absorber", "value":"Fe"},
                    {"name": "density", "value":"None"},
                    {"name": "surface_density", "value":"None"},
                    {"name": "mass", "value":"None"},
                    {"name": "area", "value":"None"},
                    {"name": "thickness", "value":"None"},
                    {"name": "mu_total", "value":"2.6"},
                    {"name": "mass_unit", "value":"g"},
                    {"name": "energy_unit", "value":"eV"},
                    {"name": "length_unit", "value":"cm"} 
                    ]
            }
        
            ]
        }
    }
        

    