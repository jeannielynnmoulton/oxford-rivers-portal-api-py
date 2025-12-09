import pandas as pd

from oxrivers_api.models.request_models import SitesInfo, TimeseriesInfo, DataForDateInfo, Request


class AbstractLoader:
    def load(self, request: Request):
        """Convenience method for loading from the Request"""
        raise NotImplemented

    def load_datasets(self) -> pd.DataFrame:
        raise NotImplemented

    def load_determinands(self) -> pd.DataFrame:
        raise NotImplemented

    def load_sites(self, info: SitesInfo) -> pd.DataFrame:
        raise NotImplemented

    def load_timeseries(self, info: TimeseriesInfo) -> pd.DataFrame:
        raise NotImplemented

    def load_data_for_date(self, info: DataForDateInfo) -> pd.DataFrame:
        raise NotImplemented