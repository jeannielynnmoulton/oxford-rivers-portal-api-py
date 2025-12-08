import logging
import pandas as pd

from src.oxrivers_api.loader import Loader


class DatasetsDiscovery:

    loader: Loader
    datasets: pd.DataFrame

    def __init__(self, loader):
        self.loader = loader
        self.datasets = loader.load_datasets()

    def get_ids(self):
        ids = self.datasets["id"]
        logging.info(ids)
        return ids

    def get_columns(self):
        columns = list(self.datasets.columns)
        logging.info(columns)
        return columns

    def get_datasets_with_timeseries(self):
        result = self.datasets[self.datasets["metadata_graph"] == True]
        logging.info(result)
        return result

    def get_datasets_with_data_for_date(self):
        result = self.datasets.loc[self.datasets["metadata_map"] == True]
        logging.info(result)
        return result

    def get_datasets_info(self):
        result = self.datasets[["id", "name", "metadata_name"]]
        logging.info(result)
        return result
