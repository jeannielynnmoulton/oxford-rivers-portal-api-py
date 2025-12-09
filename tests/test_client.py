import unittest
from pathlib import Path

from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.errors.exceptions import InvalidDateFormat
from oxrivers_api.models.request_models import DatasetsRequest, DeterminandsRequest, SitesInfo, \
    DataForDateInfo, TimeseriesInfo
from oxrivers_api.storage.json_storage import LocalJsonStorage


class TestClient(unittest.TestCase):
    storage = LocalJsonStorage(Path("./data"))

    def test_build_url_datasets(self):
        url = APIToJson.build_url(DatasetsRequest())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDatasets")

    def test_build_url_determinands(self):
        url = APIToJson.build_url(DeterminandsRequest())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDeterminands")

    def test_build_url_sites(self):
        url = APIToJson.build_url(SitesInfo("edm").request())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getSites?datasetID=edm")

    def test_build_url_dates(self):
        url = APIToJson.build_url(DataForDateInfo("fft", "2024-04-04").request())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDataForDate?datasetID=fft&date=2024-04-04")

    def test_build_url_timeseries(self):
        url = APIToJson.build_url(TimeseriesInfo("fft", "Oxford").request())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getTimeseries?datasetID=fft&siteID=Oxford")

    def test_check_date_format(self):
        APIToJson.checkDateFormat("2025-05-05")
        with self.assertRaises(InvalidDateFormat):
            APIToJson.checkDateFormat("05-05-2025")
        with self.assertRaises(InvalidDateFormat):
            APIToJson.checkDateFormat("2025-5-05")
        with self.assertRaises(InvalidDateFormat):
            APIToJson.checkDateFormat("2025-13-5")

    def test_build_url_timeseries_determinand(self):
        url = APIToJson.build_url(TimeseriesInfo("ea_bathing_water", "EA1234", "EC").request())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getTimeseries?datasetID=ea_bathing_water&siteID=EA1234&determinand=EC")

    def test_getDatasets(self):
        client = APIToJson(self.storage)
        client.get_datasets()

    def test_getDeterminands(self):
        client = APIToJson(self.storage)
        client.get_determinands()

    def test_getSites(self):
        client = APIToJson(self.storage)
        client.get_sites("fft")

    def test_getDataForDate(self):
        client = APIToJson(self.storage)
        client.get_data_for_date("rainfall", "2024-07-31")

    def test_getTimeseries(self):
        client = APIToJson(self.storage)
        client.get_timeseries("fft", "Oxford")

    def test_getTimeseriesDeterminand(self):
        client = APIToJson(self.storage)
        client.get_timeseries("ea_wq_sonde", "E01612A", "fdom")


if __name__ == '__main__':
    unittest.main()
