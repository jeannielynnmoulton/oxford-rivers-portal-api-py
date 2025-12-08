import logging

import pandas as pd

from src.oxrivers_api.loader import Loader


class DeterminandsDiscovery:

    loader: Loader
    determinands: pd.DataFrame

    def __init__(self, loader):
        self.loader = loader
        self.determinands = loader.load_determinands()

    def get_ids(self):
        ids = list(self.determinands["name"])
        logging.info(ids)
        return ids

    def get_columns(self):
        columns = list(self.determinands.columns)
        logging.info(columns)
        return columns

    def get_determinands_info(self):
        result = self.determinands[["name", "description"]]
        logging.info(result)
        return result

    def get_datasets_with_determinand(self, determinand: str):
        if determinand not in self.get_ids():
            raise Exception(f"Invalid determinand name {determinand}")
        result = (
            self.determinands.loc[self.determinands["name"]==determinand, "datasets"]
                .explode()
                .apply(pd.Series)
                .reset_index(drop=True)
        )
        result.columns = ["dataset", "id"]
        logging.info(result)
        return result