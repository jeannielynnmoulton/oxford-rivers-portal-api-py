import pandas as pd

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.datasets_discovery import DatasetsDiscovery
from src.oxrivers_api.loader import Loader


class SitesDiscovery:

    loader: Loader
    datasetID: str
    sites: pd.DataFrame

    def __init__(self, loader, datasetID):
        self.loader = loader
        self.datasetID = datasetID
        self.sites = loader.load_sites(datasetID)

    def get_ids(self):
        ids = self.sites["id"]
        print(ids)
        return ids

    def get_columns(self):
        columns = list(self.sites.columns)
        print(self.sites.columns)
        print(columns)
        return columns

    def get_sites_info(self):
        result = self.sites[["properties_id", "properties_name"]]
        print(result)
        return result

if __name__ == '__main__':
    client = OxfordRiversClient("../../data")
    loader = Loader(client)
    dataset_discovery = DatasetsDiscovery(loader)
    datasets = dataset_discovery.get_ids()
    site_discovery_list = []
    for datasetID in datasets:
        print(datasetID)
        site_discovery = SitesDiscovery(loader, datasetID)
        info = site_discovery.get_sites_info()
        site_discovery_list.append(info)
        print(info.to_string())