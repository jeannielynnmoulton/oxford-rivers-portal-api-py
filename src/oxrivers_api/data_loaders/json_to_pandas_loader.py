import json
from pathlib import Path

import pandas as pd

from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.data_loaders.abstract_loader import AbstractLoader
from oxrivers_api.models.data_models import Determinand, Site, Timeseries
from oxrivers_api.models.request_models import Request, DatasetsRequest, TimeseriesInfo, DataForDateInfo, SitesInfo


class JsonToPandasLoader(AbstractLoader):
    """
    Converts JSON to Pandas Dataframe
    """

    api_client: APIToJson

    def __init__(self, api_client: APIToJson):
        self.api_client = api_client

    def load(self, request: Request):
        return request.as_pandas(self)

    def base_load(self, request: Request):
        with open(request.request(self.api_client), "r") as f:
            data = json.load(f)
        datasets = [request.data_model(**d) for d in data]
        dicts = [d.model_dump() for d in datasets]
        return pd.json_normalize(dicts, sep='_')

    def load_datasets(self) -> pd.DataFrame:
        return self.base_load(DatasetsRequest())

    def load_determinands(self) -> pd.DataFrame:
        with open(self.api_client.get_determinands(), "r") as f:
            data = json.load(f)
        determinands = [Determinand(**d) for d in data["features"]]
        dicts = [d.model_dump() for d in determinands]
        return pd.json_normalize(dicts, sep='_')

    def load_sites(self, info: SitesInfo) -> pd.DataFrame:
        with open(self.api_client.get_sites(info.datasetID), "r") as f:
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

    def load_data_for_date(self, info: DataForDateInfo) -> pd.DataFrame:
        with open(self.api_client.get_data_for_date(info.datasetID, info.date), "r") as f:
            raw = json.load(f)
        df = pd.DataFrame(raw.get("data", []))

        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime']).dt.date
        if 'value' in df.columns:
            df['value'] = df['value'].astype(float)

        return df

    def dict_to_list(self, d: dict[str, dict[str, dict]]) -> list:
        result = []
        columns = list(d.keys())
        # assume all inner dicts share the same index keys
        indices = list(d[columns[0]].keys())
        for index in indices:
            row = {}
            for column in columns:
                row[column] = d[column].get(index)
            result.append(row)
        return result

    def load_timeseries_base(self, json_file: Path) -> pd.DataFrame:
        with open(json_file, "r") as f:
            raw = json.load(f)
        ts = Timeseries(**raw)
        if type(ts.data) is list:
            df = pd.json_normalize([p.model_dump() for p in ts.data])
            df.rename(columns={"timestamp": "datetime"}, inplace=True)
        else:
            df = pd.json_normalize(self.dict_to_list(ts.data.root))
            df.rename(columns={"sample date time": "datetime"}, inplace=True)
        for key, value in ts.metadata.model_dump().items():
            df[key] = value
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df

    def load_timeseries(self, info: TimeseriesInfo) -> pd.DataFrame:
        return self.load_timeseries_base(self.api_client.get_timeseries(info.datasetID, info.siteID, info.determinand))
