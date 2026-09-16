from sample_mass_calcs.xas_sample import XRaySample, Measurement, PhotoElement
from numpy import ndarray, array
from .models import (SampleMeasurement, SampleChemistryProps,
                     SamplePhysicalProps, SampleAbsorptionProps,
                     SampleElementProps, SampleUnitProps)

from typing import Literal

def sample_to_dict(sample:XRaySample)->dict:
    out = {"total": {},
           }
    
    total = {}

    for val in SampleChemistryProps._member_names_:
        value, unit = get_name_and_unit(sample, val)
        total[val] = {"value": value, "unit": unit}

    for val in SamplePhysicalProps._member_names_:
        value, unit = get_name_and_unit(sample, val)
        total[val] = {"value": value, "unit": unit}

    for val in SampleAbsorptionProps._member_names_:
        value, unit = get_name_and_unit(sample, val)
        if isinstance(value, ndarray): value = value.tolist()
        else: value = str(value)
        total[val] = {"value": value, "unit": unit}


    out["total"] = total

    for element in sample.elements:
        out[element.name] = {}
        for val in SampleElementProps._member_names_:
            value, unit = get_name_and_unit(element, val)
            if isinstance(value, ndarray): value = value.tolist()
            else: value = str(value)
            out[element.name][val] = {"value": value, "unit": unit}

    return out

def input_data_to_kwargs(input_data:list[SampleMeasurement])->dict:
    """
    Convert dictionary of input data to keyword-arguments 
    for making an `XRaySample` object. \\
    """
    kwargs = {}
    for itm in input_data:
        k = itm.name; v = itm.value
        if v == "None":
            kwargs[k] = None; continue
        if k in SamplePhysicalProps._member_names_:
            if isinstance(v, str):
                kwargs[k] = float(v)
        if k in SampleChemistryProps._member_names_ or k in SampleUnitProps._member_names_:
            kwargs[k] = str(v)

    return kwargs

def make_XRaySample(input_data:list[SampleMeasurement])->XRaySample:
    """
    Make `XRaySample` object from input values. \\
    Each entry in the `input_dict` must be of form: \
        `key { "val": , "dtype"}`.
    """
    values = input_data_to_kwargs(input_data)
    sample = XRaySample(**values)
    return sample

def get_name_and_unit(sample:XRaySample|PhotoElement, name:str)\
                    ->tuple[str|ndarray|float|int|None, str|None]:
    """
    Get value and unit for a `Measurement` on `XRaySample` object.

    Arguments:
        sample (XRaySample): Sample.
        name (str): Name of measurement.

    Returns:
        tuple (tuple): tuple containing:
            value (str|ndarray|float|int|None): Value of measurement.
            unit (str|None): Unit as a string.
    """
    measurement = getattr(sample, name)
    if hasattr(measurement, "unit"):
        unit = measurement.unit; value = measurement.value
    else:
        unit = None; value = measurement
    return value, unit

def calculate_thickness(input_data:list[SampleMeasurement])->None:
    """
    If sample density is known, calculate sample thickness and update
    `input_dict`.
    """
    sample = make_XRaySample(input_data)
    if sample.density.value is not None:
        sample.calculate_thickness()
    return sample_to_dict(sample)

def calculate_mass(input_data:list[SampleMeasurement])->None:
    """
    If sample area and sample density (+ thickness) are known,\
    calculate sample mass and update `input_dict`.
    """
    sample = make_XRaySample(input_data)
    if sample.area.value is not None and sample.density.value is not None:
        sample.calculate_mass()
    return sample_to_dict(sample)

def set_xy_data(x:ndarray|Measurement, 
                 y:list[ndarray]|list[Measurement])\
    ->tuple[str, str, str, str]:
    xlabel, ylabel = "", ""
    
    if hasattr(x, "unit"):
        xlabel = x.unit._repr_html_()
        x = x.value
    if hasattr(y, "unit"):
        ylabel = y.unit._repr_html_()
        y = y.value
    if isinstance(y, list):
        if hasattr(y[0], "unit"):
            ylabel = y[0].unit._repr_html_()
            y_out = []
        for yi in y:
            if hasattr(yi, "value"):
                y_out.append(yi.value)
            else: y_out.append(yi)
        y = array(y_out)

    x = x.tolist()
    y = [y0.tolist() for y0 in y]

    return x, y, xlabel, ylabel

def get_absorption_data_all_elements(
        input_data:list[SampleMeasurement],
        abs_type:Literal["mass", "linear", "total"])\
    -> dict:
    sample = make_XRaySample(input_data)
    if abs_type != "mass":
        sample.calculate_density()
        sample.calculate_thickness()
        sample.calculate_mass()
    out = {}
    out["kind"] = abs_type

    xtotal = sample.energy
    ytotal = []

    if abs_type == "mass":
        yt = sample.mass_absorption
        xt, yt, xl, yl = set_xy_data(xtotal, yt)
        ytotal.append({"name": "total", "y": yt})
        for e in sample.elements:
            yt = set_xy_data(xtotal,
                            e.mass_absorption)[1]
            ytotal.append({"name": e.name, "y": yt})

    if abs_type == "linear":
        if sample.density.value is None:
            return {"error": "sample has no attribute density"}
        yt = sample.mass_absorption * sample.density
        xt, yt, xl, yl = set_xy_data(xtotal, yt)
        ytotal.append({"name": "total", "y": yt})
        for e in sample.elements:
            yt = set_xy_data(xtotal,
                e.mass_absorption*sample.density)[1]
            ytotal.append({"name": e.name, "y": yt})

    if abs_type == "total":
        missing = []
        if sample.density.value is None:
            missing.append("density")
        if sample.thickness.value is None:
            missing.append("thickness")
        if len(missing) > 0:
            return {"error": f"sample has no attribute {[k for k in missing]}"}
        yt = sample.mass_absorption*sample.density*sample.thickness
        xt, yt, xl, yl = set_xy_data(xtotal, yt)
        ytotal.append({"name": "total", "y": yt})
        for e in sample.elements:
            yt = set_xy_data(xtotal,
                e.mass_absorption*sample.density*sample.thickness)[1]
            ytotal.append({"name": e.name, "y": yt})

    out["x"] = xt; out["xlabel"] = xl; out["ylabel"] = yl
    out["y"] = ytotal
    return out

