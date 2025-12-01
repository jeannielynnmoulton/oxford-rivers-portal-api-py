import tempfile
import unittest
from pathlib import Path

from src.oxrivers_api.endpoints import Endpoint
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

    def test_endpoint_folders(self):
        for endpoint in Endpoint:
            data_dir: Path = Path(self.tmpdir) / "data"
            storage = Storage(Path(data_dir).resolve())
            endpoint_folder = storage.create_endpoint_folder(endpoint)
            self.assertEqual(endpoint_folder, Path(data_dir).resolve() / endpoint.value.json_folder)



if __name__ == '__main__':
    unittest.main()
