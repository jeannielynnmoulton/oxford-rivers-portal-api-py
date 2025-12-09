import tempfile
import unittest
from pathlib import Path

from src.oxrivers_api.models.request_models import SitesInfo, DataForDateInfo, TimeseriesInfo, DatasetsInfo, DeterminandInfo
from src.oxrivers_api.storage.json_storage import JSONStorage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.tmpdir_obj = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmpdir_obj.name)
        self.assertTrue(Path(self.tmpdir).exists())

    def tearDown(self):
        self.tmpdir_obj.cleanup()
        self.assertFalse(Path(self.tmpdir).exists())

    def test_set_data_folder_relative(self):
        data_dir: Path = Path(self.tmpdir) / "data"
        storage = JSONStorage(data_dir)
        self.assertEqual(storage._get_data_folder_location(), Path(data_dir).resolve())

    def test_set_data_folder_absolute(self):
        data_dir: Path = Path(self.tmpdir) / "data"
        storage = JSONStorage(Path(data_dir).resolve())
        self.assertEqual(storage._get_data_folder_location(), Path(data_dir).resolve())

    def test_dataset_request_storage(self):
        data_dir = Path(self.tmpdir) / "data"
        storage = JSONStorage(Path(data_dir).resolve())
        requests = [DatasetsInfo().request(), DeterminandInfo().request(), SitesInfo("dataset").request(), DataForDateInfo("site", "2025-05-05").request(), TimeseriesInfo("dataset", "site").request(), TimeseriesInfo("dataset", "site", "determinand").request() ]
        for request in requests:
            endpoint_folder = storage.create_endpoint_folder(request)
            self.assertEqual(endpoint_folder, Path(data_dir).resolve() / request.json_storage_folder)

if __name__ == '__main__':
    unittest.main()
