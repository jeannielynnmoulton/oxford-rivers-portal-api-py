from typing import Optional

import pandas as pd

from src.oxrivers_api.loader import Loader


class TimeseriesDiscovery:

    loader: Loader
    datasetID: str
    siteID: str
    determinand: Optional[str] = None
    timeseries: pd.DataFrame

    def __init__(self, loader: Loader, datasetID: str, siteID: str):
        self.datasetID = datasetID
        self.siteID = siteID
        self.loader = loader
        # try:
        self.timeseries = loader.load_timeseries(datasetID, siteID)
        # except Exception as e:
        #     raise Exception(f"Does this timeseries require a determinand? {e}")

    def __init__(self, loader: Loader, datasetID: str, siteID: str, determinand: str):
        self.datasetID = datasetID
        self.siteID = siteID
        self.loader = loader
        self.determinand = determinand
        # try:
        self.timeseries = loader.load_timeseries_determinand(datasetID, siteID, determinand)
        # except Exception as e:
        #     raise Exception(f"Maybe this timeseries does not require a determinand? {e}")

    def get_date_range(self):
        return self.timeseries.loc[0, "datetime"], self.timeseries.loc[len(self.timeseries["datetime"])-1, "datetime"]

    def get_number_of_data_points(self):
        return len(self.timeseries["datetime"])