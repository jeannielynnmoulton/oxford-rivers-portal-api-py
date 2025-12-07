import pandas as pd

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.loader import Loader


class DatasetsDiscovery:

    loader: Loader
    datasets: pd.DataFrame

    def __init__(self, loader):
        self.loader = loader
        self.datasets = loader.load_datasets()

    def get_ids(self):
        ids = self.datasets["id"]
        print(ids)
        return ids

    def get_columns(self):
        columns = list(self.datasets.columns)
        print(self.datasets.columns)
        print(columns)
        return columns

    def get_datasets_with_timeseries(self):
        result = self.datasets[self.datasets["metadata_graph"] == True]
        print(result)
        return result

    def get_datasets_with_data_for_date(self):
        result = self.datasets.loc[self.datasets["metadata_map"] == True]
        print(result)
        return result

    def get_datasets_info(self):
        result = self.datasets[["id", "name", "metadata_name"]]
        print(result)
        return result

if __name__ == '__main__':
    client = OxfordRiversClient("../../data")
    loader = Loader(client)
    discovery = DatasetsDiscovery(loader)
    discovery.get_ids()
    discovery.get_columns()
    discovery.get_datasets_with_timeseries()
    discovery.get_datasets_with_data_for_date()
    discovery.get_datasets_info()
