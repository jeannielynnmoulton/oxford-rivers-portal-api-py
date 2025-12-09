import pandas as pd

from src.oxrivers_api.loader import Loader
from src.oxrivers_api.request_models import TimeseriesInfo, DataForDateInfo, RequestInfo, DeterminandInfo, DatasetsInfo, \
    SitesInfo, SitesRequest, DatasetRequest, DeterminandRequest


class DataOrganizer:

    loader: Loader

    datasets: pd.DataFrame
    # determinands: pd.DataFrame
    sites: dict[str, pd.DataFrame]
    timeseries: dict[str, pd.DataFrame]
    dates: dict[str, pd.DataFrame]

    key_to_info: dict[str, RequestInfo]

    named_store: dict[str, RequestInfo]

    def __init__(self, loader):
        self.loader = loader
        self.datasets = loader.load(DatasetRequest())
        self.determinands = loader.load(DeterminandRequest())
        self.sites = {datasetID: loader.load(SitesRequest(SitesInfo(datasetID))) for datasetID in self.datasets["id"]}
        self.timeseries = {}
        self.dates = {}
        self.key_to_info = {}

    def lookup_determinand_name(self, datasetID: str, determinand: str) -> str | None:
            for _, row in self.determinands.iterrows():
                for d in row["datasets"]:
                    if d["code"] == datasetID and d["id"] == determinand:
                        return "_".join(row["name"].split(" "))
            return None

    def get_timeseries(self, info: TimeseriesInfo, key: str = None) -> pd.DataFrame:
        if key is not None and key in self.timeseries.keys():
            raise Exception(f"Key {key} already exists for timeseries. Choose a unique key.")
        if key is None:
            sites_df = self.sites[info.datasetID]
            sites_name = "_".join(sites_df[sites_df["properties_id"] == info.siteID].loc[0, "properties_name"].split(" "))
            print(sites_name)
            determinand_name = self.lookup_determinand_name(info.datasetID, info.determinand)
            key = ":".join([info.datasetID, sites_name, determinand_name])
        self.key_to_info[key] = info
        self.timeseries[key] = self.loader.load_timeseries(info)
        return self.timeseries[key]

    def get_data_for_date(self, info: DataForDateInfo, key: str = None) -> pd.DataFrame:
        if key is not None and key in self.dates.keys():
            raise Exception(f"Key {key} already exists for data for date. Choose a unique key.")
        if key is None:
            key = "_".join([info.datasetID, info.date])
        self.key_to_info[key] = info
        self.timeseries[key] = self.loader.load_data_for_date(info)
        return self.timeseries[key]

    def list_timeseries_info(self):
        return self.key_to_info
