from pydantic import BaseModel, field_validator, RootModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date

"""
Models for data from the API. Used to convert
"""

# -------------------------
# Dataset
# -------------------------

class DatasetMetadata(BaseModel):
    name: str
    graph: bool
    map: bool

class Dataset(BaseModel):
    id: str
    name: str
    group: str
    type: str
    metadata: DatasetMetadata

class Datasets(BaseModel):
    datasets: List[Dataset]

# -------------------------
# Determinand
# -------------------------
class DeterminandDatasetRef(BaseModel):
    code: str
    id: str

class Determinand(BaseModel):
    name: str
    description: str
    datasets: List[DeterminandDatasetRef]

# -------------------------
# Site
# -------------------------
class Geometry(BaseModel):
    coordinates: List[float]


class SiteProperties(BaseModel):
    id: str|int
    name: str
    threshold: Optional[float] = None
    popserved: Optional[int] = None


class Site(BaseModel):
    geometry: Geometry
    properties: SiteProperties

# -------------------------
# DataForDate
# -------------------------
class DataForDatePoint(BaseModel):
    datetime: date
    value: float
    id: int


class DataForDate(BaseModel):
    metadata: dict
    data: List[DataForDatePoint]

# -------------------------
# Timeseries
# -------------------------

class TimeseriesMetadata(BaseModel):
    id: str
    siteID: str
    endPoint: str
    determinand: Optional[str] = None
    determinand_label: Optional[str] = None
    determinand_unit: Optional[str] = None

class TimeseriesPoint(BaseModel):
    datetime: datetime
    value: Optional[float] = None
    qualifier: Optional[str] = None

    @field_validator("value", mode="before")
    def parse_value(cls, v):
        if v in ("", None):
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

class TimeseriesDict(RootModel[Dict[str, Dict[str, Any]]]):
    pass


TimeseriesData = Union[
    List[TimeseriesPoint],
    TimeseriesDict
]

class Timeseries(BaseModel):
    metadata: TimeseriesMetadata
    data: TimeseriesData
