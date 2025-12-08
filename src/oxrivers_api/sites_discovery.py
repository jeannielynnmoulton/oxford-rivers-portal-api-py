import logging

import pandas as pd
from shapely import Point
from src.oxrivers_api.loader import Loader
import geopandas as gpd


class SitesDiscovery:

    loader: Loader
    datasetID: str
    sites: pd.DataFrame

    crs_meters = "EPSG:27700"  # British National Grid (BNG)
    crs_lat_lon = "EPSG:4326"  # Standard Latitude and Longitude


    def __init__(self, loader, datasetID):
        self.loader = loader
        self.datasetID = datasetID
        self.sites = loader.load_sites(datasetID)

    def get_ids(self):
        ids = self.sites["id"]
        logging.info(ids)
        return ids

    def get_columns(self):
        columns = list(self.sites.columns)
        logging.info(self.sites.columns)
        logging.info(columns)
        return columns

    def get_sites_info(self):
        result = self.sites[["properties_id", "properties_name"]]
        logging.info(result)
        return result

    def get_closest_sites_to(self, lon_lat: tuple[float, float] , num: int=10):
        lon, lat = lon_lat
        gdf_sites = gpd.GeoDataFrame(
            self.sites,
            geometry=gpd.points_from_xy(self.sites["lon"], self.sites["lat"]),
            crs=self.crs_lat_lon
        ).to_crs(self.crs_meters)
        ref_point = (
            gpd.GeoSeries([Point(lon, lat)], crs=self.crs_lat_lon)
            .to_crs(self.crs_meters)
            .iloc[0]
        )
        distance_col = "distance_from_ref"
        gdf_sites[distance_col] = gdf_sites.geometry.distance(ref_point)
        return_columns = self.get_columns()
        return_columns.append(distance_col)
        return gdf_sites.sort_values(distance_col)[return_columns].head(num)