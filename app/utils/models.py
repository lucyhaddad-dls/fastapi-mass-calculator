from pydantic import BaseModel
from typing import Optional
import json
from numpy import ndarray

input_data = [
    {"name": "formula",
      "value": {"val": "Cu", "dtype": "str"}},
    {"name": "absorber",
      "value": {"val": "Cu", "dtype": "str"}},
    {"name": "edge",
      "value": {"val": "K", "dtype": "str"}},
    {"name": "density",
      "value": {"val": None, "dtype": "float"}},
    {"name": "area",
      "value": {"val": None, "dtype": "float"}},
    {"name": "mass",
      "value": {"val": None, "dtype": "float"}},
    {"name": "thickness",
      "value": {"val": None, "dtype": "float"}},
    {"name": "mu_total",
      "value": {"val": "2.6", "dtype": "float"}},
    {"name": "mass_unit",
      "value": {"val": "g", "dtype": "str"}},
    {"name": "length_unit",
      "value": {"val": "cm", "dtype": "str"}},
    {"name": "energy_unit",
      "value": {"val": "gev", "dtype": "str"}}
              ]

class InputMeasurement(BaseModel):
    val: str | None
    dtype: str | None

class AMeasurement(BaseModel):
    value: Optional[InputMeasurement] = None
    name: str

 
class NumpyEncoder(json.JSONEncoder):
    """
    e.g.
    ```
    # save as JSON
    a = np.array([[1, 2, 3],[4, 5, 6]])
    out = json.dumps({"val": a, "b": [2]}, cls=NumpyEncoder)

    # restore:
    restored = json.loads(out)
    a_restored = np.asarray(json_load["val])

    ```
    """
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return super().default(obj)