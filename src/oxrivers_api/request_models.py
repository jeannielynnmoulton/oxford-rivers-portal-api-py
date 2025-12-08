from dataclasses import dataclass
from typing import Optional

from src.oxrivers_api.data_models import Dataset, Determinand, Site, DataForDate, Timeseries

@dataclass
class Request:
    # data_model: type = None
    def as_pandas(self, loader):
        raise NotImplementedError
    def request(self, client):
        raise NotImplementedError

@dataclass
class DatasetRequest(Request):
    data_model: type = Dataset
    def as_pandas(self, loader):
        return loader.load_datasets()
    def request(self, client):
        return client.getDatasets()


@dataclass
class DeterminandRequest(Request):
    data_model: type = Determinand
    def as_pandas(self, loader):
        return loader.load_determinands()
    def request(self, client):
        return client.getDeterminands()


@dataclass
class SitesRequest(Request):
    datasetID: str
    data_model: type = Site
    def as_pandas(self, loader):
        return loader.load_sites(self.datasetID)
    def request(self, client):
        return client.getSites(self.datasetID)


@dataclass
class DataForDateRequest(Request):
    datasetID: str
    date: str
    data_model: type = DataForDate
    def as_pandas(self, loader):
        return loader.load_data_for_date(self.datasetID, self.date)
    def request(self, client):
        return client.getDataForDate(self.datasetID, self.date)


@dataclass
class TimeseriesRequest(Request):
    datasetID: str
    siteID: str
    determinand: Optional[str] = None
    data_model: type = Timeseries
    def as_pandas(self, loader):
        if self.determinand is None:
            return loader.load_timeseries(self.datasetID, self.siteID)
        else:
            return loader.load_timeseries_determinand(self.datasetID, self.siteID, self.determinand)
    def request(self, client):
        if self.determinand is None:
            return client.getTimeseries(self.datasetID, self.siteID)
        else:
            return client.getTimeseriesDeterminand(self.datasetID, self.siteID, self.determinand)
