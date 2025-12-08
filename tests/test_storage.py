import tempfile
import unittest
from pathlib import Path

from src.oxrivers_api.request_models import DatasetRequest, DeterminandRequest, SitesRequest, DataForDateRequest, \
    TimeseriesRequest
from src.oxrivers_api.storage import Storage


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
        storage = Storage(data_dir)
        self.assertEqual(storage.get_data_folder_location(), Path(data_dir).resolve())

    def test_set_data_folder_absolute(self):
        data_dir: Path = Path(self.tmpdir) / "data"
        storage = Storage(Path(data_dir).resolve())
        self.assertEqual(storage.get_data_folder_location(), Path(data_dir).resolve())

    def test_dataset_request_storage(self):
        data_dir = Path(self.tmpdir) / "data"
        storage = Storage(Path(data_dir).resolve())
        requests = [DatasetRequest(), DeterminandRequest(), SitesRequest("dataset"), DataForDateRequest("site", "2025-05-05"), TimeseriesRequest("dataset", "site"), TimeseriesRequest("dataset", "site", "determinand")]
        for request in requests:
            endpoint_folder = storage.create_endpoint_folder(request)
            self.assertEqual(endpoint_folder, Path(data_dir).resolve() / request.json_storage_folder)

if __name__ == '__main__':
    unittest.main()
