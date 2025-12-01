from src.oxrivers_api.storage import Storage


class OxfordRiversClient:
    """Responsible for getting JSON from the API.
    JSON is stored """

    storage: Storage
    BASE_URL: str = "https://oxfordrivers.ceh.ac.uk/"

    def __init__(self, data_dir):
        self.storage = Storage(data_dir)



