import unittest

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.exceptions import MissingParameterException, InvalidDateFormat
from src.oxrivers_api.request_models import DatasetRequest, DatasetsInfo, DeterminandRequest, SitesRequest, SitesInfo, \
    DataForDateRequest, DataForDateInfo, TimeseriesRequest, TimeseriesInfo


class MyTestCase(unittest.TestCase):
    def test_build_url_datasets(self):
        url = OxfordRiversClient.build_url(DatasetRequest())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDatasets")

    def test_build_url_determinands(self):
        url = OxfordRiversClient.build_url(DeterminandRequest())
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDeterminands")

    def test_build_url_sites(self):
        url = OxfordRiversClient.build_url(SitesRequest(SitesInfo("edm")))
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getSites?datasetID=edm")

    def test_build_url_dates(self):
        url = OxfordRiversClient.build_url(DataForDateRequest(DataForDateInfo("fft", "2024-04-04")))
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDataForDate?datasetID=fft&date=2024-04-04")

    def test_build_url_timeseries(self):
        url = OxfordRiversClient.build_url(TimeseriesRequest(TimeseriesInfo("fft", "Oxford")))
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getTimeseries?datasetID=fft&siteID=Oxford")

    def test_check_date_format(self):
        OxfordRiversClient.checkDateFormat("2025-05-05")
        with self.assertRaises(InvalidDateFormat):
            OxfordRiversClient.checkDateFormat("05-05-2025")
        with self.assertRaises(InvalidDateFormat):
            OxfordRiversClient.checkDateFormat("2025-5-05")
        with self.assertRaises(InvalidDateFormat):
            OxfordRiversClient.checkDateFormat("2025-13-5")

    def test_build_url_timeseries_determinand(self):
        url = OxfordRiversClient.build_url(TimeseriesRequest(TimeseriesInfo("ea_bathing_water", "EA1234", "EC")))
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getTimeseries?datasetID=ea_bathing_water&siteID=EA1234&determinand=EC")

    def test_getDatasets(self):
        client = OxfordRiversClient("./data")
        client.getDatasets()

    def test_getDeterminands(self):
        client = OxfordRiversClient("./data")
        client.getDeterminands()

    def test_getSites(self):
        client = OxfordRiversClient("./data")
        client.getSites("fft")

    def test_getDataForDate(self):
        client = OxfordRiversClient("./data")
        client.getDataForDate("rainfall", "2024-07-31")

    def test_getTimeseries(self):
        client = OxfordRiversClient("./data")
        client.getTimeseries("fft", "Oxford")

    def test_getTimeseriesDeterminand(self):
        client = OxfordRiversClient("./data")
        client.getTimeseriesDeterminand("ea_wq_sonde", "E01612A", "fdom")


if __name__ == '__main__':
    unittest.main()
