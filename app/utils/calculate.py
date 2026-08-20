from sample_mass_calcs.xas_sample import XRaySample, Measurement
from numpy import ndarray, array
from .models import (input_data, AMeasurement, NumpyEncoder)
import json

_types = {"str": str,
            "float": float}

def _to_type(dtype:str): return _types[dtype]

def input_data_to_kwargs(input_data:list[AMeasurement])->dict:
    """
    Convert dictionary of input data to keyword-arguments 
    for making an `XRaySample` object. \\
    
    """
    kwargs = {}
    for itm in input_data:
        k = itm["name"]; v = itm["value"]
        if v["val"] is None or v["val"] == "None":
            kwargs[k] = None
        else:
            dtype = _to_type(v["dtype"])
            kwargs[k] = dtype(v["val"])
    return kwargs

def make_XRaySample(input_data:list[AMeasurement])->XRaySample:
    """
    Make `XRaySample` object from input values. \\
    Each entry in the `input_dict` must be of form: \
        `key { "val": , "dtype"}`.
    """
    values = input_data_to_kwargs(input_data)
    sample = XRaySample(**values)
    return sample

def get_name_and_unit(sample:XRaySample, name:str)\
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

def calculate_thickness(input_data:list[AMeasurement])->None:
    """
    If sample density is known, calculate sample thickness and update
    `input_dict`.
    """
    sample = make_XRaySample(input_data)
    if sample.density.value is not None:
        sample.calculate_thickness()
        update_input_data_from_sample(sample)

def calculate_mass(input_data:list[AMeasurement])->None:
    """
    If sample area and sample density (+ thickness) are known,\
    calculate sample mass and update `input_dict`.
    """
    sample = make_XRaySample(input_data)
    if sample.area.value is not None and sample.density.value is not None:
        sample.calculate_mass()
        update_input_data_from_sample(sample)

def update_input_data_from_sample(sample:XRaySample):
    """
    Update `input_data` with new sample values.
    """
    for i in range(len(input_data)):
        k = input_data[i]["name"]
        val = getattr(sample, k)
        if val is None:
            tmp = input_data[i]["value"]
            tmp["val"] = None
            input_data[i]["value"] = tmp
        elif hasattr(val, "value"):
            input_data[i]["value"]["val"] = str(val.value)
        else:
            input_data[i]["value"]["val"] = str(val)

def update_input_data_from_key(name:str, value:str):
    """
    Update`input_data` for a given value.
    """
    idx = [i for i in range(len(input_data))\
          if input_data[i]["name"] == name][0]
    input_data[idx]["value"]["val"] = value
  
def get_input_data_from_key(name:str)->str:
    idx = [i for i in range(len(input_data))\
              if input_data[i]["name"] == name][0]
    return input_data[idx]["value"]["val"]

def get_mass_absorption_data(elements:list[str])\
    ->tuple[str, str, str, str]:
    sample = make_XRaySample(input_data)
    ydata = [e.mass_absorption for e in sample.elements \
             if e.name in elements]
    if "total" in elements:
        ydata.append(sample.mass_absorption)
    xdata = sample.energy

    xdata, ydata, xlabel, ylabel = set_xy_data(xdata, ydata)

    return xdata, ydata, xlabel, ylabel

def get_linear_absorption_data(elements:list[str])\
    ->tuple[str, str, str, str]:
    # mass absorption data * density
    sample = make_XRaySample(input_data)
    if sample.density.value is None:
        raise AttributeError("Sample needs density value.")
    
    ydata = [e.mass_absorption*sample.density for e in sample.elements \
        if e.name in elements]
    if "total" in elements:
        ydata.append(sample.mass_absorption*sample.density)
    xdata = sample.energy
    xdata, ydata, xlabel, ylabel = set_xy_data(xdata, ydata)
    return xdata, ydata, xlabel, ylabel

def get_total_absorption_data(elements:list[str])\
    ->tuple[str, str, str, str]:
    # mass absorption data * density * thickness
    sample = make_XRaySample(input_data)
    if sample.density.value is None:
        raise AttributeError("Sample needs density value.")
    if sample.thickness.value is None:
        raise AttributeError("Sample needs thickness value.")

    ydata = [e.mass_absorption*sample.density*sample.thickness \
              for e in sample.elements if e.name in elements]
    if "total" in elements:
        ydata.append(sample.mass_absorption*sample.density*sample.thickness)
    xdata = sample.energy
    xdata, ydata, xlabel, ylabel = set_xy_data(xdata, ydata)
    return xdata, ydata, xlabel, ylabel    

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

    x = json.dumps(x, cls=NumpyEncoder)
    y = json.dumps(x, cls=NumpyEncoder)

    return x, y, xlabel, ylabel

