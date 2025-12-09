import unittest
from pathlib import Path

from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from oxrivers_api.models.request_models import DatasetsRequest, DeterminandsRequest, SitesRequest, \
    DataForDateRequest, TimeseriesRequest, SitesInfo, TimeseriesInfo, DataForDateInfo
from oxrivers_api.storage.json_storage import LocalJsonStorage


class TestLoader(unittest.TestCase):

    data_dir = Path("./tests/data")
    storage = LocalJsonStorage(data_dir)
    client = APIToJson(storage)
    loader = JsonToPandasLoader(client)

    def test_load_datasets(self):
        request = DatasetsRequest()
        result = self.loader.load(request)
        self.assertListEqual(
            list(result.columns),
            ['id', 'name', 'group', 'type', 'metadata_name', 'metadata_graph', 'metadata_map']
        )
        self.assertEqual(len(result), 11)

    def test_load_determinands(self):
        request = DeterminandsRequest()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns), ['name', 'description', 'datasets'])
        self.assertEqual(len(result), 29)

    def test_load_sites(self):
        datasetID = "fft"
        request = SitesInfo(datasetID).request()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns), ['geometry_coordinates', 'properties_id', 'properties_name', 'properties_threshold', 'properties_popserved', 'lon', 'lat'])
        self.assertEqual(len(result), 17)

    def test_load_timeseries(self):
        datasetID = "fft"
        siteID = "Oxford"
        request = TimeseriesInfo(datasetID, siteID).request()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns),
                             ['datetime', 'value', 'qualifier', 'id', 'siteID', 'endPoint', 'determinand', 'determinand_label', 'determinand_unit'])
        self.assertEqual(len(result), 35040)

    def test_load_data_for_date(self):
        datasetID = "rainfall"
        date = "2024-07-31"
        request = DataForDateInfo(datasetID, date).request()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns),['datetime', 'value', 'id'])
        self.assertEqual(len(result), 129)

    def test_load_timeseries_determinand(self):
        datasetID = "ea_wq_sonde"
        siteID = "E01612A"
        determinand = "fdom"
        request = TimeseriesInfo(datasetID, siteID, determinand).request()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns),
                             ['datetime', 'value', 'qualifier', 'id', 'siteID', 'endPoint', 'determinand', 'determinand_label', 'determinand_unit'])
        self.assertEqual(len(result), 3683)

    def test_load_timeseries_determinand_dict(self):
        datasetID = "ea_bathing_water"
        siteID = "11946"
        determinand = "EC"
        request = TimeseriesInfo(datasetID, siteID, determinand).request()
        result = self.loader.load(request)
        self.assertListEqual(list(result.columns),
                             ['datetime', 'record date', 'escherichia coli count',
                              'escherichia coli qualifier', 'intestinal enterococci count',
                              'intestinal enterococci qualifier', 'id', 'siteID', 'endPoint',
                              'determinand', 'determinand_label', 'determinand_unit'])
        self.assertEqual(len(result), 78)

if __name__ == '__main__':
    unittest.main()
