import datetime

from src.oxrivers_api.endpoints import Endpoint
from src.oxrivers_api.exceptions import MissingParameterException, InvalidDateFormat
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




