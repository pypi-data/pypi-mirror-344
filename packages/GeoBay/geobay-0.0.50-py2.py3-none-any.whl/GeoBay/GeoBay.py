# Main module.

from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl, ImageOverlay, SearchControl, VideoOverlay, WMSLayer, WidgetControl, CircleMarker, MarkerCluster, Polyline, SplitMapControl, Marker
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display
import leafmap

class CustomIpyleafletMap(IpyleafletMap):
    """
    A custom wrapper around ipyleaflet.Map with additional helper methods
    for adding basemaps, vector data, raster layers, images, videos, and WMS layers.
    """

    def __init__(self, center, zoom=12, **kwargs):
        """
        Initialize the custom map.

        Args:
            center (tuple): Latitude and longitude of the map center.
            zoom (int, optional): Zoom level of the map. Defaults to 12.
            **kwargs: Additional keyword arguments for ipyleaflet.Map.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_basemap(self, basemap_name: str):
        """
        Add a basemap layer to the map.

        Args:
            basemap_name (str): Name of the basemap ('OpenStreetMap', 'Esri.WorldImagery', or 'OpenTopoMap').

        Raises:
            ValueError: If the basemap name is not supported.
        """
        basemap_urls = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Esri.WorldImagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
        }

        if basemap_name not in basemap_urls:
            raise ValueError(f"Basemap '{basemap_name}' is not supported.")

        basemap = TileLayer(url=basemap_urls[basemap_name])
        self.add_layer(basemap)
        
    def add_basemap_gui(self, options=None, position="topright"):    
        """
        Adds a graphical user interface (GUI) for selecting basemaps.

        Args:
            -options (list, optional): A list of basemap options to display in the dropdown.
               ["OpenStreetMap.Mapnik", "OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"].
            -position (str, optional): The position of the widget on the map. Defaults to "topright".

        Behavior:
            - A toggle button is used to show or hide the dropdown and close button.
            - The dropdown allows users to select a bsemap from the provided options.
            - The close button hides the widget from the map.

        Event Handlers:
            - `on_toggle_change`: Toggles the visibility of the dropdown and close button.
            - `on_button_click`: Closes the widget when button is clicked
            - `on_dropdown_change`: Updates the basemap when a new option is selected.
        """
        if options is None:
            options = [
                "OpenStreetMap.Mapnik",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "CartoDB.DarkMatter",
            ]

        toggle = widgets.ToggleButton(
            value=True,
            button_style="",
            tooltip="Click me",
            icon="map",
        )
        toggle.layout = widgets.Layout(width="38px", height="38px")

        dropdown = widgets.Dropdown(
            options=options,
            value=options[0],
            description="Basemap:",
            style={"description_width": "initial"},
        )
        dropdown.layout = widgets.Layout(width="250px", height="38px")

        button = widgets.Button(
            icon="times",
        )
        button.layout = widgets.Layout(width="38px", height="38px")

        hbox = widgets.HBox([toggle, dropdown, button])

        def on_toggle_change(change):
            if change["new"]:
                hbox.children = [toggle, dropdown, button]
            else:
                hbox.children = [toggle]

        toggle.observe(on_toggle_change, names="value")

        def on_button_click(b):
            hbox.close()
            toggle.close()
            dropdown.close()
            button.close()

        button.on_click(on_button_click)

        def on_dropdown_change(change):
            if change["new"]:
                self.layers = self.layers[:-2]
                self.add_basemap(change["new"])

        dropdown.observe(on_dropdown_change, names="value")

        control = WidgetControl(widget=hbox, position=position)
        self.add(control)

    def add_widget(self, widget, position="topright", **kwargs):
        """Add a widget to the map.

        Args:
            widget (ipywidgets.Widget): The widget to add.
            position (str, optional): Position of the widget. Defaults to "topright".
            **kwargs: Additional keyword arguments for the WidgetControl.
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position, **kwargs)
        self.add(control)
        
    def add_layer_control(self):
        """
        Add a control to toggle map layers on and off.
        """
        control = LayersControl()
        self.add_control(control)

    def add_vector(self, vector_data):
        """
        Add a vector layer to the map from a file path or GeoDataFrame.

        Args:
            vector_data (str or geopandas.GeoDataFrame): Path to a vector file or a GeoDataFrame.

        Raises:
            ValueError: If the input is not a valid file path or GeoDataFrame.
        """
        if isinstance(vector_data, str):
            gdf = gpd.read_file(vector_data)
        elif isinstance(vector_data, gpd.GeoDataFrame):
            gdf = vector_data
        else:
            raise ValueError("Input must be a file path or a GeoDataFrame.")

        geo_json_data = gdf.__geo_interface__
        geo_json_layer = GeoJSON(data=geo_json_data)
        self.add_layer(geo_json_layer)

    def add_raster(self, url, name=None, colormap=None, opacity=1.0):
        """
        Add a raster tile layer to the map.

        Args:
            url (str): URL template for the raster tiles.
            name (str, optional): Layer name. Defaults to "Raster Layer".
            colormap (optional): Colormap to apply (not used here but reserved).
            opacity (float, optional): Opacity of the layer (0.0 to 1.0). Defaults to 1.0.
        """
        tile_layer = TileLayer(
            url=url,
            name=name or "Raster Layer",
            opacity=opacity
        )
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        """
        Add an image overlay to the map.

        Args:
            url (str): URL of the image.
            bounds (list): Bounding box of the image [[south, west], [north, east]].
            opacity (float, optional): Opacity of the image. Defaults to 1.0.
        """
        image_layer = ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(image_layer)

    def add_video(self, url, bounds, opacity=1.0):
        """
        Add a video overlay to the map.

        Args:
            url (str): URL of the video.
            bounds (list): Bounding box for the video [[south, west], [north, east]].
            opacity (float, optional): Opacity of the video. Defaults to 1.0.
        """
        video_layer = VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name=None, format='image/png', transparent=True, **extra_params):
        """
        Add a WMS (Web Map Service) layer to the map.

        Args:
            url (str): WMS base URL.
            layers (str): Comma-separated list of layer names.
            name (str, optional): Display name for the layer. Defaults to "WMS Layer".
            format (str, optional): Image format. Defaults to 'image/png'.
            transparent (bool, optional): Whether the background is transparent. Defaults to True.
            **extra_params: Additional parameters to pass to the WMSLayer.
        """
        wms_layer = WMSLayer(
            url=url,
            layers=layers,
            name=name or "WMS Layer",
            format=format,
            transparent=transparent,
            **extra_params
        )
        self.add_layer(wms_layer)

    def show_map(self):
        """
        Display the map in a Jupyter notebook or compatible environment.

        Returns:
            ipyleaflet.Map: The configured map.
        """
        return self

    def add_search_control(self, position="topleft", zoom=10):
        """
        Add a search bar to the map using Nominatim geocoder.
        """
        search = SearchControl(
            position=position,
            url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
            zoom=zoom,
            marker=Marker()  # ✅ Provide a valid Marker object
        )
        self.add_control(search)

    
    def add_esa_worldcover(self, position="bottomright"):
        """
        Adds the ESA World Cover 2021 WMS layer and its legend to the map.

        Args:
            position (str): Position of the legend on the map. Defaults to "bottomright".
        """
        import ipywidgets as widgets
        from ipyleaflet import WMSLayer, WidgetControl
        import leafmap

        # Add ESA WorldCover WMS layer
        esa_layer = WMSLayer(
            url="https://services.terrascope.be/wms/v2?",
            layers="WORLDCOVER_2021_MAP",
            name="ESA WorldCover 2021",
            transparent=True,
            format="image/png"
        )
        self.add_layer(esa_layer)

        # Get ESA legend from leafmap's built-in legends
        legend_html = leafmap.legend_builtin['ESA_WorldCover']
        legend_widget = widgets.HTML(value=legend_html)
        legend_control = WidgetControl(widget=legend_widget, position=position)
        self.add_control(legend_control)

    def add_circle_markers_from_xy(self, gdf, radius=5, color="red", fill_color="yellow", fill_opacity=0.8):
        """
        Add circle markers from a GeoDataFrame with lat/lon columns using MarkerCluster.

        Args:
            gdf (GeoDataFrame): Must contain 'latitude' and 'longitude' columns.
            radius (int): Radius of each marker.
            color (str): Outline color.
            fill_color (str): Fill color.
            fill_opacity (float): Fill opacity.
        """
        if 'latitude' not in gdf.columns or 'longitude' not in gdf.columns:
            raise ValueError("GeoDataFrame must contain 'latitude' and 'longitude' columns")

        markers = []
        for _, row in gdf.iterrows():
            marker = CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=radius,
                color=color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke=True
            )
            markers.append(marker)

        cluster = MarkerCluster(markers=markers)
        self.add_layer(cluster)

    def add_choropleth(self, url, column, colormap="YlOrRd"):
        """
        Simulate a choropleth using GeoJSON layer and dynamic styling.

        Args:
            url (str): GeoJSON file URL.
            column (str): Attribute column to color by.
            colormap (str): Color ramp name (from branca.colormap).
        """
        import branca.colormap as cm
        import json

        gdf = gpd.read_file(url)
        gdf = gdf.to_crs("EPSG:4326")
        gdf["id"] = gdf.index.astype(str)

        values = gdf[column]
        cmap = cm.linear.__getattribute__(colormap).scale(values.min(), values.max())

        def style_dict(feature):
            value = gdf.loc[int(feature['id']), column]
            return {
                'fillColor': cmap(value),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.7
            }

        geo_json = json.loads(gdf.to_json())
        layer = GeoJSON(data=geo_json, style=style_dict, name="Choropleth")
        self.add_layer(layer)

    def add_split_map(self, pre_url, post_url, name_pre="Pre-event", name_post="Post-event"):
        """
        Add a split map control to compare pre- and post-event imagery.

        Args:
            pre_url (str): URL template for pre-event tile imagery.
            post_url (str): URL template for post-event tile imagery.
            name_pre (str): Optional label for pre-event imagery.
            name_post (str): Optional label for post-event imagery.
        """
        pre_layer = TileLayer(url=pre_url, name=name_pre)
        post_layer = TileLayer(url=post_url, name=name_post)

        split_control = SplitMapControl(left_layer=pre_layer, right_layer=post_layer)
        self.add_control(split_control)

    def add_building_polygons(self, url):
        """
        Add building polygons with red outline and no fill.
        """
        gdf = gpd.read_file(url)
        geo_json = gdf.__geo_interface__

        style = {
            "color": "red",
            "weight": 1,
            "fill": False,
            "fillOpacity": 0.0
        }

        self.add_layer(GeoJSON(data=geo_json, style=style, name="Buildings"))
        
    def add_roads(self, url):
        """
        Add road polylines with red color and width 2.
        """
        gdf = gpd.read_file(url)
        geo_json = gdf.__geo_interface__

        style = {
            "color": "red",
            "weight": 2,
            "opacity": 1.0
        }

        self.add_layer(GeoJSON(data=geo_json, style=style, name="Roads"))
    
