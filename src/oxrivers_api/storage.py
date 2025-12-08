import json
import logging
from dataclasses import fields
from pathlib import Path

from src.oxrivers_api.exceptions import MissingParameterException
from src.oxrivers_api.request_models import Request


class Storage:

    dir_data: Path

    def __init__(self, data_dir: Path):
        self.data_dir : Path = Path(data_dir).resolve()

    @staticmethod
    def create_folder(folder_path: Path):
        abs_path = folder_path.resolve()
        try:
            abs_path.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logging.error(f"You do not have permission to make directory {folder_path}: {e}")
        except OSError as e:
            logging.error(f"There was an operating system error trying to make directory {folder_path}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error creating directory {folder_path}: {e}")

    def create_data_folder(self) -> Path:
        self.create_folder(self.data_dir)
        logging.debug(f"Data storage directory created at {self.data_dir}")
        return self.data_dir

    def get_data_folder_location(self) -> Path:
        return self.data_dir

    def create_endpoint_folder(self, request: Request) -> Path:
        self.create_data_folder()
        endpoint_folder = Path(self.data_dir) / request.json_storage_folder
        self.create_folder(endpoint_folder)
        logging.debug(f"Endpoint storage directory created at {endpoint_folder}")
        return endpoint_folder

    def get_endpoint_json_filepath(self, request: Request):
        endpoint_file_path = self.create_endpoint_folder(request)
        path_suffix = request.json_storage_folder
        for i, f in enumerate(fields(request.request_info)):
            value = getattr(request.request_info, f.name)
            path_suffix += "_" + str(value)
        path_suffix += ".json"
        return endpoint_file_path / path_suffix

    def json_file_exists(self, request: Request, **kwargs):
        return self.get_endpoint_json_filepath(request, **kwargs).exists()

    def write(self, response, filepath: Path):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)