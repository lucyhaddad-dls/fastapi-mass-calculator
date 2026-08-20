from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.calculate import (input_data, update_input_data_from_key, calculate_thickness,
                              calculate_mass,
                              AMeasurement, get_input_data_from_key,
                              get_linear_absorption_data, get_mass_absorption_data,
                                get_total_absorption_data)

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

@app.post("/api/calculate/mass-absorption",
          tags=["calculate-mass_absorption"])
async def calculate_mass_absorption(elements:list[str]=["total"])->dict:
    xdata, ydata, xlabel, ylabel = get_mass_absorption_data(elements)
    out = {"xlabel": xlabel, "ylabel": ylabel, "x": xdata, "y": ydata}
    return out

@app.post("/api/calculate/linear-mass-absorption", 
         tags=["calculate-linear_mass_absorption"])
async def calculate_linear_absorption(elements:list[str]=["total"])->dict:
    xdata, ydata, xlabel, ylabel = get_linear_absorption_data(elements)
    out = {"xlabel": xlabel, "ylabel": ylabel, "x": xdata, "y": ydata}
    return out

@app.post("/api/calculate/total-mass-absorption", 
         tags=["calculate-total_mass_absorption"])
async def calculate_total_absorption(elements:list[str]=["total"])->dict:
    xdata, ydata, xlabel, ylabel = get_total_absorption_data(elements)
    out = {"xlabel": xlabel, "ylabel": ylabel, "x": xdata, "y": ydata}
    return out

