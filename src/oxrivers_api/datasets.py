import pandas as pd

from src.oxrivers_api.AbstractData import AbstractData
from src.oxrivers_api.loader import Loader


class Datasets(AbstractData):

    def __init__(self, loader):
        super().__init__(loader)
        self.loader.load_datasets()

    def ids(self):
        return