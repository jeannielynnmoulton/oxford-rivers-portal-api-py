import pandas as pd

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.loader import Loader


class DeterminandsDiscovery:

    loader: Loader
    determinands: pd.DataFrame

    def __init__(self, loader):
        self.loader = loader
        self.determinands = loader.load_determinands()

    def get_ids(self):
        ids = list(self.determinands["name"])
        print(ids)
        return ids

    def get_columns(self):
        columns = list(self.determinands.columns)
        print(self.determinands.columns)
        print(columns)
        return columns

    def get_determinands_info(self):
        result = self.determinands[["name", "description"]]
        print(result)
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
        print(result)
        return result

# if __name__ == '__main__':
#     client = OxfordRiversClient("../../data")
#     loader = Loader(client)
#     discovery = DeterminandsDiscovery(loader)
#     print(discovery.determinands)
#     discovery.get_ids()
#     discovery.get_columns()
#     discovery.get_determinands_info()
#     discovery.get_datasets_with_determinand("Escherichia coli (EC)")