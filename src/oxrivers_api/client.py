import datetime

import requests

from src.oxrivers_api.endpoints import Endpoint
from src.oxrivers_api.exceptions import MissingParameterException, InvalidDateFormat, ClientRequestError
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
    def build_url(endpoint: Endpoint, **kwargs):
        url = OxfordRiversClient.BASE_URL + endpoint.value.url_endpoint
        infos = []
        for required_info in endpoint.value.required_url_info:
            try:
                infos.append((required_info, kwargs[required_info]))
            except:
                raise MissingParameterException(f"Error building url for \'{endpoint.value.url_endpoint}\'. Missing parameter \'{required_info}\'.")
        if len(infos) == 0:
            return url
        url = url + "?"
        for i, info,  in enumerate(infos):
            url = url + info[0]+"="+info[1]
            if i < len(infos)-1:
                url = url + "&"
        return url

    def request(self, url):
        try:
            response = requests.get(url).json()
            return response
        except Exception as e:
            raise ClientRequestError(e)

    def getDatasets(self):
        endpoint = Endpoint.DATASETS
        filepath = self.storage.get_endpoint_json_filepath(endpoint)
        if not self.storage.json_file_exists(endpoint):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint)), filepath)
        return filepath

    def getDeterminands(self):
        endpoint = Endpoint.DETERMINANDS
        filepath = self.storage.get_endpoint_json_filepath(endpoint)
        if not self.storage.json_file_exists(endpoint):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint)), filepath)
        return filepath

    def getSites(self, datasetID: str):
        endpoint = Endpoint.SITES
        filepath = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID)
        if not self.storage.json_file_exists(endpoint, datasetID=datasetID):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint, datasetID=datasetID)), filepath)
        return filepath

    def getDataForDate(self, datasetID: str, date: str):
        OxfordRiversClient.checkDateFormat(date)
        endpoint = Endpoint.DATES
        filepath = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID, date=date)
        if not self.storage.json_file_exists(endpoint, datasetID=datasetID, date=date):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint, datasetID=datasetID, date=date)), filepath)
        return filepath

    def getTimeseries(self, datasetID: str, siteID: str):
        endpoint = Endpoint.TIMESERIES
        filepath = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID, siteID=siteID)
        if not self.storage.json_file_exists(endpoint, datasetID=datasetID, siteID=siteID):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint, datasetID=datasetID, siteID=siteID)), filepath)
        return filepath

    def getTimeseriesDeterminand(self, datasetID: str, siteID: str, determinand: str):
        endpoint = Endpoint.TIMESERIES_DETERMINAND
        filepath = self.storage.get_endpoint_json_filepath(endpoint, datasetID=datasetID, siteID=siteID, determinand=determinand)
        if not self.storage.json_file_exists(endpoint, datasetID=datasetID, siteID=siteID, determinand=determinand):
            self.storage.write(self.request(OxfordRiversClient.build_url(endpoint, datasetID=datasetID, siteID=siteID, determinand=determinand)), filepath)
        return filepath



