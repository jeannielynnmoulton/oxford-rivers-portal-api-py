from pathlib import Path

from src.oxrivers_api.models.request_models import Request


class AbstractStorage:
    """For future possibility of extending to other storage mechanisms"""

    def create_endpoint_folder(self, request: Request) -> Path:
        raise NotImplementedError

    def get_endpoint_json_filepath(self, request: Request):
        raise NotImplementedError

    def json_file_exists(self, request: Request):
        raise NotImplementedError

    def write(self, response, filepath: Path):
        raise NotImplementedError