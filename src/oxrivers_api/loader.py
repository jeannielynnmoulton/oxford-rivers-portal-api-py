import json
from pathlib import Path

import pandas as pd

from src.oxrivers_api.data_models import Dataset, Determinand, Site, Timeseries
from src.oxrivers_api.endpoints import Endpoint
from src.oxrivers_api.storage import Storage


class Loader:

    storage: Storage

    def __init__(self, storage: Storage):
        self.storage = storage

    def load_datasets(self) -> pd.DataFrame:
        endpoint = Endpoint.DATASETS
        json_file = self.storage.get_endpoint_json_filepath(endpoint)
        with open(json_file, "r") as f:
            data = json.load(f)
        datasets = [Dataset(**d) for d in data]
        dicts = [d.model_dump() for d in datasets]
        return pd.json_normalize(dicts, sep='_')

    def load_determinands(self) -> pd.DataFrame:
        endpoint = Endpoint.DETERMINANDS
        json_file = self.storage.get_endpoint_json_filepath(endpoint)
        with open(json_file, "r") as f:
            data = json.load(f)
        determinands = [Determinand(**d) for d in data["features"]]
        dicts = [d.model_dump() for d in determinands]
        return pd.json_normalize(dicts, sep='_')

    def load_sites(self, datasetID: str) -> pd.DataFrame:
        endpoint = Endpoint.SITES
        json_file = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID)
        with open(json_file, "r") as f:
            data = json.load(f)
        datasets = [Site(**d) for d in data["features"]]
        dicts = [d.model_dump() for d in datasets]
        df = pd.json_normalize(dicts, sep='_')

        # Flatten geometry and properties
        if 'geometry_coordinates' in df.columns:
            df[['lon', 'lat']] = pd.DataFrame(df['geometry_coordinates'].tolist(), index=df.index)
        if 'properties' in df.columns:
            props = pd.json_normalize(df['properties'])
            df = df.drop(columns=['properties']).join(props)

        return df
    #
    # # -------------------------
    # # Load DataForDate → DataFrame
    # # -------------------------
    # def load_data_for_date(self) -> pd.DataFrame:
    #     # get json
    #     raw = endpoint.get_json()
    #     df = pd.DataFrame(raw.get("data", []))
    #
    #     if 'datetime' in df.columns:
    #         df['datetime'] = pd.to_datetime(df['datetime']).dt.date
    #     if 'value' in df.columns:
    #         df['value'] = df['value'].astype(float)
    #
    #     return df
    #
    # -------------------------
    # Load Timeseries → DataFrame
    # -------------------------
    def load_timeseries_base(self, json_file: Path) -> pd.DataFrame:
        # Load JSON
        with open(json_file, "r") as f:
            raw = json.load(f)

        # Validate with Pydantic
        ts = Timeseries(**raw)

        # Flatten data points
        df = pd.json_normalize([p.model_dump() for p in ts.data])
        df.rename(columns={"timestamp": "datetime"}, inplace=True)

        # Add metadata columns
        for key, value in ts.metadata.model_dump().items():
            df[key] = value

        # Ensure datetime type
        df["datetime"] = pd.to_datetime(df["datetime"])

        return df

    def load_timeseries(self, datasetID: str, siteID: str) -> pd.DataFrame:
        endpoint = Endpoint.TIMESERIES
        json_file = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID, siteID=siteID)
        return self.load_timeseries_base(json_file)

    def load_timeseries_determinand(self, datasetID: str, siteID: str, determinand: str) -> pd.DataFrame:
        endpoint = Endpoint.TIMESERIES
        json_file = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID, siteID=siteID, determinand=determinand)
        return self.load_timeseries_base(json_file)
