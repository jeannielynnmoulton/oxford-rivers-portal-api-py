import unittest

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.loader import Loader


class MyTestCase(unittest.TestCase):
    def test_load_datasets(self):
        client = OxfordRiversClient("./tests/data")
        client.getDatasets()
        loader = Loader(client.storage)
        result = loader.load_datasets()
        self.assertListEqual(
            list(result.columns),
            ['id', 'name', 'group', 'type', 'metadata_name', 'metadata_graph', 'metadata_map']
        )
        self.assertEqual(len(result), 11)

    def test_load_determinands(self):
        client = OxfordRiversClient("./tests/data")
        client.getDeterminands()
        loader = Loader(client.storage)
        result = loader.load_determinands()
        self.assertListEqual(list(result.columns), ['name', 'description', 'datasets'])
        self.assertEqual(len(result), 29)

    def test_load_sites(self):
        datasetID = "fft"
        client = OxfordRiversClient("./tests/data")
        client.getSites(datasetID)
        loader = Loader(client.storage)
        result = loader.load_sites(datasetID)
        self.assertListEqual(list(result.columns), ['geometry_coordinates', 'properties_id', 'properties_name', 'properties_threshold', 'properties_popserved', 'lon', 'lat'])
        self.assertEqual(len(result), 17)

    def test_load_timeseries(self):
        datasetID = "fft"
        siteID = "Oxford"
        client = OxfordRiversClient("./tests/data")
        client.getTimeseries(datasetID, siteID)
        loader = Loader(client.storage)
        result = loader.load_timeseries(datasetID, siteID)
        self.assertListEqual(list(result.columns),
                             ['datetime', 'value', 'id', 'siteID', 'endPoint', 'determinand', 'determinand_label', 'determinand_unit'])
        self.assertEqual(len(result), 35040)

    def test_load_timeseries_determinand(self):
        datasetID = "ea_wq_sonde"
        siteID = "E01612A"
        determinand = "fdom"
        client = OxfordRiversClient("./tests/data")
        client.getTimeseriesDeterminand(datasetID, siteID, determinand)
        loader = Loader(client.storage)
        result = loader.load_timeseries_determinand(datasetID, siteID, determinand)
        self.assertListEqual(list(result.columns),
                             ['datetime', 'value', 'id', 'siteID', 'endPoint', 'determinand', 'determinand_label', 'determinand_unit'])
        self.assertEqual(len(result), 3683)


if __name__ == '__main__':
    unittest.main()
