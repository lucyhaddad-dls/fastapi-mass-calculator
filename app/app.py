from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.calculate import (input_data, update_input_data_from_key, calculate_thickness,
                            calculate_mass,
                            AMeasurement, get_input_data_from_key,
                            make_XRaySample, get_absorption_data_all_elements)
from .utils.sample_builder import formula_from_mass_ratios
from typing import Literal

app = FastAPI()

origins = ["http://localhost:5173",
           "localhost:5173"]

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                )


@app.get("/api", tags=["root"])
async def read_root() -> dict:
    return {"message": "MASS CALCULATOR!!!"}


@app.get("/api/input", tags=["input"])
async def get_data()->list[AMeasurement]:
    """
    Return full `input_data`
    """
    return input_data

@app.post("/api/input", tags=["input"])
async def change_value(name:str, value:str)->list[AMeasurement]:
    """
    Change a single value in `input_data`.

    Arguments:
        name (str): Name of value.
        value (str): Value to change it to.

    """
    update_input_data_from_key(name, value)
    return input_data

@app.get("/api/calculate/mass", tags=["calculate-mass"])
async def _calculate_mass()->dict:
    """
    Calculate mass.

    Returns:
        out (dict): dictionary:
            "mass": mass value,
            "unit": unit value
    """
    calculate_mass(input_data)
    mass = get_input_data_from_key("mass")
    unit = get_input_data_from_key("mass_unit")
    return {"mass": mass,
            "unit": unit}

@app.get("/api/calculate/thickness", tags=["calculate-thickness"])
async def _calculate_thickness()->dict:
    """
    Calculate thickness.

    Returns:
        out (dict): dictionary:
            "thickness": thickness value,
            "unit": unit value.
    """
    calculate_thickness(input_data)
    thickness = get_input_data_from_key("thickness")
    unit = get_input_data_from_key("length_unit")

    return {"thickness": thickness,
            "unit": unit}

@app.get("/api/elements", tags=["elements"])
async def get_elements_list()->dict:
    sample = make_XRaySample(input_data)
    elements = sample.elements
    return {"elements": [e.name for e in elements]}

@app.get("/api/absorption", tags=["absorption"])
async def get_all_absorption(abs_type:Literal["mass", "total", "linear"])\
    ->dict:
    out = get_absorption_data_all_elements(abs_type=abs_type)
    return out


@app.post("/api/calculate/formula/mass-ratios", 
         tags=["formula-mass-ratios"])
async def make_formula_from_mass_ratios(formula_list:list[str],
                                         ratios:list[str|float|int])->str:
    out = formula_from_mass_ratios(formula_list= formula_list,
                                    ratios= ratios,
                                    keep_order=True)
    return out