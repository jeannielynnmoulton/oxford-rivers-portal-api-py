from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime, date

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
    timestamp: datetime = Field(..., alias="datetime")
    value: Optional[float]

    @field_validator("value", mode="before")
    def parse_value(cls, v):
        if v in ("", None):
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None


class Timeseries(BaseModel):
    metadata: TimeseriesMetadata
    data: List[TimeseriesPoint]

    model_config = {
        "populate_by_name": True,  # allow using field names even if there are aliases
        "extra": "ignore"          # ignore fields not defined in the model
    }
