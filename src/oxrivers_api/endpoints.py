from collections import namedtuple
from enum import Enum

EndpointInfo = namedtuple("EndpointInfo", ["url_endpoint", "required_url_info", "json_folder"])

class Endpoint(Enum):
    """List of endpoints with tuple value of
    - url endpoint
    - required info list
    - local storage location for json"""
    DATASETS = EndpointInfo(url_endpoint="getDatasets", required_url_info=[], json_folder="datasets")
    SITES = EndpointInfo(url_endpoint="getSites", required_url_info=["dataset"], json_folder="sites")
    DATES = EndpointInfo(url_endpoint="getDataForDate", required_url_info=["dataset", "date"], json_folder="dates")
    TIMESERIES = EndpointInfo(url_endpoint="getTimeseries", required_url_info=["dataset", "site", "determinand"], json_folder="timeseries")
