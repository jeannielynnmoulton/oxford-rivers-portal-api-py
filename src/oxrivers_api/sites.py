import pandas as pd

from src.oxrivers_api.loader import Loader


class Sites:
    loader: Loader
    df: pd.DataFrame

    def __init__(self):
        loader: Loader
        df: pd.DataFrame

