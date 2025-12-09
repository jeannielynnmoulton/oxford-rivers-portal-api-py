import datetime
from dataclasses import fields

import requests

from src.oxrivers_api.exceptions import InvalidDateFormat, ClientRequestError
from src.oxrivers_api.request_models import DatasetRequest, DeterminandRequest, SitesRequest, DataForDateRequest, \
    TimeseriesRequest, DataForDateInfo, TimeseriesInfo, SitesInfo, Request
from src.oxrivers_api.storage import Storage

class OxfordRiversClient:
    """Responsible for getting JSON from the API.
    JSON is stored """

    storage: Storage
    BASE_URL: str = "https://oxfordrivers.ceh.ac.uk/"

    def __init__(self, data_dir):
        self.storage = Storage(data_dir)

    @staticmethod
    def checkDateFormat(date: str):
        try:
            formatted = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
        except:
            raise InvalidDateFormat(f"{date} is not a valid date format. Date must have format YYYY-MM-DD.")
        if formatted != date:
            raise InvalidDateFormat(f"{date} is not a valid date format. Date must have format YYYY-MM-DD.")


    @staticmethod
    def build_url(request: Request):
        url = OxfordRiversClient.BASE_URL + request.url_endpoint
        request_info = fields(request.request_info)
        if len(request_info) == 0:
            return url
        parameter_elements = []
        for i, info in enumerate(request_info):
            if info.name is None or getattr(request.request_info, info.name) is None:
                continue
            parameter_elements.append(info.name+"="+getattr(request.request_info, info.name))
        return url + "?" + "&".join(parameter_elements)

    def request(self, url):
        try:
            response = requests.get(url).json()
            return response
        except Exception as e:
            raise ClientRequestError(e)

    def getDatasets(self):
        request = DatasetRequest()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self.request(OxfordRiversClient.build_url(request)), filepath)
        return filepath

    def getDeterminands(self):
        request = DeterminandRequest()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self.request(OxfordRiversClient.build_url(request)), filepath)
        return filepath

    def getSites(self, datasetID: str):
        request = SitesRequest(SitesInfo(datasetID))
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self.request(OxfordRiversClient.build_url(request)), filepath)
        return filepath

    def getDataForDate(self, datasetID: str, date: str):
        OxfordRiversClient.checkDateFormat(date)
        request = DataForDateRequest(DataForDateInfo(datasetID, date))
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self.request(OxfordRiversClient.build_url(request)), filepath)
        return filepath

    def getTimeseries(self, datasetID: str, siteID: str, determinand: str = None):
        request = TimeseriesRequest(TimeseriesInfo(datasetID, siteID, determinand))
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self.request(OxfordRiversClient.build_url(request)), filepath)
        return filepath



