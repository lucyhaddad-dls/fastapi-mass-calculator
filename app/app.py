from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from .utils.calculate import (make_XRaySample,
                              get_absorption_data_all_elements,
                              calculate_thickness, calculate_mass,
                              sample_to_dict)
from .utils.sample_builder import formula_from_mass_ratios
from .utils.models import (SampleInputData)
from typing import Literal, Annotated

app = FastAPI()

origins = ["http://localhost:5173",
           "localhost:5173"]

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                )


@app.get("/api")
async def read_root() -> dict:
    return {"message": "MASS CALCULATOR!!!"}


@app.post("/api/calculate/mass", tags=["physical properties"])
async def _calculate_mass(input_data:Annotated[SampleInputData,
            Body(examples=[
                {"input_data":[
                            {"name":"formula" ,"value":"TiO2"},
                            {"name":"edge" , "value":"L2"},
                            {"name":"absorber", "value":"Ti"},
                            {"name": "density", "value":"2.3"},
                            {"name": "area", "value":"5"},
                            {"name":"mass_unit", "value": "mg"}]
                }])])->dict:
    """
    Calculate mass.

    Returns:
        out (dict): dictionary:
            "value": mass value,
            "unit": unit value
    """
    out = calculate_mass(input_data)


    return out["total"]["mass"]

@app.post("/api/calculate/thickness", tags=["physical properties"])
async def _calculate_thickness(input_data:Annotated[SampleInputData,
            Body(examples=[
                {"input_data":[
                            {"name":"formula" ,"value":"TiO2"},
                            {"name":"edge" , "value":"K"},
                            {"name":"absorber", "value":"Ti"},
                            {"name": "density", "value":"34"},
                            {"name": "mu_total", "value": "2.3"}]
                }])])->dict:
    """
    Calculate thickness.

    Returns:
        out (dict): dictionary:
            "value": thickness value,
            "unit": unit value.
    """
    out = calculate_thickness(input_data)
    return out["total"]["thickness"]

@app.post("/api/elements", tags=["chemical properties"])
async def get_elements_list(input_data:Annotated[SampleInputData,
            Body(examples=[
                {"input_data":[
                            {"name":"formula" ,"value":"RhClFe3OH4"},
                            {"name":"edge", "value": "k"},
                            {"name": "absorber", "value": "Rh"}]
                }])])->dict:
    sample = make_XRaySample(input_data)
    elements = sample.elements
    return {"elements": [e.name for e in elements]}

@app.post("/api/absorption", tags=["absorption"])
async def get_all_absorption(
    input_data:SampleInputData,
    abs_type:Literal["mass", "total", "linear"])\
    ->dict:
    out = get_absorption_data_all_elements(input_data=input_data,
                                           abs_type=abs_type)
    return out

@app.post("/api/calculate/formula/mass-ratios", 
         tags=["physical properties"])
async def make_formula_from_mass_ratios(formula_list:Annotated[list[str],
                                                Body(examples=[["Fe", "O", "P"]])],
                                         ratios:Annotated[list[str|float|int],
                                                Body(examples=[ [1, 0.5, 0.3] ])])->str:
    out = formula_from_mass_ratios(formula_list= formula_list,
                                    ratios= ratios,
                                    keep_order=True)
    return out

@app.post("/api/calculate/all", 
          tags=["absorption", "chemical properties", "physical properties"])
async def get_sample_dict(input_data:SampleInputData)->dict:
    sample = make_XRaySample(input_data)
    if sample.density.value is not None:
        sample.calculate_thickness()
        if sample.area.value is not None:
            sample.calculate_mass()
    return sample_to_dict(sample)