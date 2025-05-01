"""Main module."""
from ipyleaflet import Map as IpyleafletMap, basemaps, basemap_to_tiles, LayersControl, GeoData
import geopandas as gpd
import os

class Map(IpyleafletMap):
    """
    A custom map class for the homestock package, extending ipyleaflet.Map
    with support for basemaps, layer control, and vector data display.
    """

    def add_basemap(self, basemap_name: str):
        """
        Add a basemap to the map using a specified name.
        
        Parameters:
        ----------
        basemap_name : str
            Name of the basemap. Supported names include:
            "OpenStreetMap", "Esri.WorldImagery", "OpenTopoMap", etc.

        Returns:
        -------
        None
        """
        try:
            if "." in basemap_name:
                provider, variant = basemap_name.split(".")
                basemap = getattr(getattr(basemaps, provider), variant)
            else:
                basemap = getattr(basemaps, basemap_name)
            tile_layer = basemap_to_tiles(basemap)
            self.add_layer(tile_layer)
        except AttributeError:
            raise ValueError(f"Basemap '{basemap_name}' not recognized.")

    def add_layer_control(self):
        """
        Add a layer control widget to the map.

        This widget allows users to toggle the visibility of different layers.

        Returns:
        -------
        None
        """
        self.add_control(LayersControl(position="topright"))

    def add_vector(self, data):
        """
        Add vector data to the map. Accepts file paths (GeoJSON, Shapefile) or GeoDataFrames.

        Parameters:
        ----------
        data : str or geopandas.GeoDataFrame
            Path to the vector data file or a GeoDataFrame.

        Returns:
        -------
        None
        """
        if isinstance(data, str):
            if not os.path.exists(data):
                raise FileNotFoundError(f"File '{data}' not found.")
            gdf = gpd.read_file(data)
        elif isinstance(data, gpd.GeoDataFrame):
            gdf = data
        else:
            raise TypeError("Data must be a file path or a GeoDataFrame.")

        geo_data = GeoData(geo_dataframe=gdf, name="Vector Layer")
        self.add_layer(geo_data)
