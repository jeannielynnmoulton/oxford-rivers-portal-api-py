from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.storage import Storage

data_dir: str = "../data"
client = OxfordRiversClient(data_dir)
print(client.storage.data_dir)