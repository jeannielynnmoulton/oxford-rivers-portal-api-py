from logging import exception
from pathlib import Path

from src.oxrivers_api.endpoints import Endpoint
from src.oxrivers_api.exceptions import StorageException


class Storage:
    def __init__(self, data_dir: Path):
        self.data_dir : Path = Path(data_dir).resolve()

    @staticmethod
    def create_folder(folder_path: Path):
        abs_path = folder_path.resolve()
        try:
            abs_path.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            print(f"You do not have permission to make directory {folder_path}: {e}")
        except OSError as e:
            print(f"There was an operating system error trying to make directory {folder_path}: {e}")
        except Exception as e:
            print(f"Unexpected error creating directory {folder_path}: {e}")

    def create_data_folder(self) -> Path:
        self.create_folder(self.data_dir)
        print(f"Data storage directory created at {self.data_dir}")
        return self.data_dir

    def get_data_folder_location(self) -> Path:
        return self.data_dir

    def create_endpoint_folder(self, endpoint: Endpoint) -> Path:
        self.create_data_folder()
        endpoint_folder = Path(self.data_dir) / endpoint.value.json_folder
        self.create_folder(endpoint_folder)
        print(f"Endpoint storage directory created at {endpoint_folder}")
        return endpoint_folder