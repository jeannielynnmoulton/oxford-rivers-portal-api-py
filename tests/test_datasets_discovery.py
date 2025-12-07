import unittest

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.datasets_discovery import DatasetsDiscovery
from src.oxrivers_api.loader import Loader


class TestDiscovery(unittest.TestCase):
    client = OxfordRiversClient("./tests/data")
    loader = Loader(client)
    discovery = DatasetsDiscovery(loader)

    def test_dataset_discovery_get_ids(self):
        self.assertListEqual(list(self.discovery.get_ids()), ['ea_bathing_water', 'edm', 'ea_flood_warnings', 'ea_lf_sonde', 'ea_water_quality', 'ea_wq_sonde', 'fft', 'rainfall', 'freshwater_watch', 'wtrt', 'thames_initiative'])

    def test_dataset_discovery_get_columns(self):
        self.assertListEqual(list(self.discovery.get_columns()), ['id', 'name', 'group', 'type', 'metadata_name', 'metadata_graph', 'metadata_map'])

    def test_dataset_discovery_get_datasets_with_timeseries(self):
        self.assertListEqual(list(self.discovery.get_datasets_with_timeseries()["id"]),
        ['ea_bathing_water', 'edm', 'ea_lf_sonde', 'ea_water_quality', 'ea_wq_sonde', 'fft', 'rainfall', 'freshwater_watch', 'wtrt', 'thames_initiative'])

    def test_dataset_discovery_get_datasets_for_date(self):
        self.assertListEqual(list(self.discovery.get_datasets_with_data_for_date()["id"]),
        ['edm', 'ea_flood_warnings', 'ea_lf_sonde', 'rainfall'])

if __name__ == '__main__':
    unittest.main()
