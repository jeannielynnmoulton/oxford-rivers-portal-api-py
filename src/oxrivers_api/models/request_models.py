from dataclasses import dataclass
from typing import Optional

from src.oxrivers_api.models.data_models import Dataset, Determinand, Site, DataForDate, Timeseries

@dataclass
class RequestInfo:
    def request(self):
        raise NotImplemented

@dataclass
class DatasetsInfo(RequestInfo):
    def request(self):
        return DatasetRequest()

@dataclass
class DeterminandInfo(RequestInfo):
    def request(self):
        return DeterminandRequest()

@dataclass
class SitesInfo(RequestInfo):
    datasetID: str
    def request(self):
        return SitesRequest(self)

@dataclass
class DataForDateInfo(RequestInfo):
    datasetID: str
    date: str
    def request(self):
        return DataForDateRequest(self)

@dataclass
class TimeseriesInfo(RequestInfo):
    datasetID: str
    siteID: str
    determinand: Optional[str] = None
    def request(self):
        return TimeseriesRequest(self)

@dataclass
class Request:
    def __init__(self):
        self.data_model = None
        self.json_storage_folder = None
        self.request_info = None
        self.url_endpoint = None
    def as_pandas(self, json_to_pandas):
        raise NotImplementedError
    def request(self, api_client):
        raise NotImplementedError

@dataclass
class DatasetRequest(Request):
    data_model: type = Dataset
    json_storage_folder: str = "datasets"
    request_info = DatasetsInfo()
    url_endpoint = "getDatasets"
    def as_pandas(self, json_to_pandas):
        return json_to_pandas.load_datasets()
    def request(self, api_client):
        return api_client.getDatasets()


@dataclass
class DeterminandRequest(Request):
    data_model: type = Determinand
    json_storage_folder: str = "determinands"
    request_info = DeterminandInfo()
    url_endpoint = "getDeterminands"
    def as_pandas(self, json_to_pandas):
        return json_to_pandas.load_determinands()
    def request(self, api_client):
        return api_client.getDeterminands()


@dataclass
class SitesRequest(Request):
    request_info: SitesInfo
    data_model: type = Site
    json_storage_folder: str = "sites"
    url_endpoint = "getSites"
    def as_pandas(self, json_to_pandas):
        return json_to_pandas.load_sites(self.request_info)
    def request(self, api_client):
        return api_client.getSites(self.request_info.datasetID)


@dataclass
class DataForDateRequest(Request):
    request_info: DataForDateInfo
    data_model: type = DataForDate
    json_storage_folder: str = "dates"
    url_endpoint = "getDataForDate"
    def as_pandas(self, json_to_pandas):
        return json_to_pandas.load_data_for_date(self.request_info)
    def request(self, client):
        return client.getDataForDate(self.request_info.datasetID, self.request_info.date)


@dataclass
class TimeseriesRequest(Request):
    request_info: TimeseriesInfo
    data_model: type = Timeseries
    json_storage_folder: str = "timeseries"
    url_endpoint = "getTimeseries"
    def as_pandas(self, json_to_pandas):
        return json_to_pandas.load_timeseries(self.request_info)
    def request(self, client):
        if self.request_info.determinand is None:
            return client.getTimeseries(self.request_info.datasetID, self.request_info.siteID)
        else:
            return client.getTimeseriesDeterminand(self.request_info.datasetID, self.request_info.siteID, self.request_info.determinand)
