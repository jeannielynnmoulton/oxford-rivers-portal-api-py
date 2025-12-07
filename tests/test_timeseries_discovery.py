import unittest

from pandas import Timestamp

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.loader import Loader
from src.oxrivers_api.timeseries_discovery import TimeseriesDiscovery


class TestTimeSeriesDiscovery(unittest.TestCase):
    client = OxfordRiversClient("./tests/data")
    loader = Loader(client)
    discovery_determinand = TimeseriesDiscovery(loader, "ea_wq_sonde", "E01612A", "fdom")
    # discovery_no_determinand = TimeseriesDiscovery(loader, "fft", "Oxford")

    def test_get_date_range(self):
        self.assertEqual(self.discovery_determinand.get_date_range(), (Timestamp('2022-11-28 10:06:17'), Timestamp('2022-06-24 12:40:35')))

    def test_get_number_of_data_points(self):
        self.assertEqual(self.discovery_determinand.get_number_of_data_points(), 3683)

if __name__ == '__main__':
    unittest.main()
