from typing import List, Dict, Any, Union

import pyarrow as pa
import pandas as pd


def convert_to_table(data: List[Dict[str, Any]]) -> Union[pd.DataFrame, pa.Table]:
    """Get the properties"""
    # Your implementation here
    if not data:
        return pa.Table({})

    data = pa.Table.from_pylist(data)
    return data


def normalize_agency(agency: str) -> str:
    agency = agency.lower().strip()
    if not agency.endswith("_sanctions"):
        agency = f"{agency}_sanctions"
    return agency
