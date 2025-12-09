import pandas as pd

from src.oxrivers_api.loader import Loader
from src.oxrivers_api.request_models import TimeseriesInfo, DataForDateInfo, RequestInfo, DeterminandInfo, DatasetsInfo, \
    SitesInfo, SitesRequest, DatasetRequest, DeterminandRequest

class DataCache:
    """A utility for getting and storing data from the Oxford Rivers API.
    Automatically stores all dataset, sites and determinand data.
    Provides functions for getting and storing timeseries and data for date,
    including a user-friendly naming scheme.

    # Example usage to get and store time series data for fft in Oxford:
    loader = Loader("./data")
    cache = DataCache(loader)
    cache.get_timeseries(TimeseriesInfo("fft", "Oxford"))
    cache.get_data_for_date(DataForDateInfo("rainfall", "2025-05-05"))

    # list contents in cache
    print(contents)
    """

    loader: Loader

    datasets: pd.DataFrame
    determinands: pd.DataFrame
    sites: dict[str, pd.DataFrame]
    timeseries: dict[str, pd.DataFrame]
    dates: dict[str, pd.DataFrame]

    key_to_info: dict[str, RequestInfo]

    def __init__(self, loader):
        self.loader = loader
        self.datasets = loader.load(DatasetRequest())
        self.determinands = loader.load(DeterminandRequest())
        self.sites = {datasetID: loader.load(SitesRequest(SitesInfo(datasetID))) for datasetID in self.datasets["id"]}
        self.timeseries = {}
        self.dates = {}
        self.key_to_info = {}

    def get_timeseries(self, info: TimeseriesInfo, key: str = None) -> pd.DataFrame:
        """
        Retrieve and store time-series data for a given dataset, site and
        determinand (not required for all datasets).

        This method loads time-series data based on the parameters in a
        ``TimeseriesInfo`` object. The resulting DataFrame is cached under a
        unique string key so it may be retrieved later without reloading.

        If ``key`` is not provided, a descriptive key is automatically
        generated in the readable form:
            ``<datasetID>:<site_name>:<determinand_name>``

        Parameters
        ----------
        info : TimeseriesInfo
            Object containing dataset ID, site ID, and determinand code used
            to fetch the appropriate time-series data.
        key : str, optional
            While the default key is human-readable, you can provide
            a unique identifier under which the time-series will be stored.
            If provided, it must not collide with an existing key.

        Returns
        -------
        pandas.DataFrame
            The loaded time-series data.

        Raises
        ------
        Exception
            If ``key`` is provided and already exists in the time-series store.
        """
        if key is not None and key in self.timeseries.keys():
            raise Exception(f"Key {key} already exists for timeseries. Choose a unique key.")
        if key is None:
            sites_df = self.sites[info.datasetID]
            sites_name: str = "_".join(sites_df[sites_df["properties_id"] == info.siteID]["properties_name"].iloc[0].split(" "))
            print(sites_name)
            determinand_name: str = self._lookup_determinand_name(info.datasetID, info.determinand)
            key = ":".join([info.datasetID, sites_name, determinand_name])
        self.key_to_info[key] = info
        self.timeseries[key] = self.loader.load_timeseries(info)
        return self.timeseries[key]

    def get_data_for_date(self, info: DataForDateInfo, key: str = None) -> pd.DataFrame:
        """
        Retrieve and store measurement data for a dataset and date.

        This method loads measurement data for a given dataset and date.
        The result is stored under a unique key based on the provided
        ``DataForDateInfo``.

        If ``key`` is not provided, a default key is generated in the form:
            ``<datasetID>_<date>``

        Parameters
        ----------
        info : DataForDateInfo
            Object containing the dataset ID and date for which measurements
            should be fetched.
        key : str, optional
            While the default key is human-readable, you can provide
            a unique identifier under which the time-series will be stored.
            If provided, it must not collide with an existing key.

        Returns
        -------
        pandas.DataFrame
            The loaded daily measurement data.

        Raises
        ------
        Exception
            If ``key`` is provided and already exists in the date-based store.
        """
        if key is not None and key in self.dates.keys():
            raise Exception(f"Key {key} already exists for data for date. Choose a unique key.")
        if key is None:
            key = "_".join([info.datasetID, info.date])
        self.key_to_info[key] = info
        self.timeseries[key] = self.loader.load_data_for_date(info)
        return self.timeseries[key]

    def contents(self):
        """
        Return a mapping of all stored keys to their corresponding request info.

        This method returns the internal dictionary that records which
        ``RequestInfo`` object was used to load each stored dataset
        (time-series or date-based).

        Returns
        -------
        dict[str, RequestInfo]
            Mapping from storage keys to the ``RequestInfo`` objects that
            describe each dataset.
        """
        return self.key_to_info

    def get_by_key(self, key: str):
        if key not in self.key_to_info.keys():
            raise Exception(f"Key {key} does not exist.")
        if key in self.timeseries.keys():
            return self.timeseries[key]
        else:
            return self.dates[key]

    def _lookup_determinand_name(self, datasetID: str, determinand: str) -> str | None:
            for _, row in self.determinands.iterrows():
                for d in row["datasets"]:
                    if d["code"] == datasetID and d["id"] == determinand:
                        return "_".join(row["name"].split(" "))
            return "None"
