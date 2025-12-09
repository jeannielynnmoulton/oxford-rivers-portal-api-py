import datetime
from dataclasses import fields

import requests

from oxrivers_api.errors.exceptions import InvalidDateFormat, ClientRequestError
from oxrivers_api.models.request_models import DatasetsRequest, DeterminandsRequest, DataForDateInfo, TimeseriesInfo, SitesInfo, Request
from oxrivers_api.storage.json_storage import AbstractStorage


class APIToJson:
    """Responsible for getting JSON from the API.
    JSON is stored locally, and calls are made to the API only
    if there is not a local JSON file with the data requested."""

    storage: AbstractStorage
    BASE_URL: str = "https://oxfordrivers.ceh.ac.uk/"

    def __init__(self, storage):
        self.storage = storage

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
        url = APIToJson.BASE_URL + request.url_endpoint
        request_info = fields(request.request_info)
        if len(request_info) == 0:
            return url
        parameter_elements = []
        for i, info in enumerate(request_info):
            if info.name is None or getattr(request.request_info, info.name) is None:
                continue
            parameter_elements.append(info.name+"="+getattr(request.request_info, info.name))
        return url + "?" + "&".join(parameter_elements)

    def _request(self, url):
        try:
            response = requests.get(url).json()
            return response
        except Exception as e:
            raise ClientRequestError(e)

    def get_datasets(self):
        """
        Makes a request to the API for getDatasets
        :return: Path to where the json file is stored
        :rtype: Path
        """
        request = DatasetsRequest()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self._request(APIToJson.build_url(request)), filepath)
        return filepath

    def get_determinands(self):
        """
        Makes a request to the API for getDeterminands
        :return: Path to where the json file is stored
        :rtype: Path
        """
        request = DeterminandsRequest()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self._request(APIToJson.build_url(request)), filepath)
        return filepath

    def get_sites(self, datasetID: str):
        """
        Makes a request to the API for getSites for given datasetID
        :param datasetID: the dataset to get
        :type datasetID: str
        :return: Path to where the json file is stored
        :rtype: Path
        """
        request = SitesInfo(datasetID).request()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self._request(APIToJson.build_url(request)), filepath)
        return filepath

    def get_data_for_date(self, datasetID: str, date: str):
        """
        Makes a request to the API for getDataForDate for given datasetID and date in YYYY-MM-DD format
        :param datasetID: the dataset to get
        :type datasetID: str
        :param date: the date to get in YYYY-MM-DD format
        :type date: str
        :return: Path to where the json file is stored
        :rtype: Path
        """
        APIToJson.checkDateFormat(date)
        request = DataForDateInfo(datasetID, date).request()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self._request(APIToJson.build_url(request)), filepath)
        return filepath

    def get_timeseries(self, datasetID: str, siteID: str, determinand: str = None):
        """
        Makes a request to the API for getTimeseries for given datasetID, siteID and determinand (if required)
        :param datasetID: the dataset to get
        :type datasetID: str
        :param siteID: the site to get, by ID not name
        :type siteID: str
        :param determinand: default None, the determinand to get, by ID not name
        :type determinand: Optional[str]
        :return: Path to where the json file is stored
        :rtype: Path
        """
        request = TimeseriesInfo(datasetID, siteID, determinand).request()
        filepath = self.storage.get_endpoint_json_filepath(request)
        if not self.storage.json_file_exists(request):
            self.storage.write(self._request(APIToJson.build_url(request)), filepath)
        return filepath



