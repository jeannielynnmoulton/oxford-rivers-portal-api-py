import unittest
import urllib

from src.demo import client
from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.endpoints import Endpoint
from src.oxrivers_api.exceptions import MissingParameterException, InvalidDateFormat


class MyTestCase(unittest.TestCase):
    def test_build_url_datasets(self):
        url = OxfordRiversClient.build_url(Endpoint.DATASETS)
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDatasets")

    def test_build_url_determinands(self):
        url = OxfordRiversClient.build_url(Endpoint.DETERMINANDS)
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDeterminands")

    def test_build_url_sites_error(self):
        with self.assertRaises(MissingParameterException):
            OxfordRiversClient.build_url(Endpoint.SITES)

    def test_build_url_sites(self):
        url = OxfordRiversClient.build_url(Endpoint.SITES, datasetID="edm")
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getSites?datasetID=edm")

    def test_build_url_dates_error(self):
        with self.assertRaises(MissingParameterException):
            OxfordRiversClient.build_url(Endpoint.DATES)

    def test_build_url_dates(self):
        url = OxfordRiversClient.build_url(Endpoint.DATES, datasetID="fft", date="2024-04-04")
        self.assertEqual(url, "https://oxfordrivers.ceh.ac.uk/getDataForDate?datasetID=fft&date=2024-04-04")

    def test_build_url_timeseries_error(self):
        with self.assertRaises(MissingParameterException):
            OxfordRiversClient.build_url(Endpoint.TIMESERIES)

    def test_build_url_timeseries(self):
        url = OxfordRiversClient.build_url(Endpoint.TIMESERIES, datasetID="fft", siteID="Oxford")
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
        url = OxfordRiversClient.build_url(Endpoint.TIMESERIES_DETERMINAND, datasetID="ea_bathing_water", siteID="EA1234", determinand="EC")
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
