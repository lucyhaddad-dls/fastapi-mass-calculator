from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.calculate import (SampleMeasurement, make_XRaySample,
                              get_absorption_data_all_elements,
                              calculate_thickness, calculate_mass,
                              sample_to_dict)
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


@app.get("/api/calculate/mass", tags=["calculate-mass"])
async def _calculate_mass(input_data:list[SampleMeasurement])->dict:
    """
    Calculate mass.

    Returns:
        out (dict): dictionary:
            "value": mass value,
            "unit": unit value
    """
    out = calculate_mass(input_data)


    return out["total"]["mass"]

@app.get("/api/calculate/thickness", tags=["calculate-thickness"])
async def _calculate_thickness(input_data:list[SampleMeasurement])->dict:
    """
    Calculate thickness.

    Returns:
        out (dict): dictionary:
            "value": thickness value,
            "unit": unit value.
    """
    out = calculate_thickness(input_data)
    return out["total"]["thickness"]

@app.get("/api/elements", tags=["elements"])
async def get_elements_list(input_data:list[SampleMeasurement])->dict:
    sample = make_XRaySample(input_data)
    elements = sample.elements
    return {"elements": [e.name for e in elements]}

@app.post("/api/absorption", tags=["absorption"])
async def get_all_absorption(
    input_data:list[SampleMeasurement],
    abs_type:Literal["mass", "total", "linear"])\
    ->dict:
    out = get_absorption_data_all_elements(input_data=input_data,
                                           abs_type=abs_type)
    return out

@app.post("/api/calculate/formula/mass-ratios", 
         tags=["formula-mass-ratios"])
async def make_formula_from_mass_ratios(formula_list:list[str],
                                         ratios:list[str|float|int])->str:
    out = formula_from_mass_ratios(formula_list= formula_list,
                                    ratios= ratios,
                                    keep_order=True)
    return out

@app.post("/api/calculate/all")
async def get_sample_dict(input_data:list[SampleMeasurement])->dict:
    sample = make_XRaySample(input_data)
    if sample.density.value is not None:
        sample.calculate_thickness()
        if sample.area.value is not None:
            sample.calculate_mass()
    return sample_to_dict(sample)