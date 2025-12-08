import pandas as pd

from src.oxrivers_api.loader import Loader


class AbstractData:

    loader: Loader
    df: pd.DataFrame

    def __init__(self, loader):
        self.loader = loader

    def as_pandas(self):
        return self.df