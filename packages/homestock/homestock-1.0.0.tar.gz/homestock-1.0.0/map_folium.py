#!/usr/bin/env python
# coding: utf-8

# In[1]:

import folium
from folium.plugins import SideBySideLayers
from localtileserver import get_folium_tile_layer


class Map:
    """
    A simple wrapper around folium.Map to provide custom mapping utilities
    including split-pane raster visualization using localtileserver.

    Attributes
    ----------
    map : folium.Map
        The folium Map object.
    """

    def __init__(self, location=[0, 0], zoom_start=2, **kwargs):
        """
        Initialize the map with a given location and zoom level.

        Parameters
        ----------
        location : list, optional
            Initial center of the map [latitude, longitude] (default is [0, 0]).
        zoom_start : int, optional
            Initial zoom level (default is 2).
        kwargs : dict
            Additional keyword arguments passed to folium.Map.
        """
        self.map = folium.Map(location=location, zoom_start=zoom_start, **kwargs)

    def add_split_map(self, left_raster_path, right_raster_path, left_name='Left Layer', right_name='Right Layer'):
        """
        Add a split-pane viewer to the map for comparing two raster datasets.

        This uses the Folium SideBySideLayers plugin along with the localtileserver
        get_folium_tile_layer function to visualize two GeoTIFFs or tile layers side by side.

        Parameters
        ----------
        left_raster_path : str
            File path to the left raster dataset (e.g., GeoTIFF).
        right_raster_path : str
            File path to the right raster dataset (e.g., GeoTIFF).
        left_name : str, optional
            Display name for the left raster layer (default is 'Left Layer').
        right_name : str, optional
            Display name for the right raster layer (default is 'Right Layer').

        Returns
        -------
        folium.Map
            The map object with the split-pane layer added.
        """
        # Generate tile layers for both rasters
        left_layer = get_folium_tile_layer(left_raster_path, name=left_name)
        right_layer = get_folium_tile_layer(right_raster_path, name=right_name)

        # Add them to the map
        left_layer.add_to(self.map)
        right_layer.add_to(self.map)

        # Add split map control
        split_control = SideBySideLayers(left_layer, right_layer)
        self.map.add_child(split_control)

        return self.map


