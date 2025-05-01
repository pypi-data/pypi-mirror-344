"""
Mapbox view widget with 3D map and car model.
"""

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from .. import config


class MapboxView(QWidget):
    """
    Widget that displays a 3D Mapbox map with a car model.

    Features:
    - Interactive 3D map using Mapbox GL JS
    - Vehicle position updating in real-time
    - Vehicle model with correct orientation (heading, pitch, roll)
    - Terrain-based visualization

    Note: Requires a valid Mapbox token set in the config module.
    """

    def __init__(self, parent=None):
        """
        Initialize the Mapbox view widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Current vehicle position and orientation
        self._latitude = 0.0
        self._longitude = 0.0
        self._heading = 0.0
        self._pitch = 0.0
        self._roll = 0.0

        # Map settings
        self._zoom = config.DEFAULT_ZOOM
        self._follow_vehicle = True

        # Set widget properties
        self.setMinimumSize(300, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create layout
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # Check if the token is set
        if config.MAPBOX_TOKEN == "YOUR_MAPBOX_TOKEN_HERE":
            # Token not set, show placeholder instead
            self._setup_placeholder()
        else:
            # Token is set, initialize the Mapbox view
            self._setup_mapbox_view()

    def _setup_placeholder(self):
        """Set up a placeholder for when the Mapbox token is not set."""
        self._placeholder = QLabel(
            "3D Live Mapbox Map with 3D Car Model\n\n"
            "Please set your Mapbox token in config.py to activate this feature."
        )
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet(
            f"color: {config.TEXT_COLOR}; "
            "background-color: #2d2d2d; "
            "border: 1px solid #555; "
            "border-radius: 4px; "
            "padding: 10px;"
        )
        self._layout.addWidget(self._placeholder)

    def _setup_mapbox_view(self):
        """Set up the Mapbox WebEngineView with the map."""
        # Create the WebEngineView
        self._web_view = QWebEngineView()

        # Enable WebGL and other required settings
        settings = self._web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        # Try disabling WebGL hardware acceleration as a potential fix for context errors
        # settings.setAttribute(QWebEngineSettings.WebGLEnabled, False) # Keep enabled for now, try below first

        # Load the initial HTML with the Mapbox map
        html = self._generate_mapbox_html()
        self._web_view.setHtml(html, QUrl("https://api.mapbox.com/"))

        # Add to layout
        self._layout.addWidget(self._web_view)

    def _generate_mapbox_html(self):
        """Generate the HTML for the Mapbox map with the car model."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
            <script src="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js"></script>
            <link href="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css" rel="stylesheet" />
            <style>
                body {{ margin: 0; padding: 0; }}
                #map {{ width: 100%; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                mapboxgl.accessToken = '{config.MAPBOX_TOKEN}';
                
                const map = new mapboxgl.Map({{
                    container: 'map',
                    style: '{config.MAPBOX_STYLE}',
                    center: [{self._longitude}, {self._latitude}],
                    zoom: {self._zoom},
                    pitch: 60,
                    bearing: {self._heading},
                    antialias: true
                }});
                
                // Wait for the map to load
                map.on('load', () => {{
                    // Add 3D buildings and terrain if available on the map style
                    if (map.getStyle().layers) {{
                        const layers = map.getStyle().layers;
                        
                        // Find the index of the first symbol layer in the map style
                        let firstSymbolId;
                        for (const layer of layers) {{
                            if (layer.type === 'symbol') {{
                                firstSymbolId = layer.id;
                                break;
                            }}
                        }}
                        
                        // Add 3D buildings
                        map.addLayer(
                            {{
                                'id': '3d-buildings',
                                'source': 'composite',
                                'source-layer': 'building',
                                'filter': ['==', 'extrude', 'true'],
                                'type': 'fill-extrusion',
                                'minzoom': 15,
                                'paint': {{
                                    'fill-extrusion-color': '#aaa',
                                    'fill-extrusion-height': [
                                        'interpolate',
                                        ['linear'],
                                        ['zoom'],
                                        15, 0,
                                        16, ['get', 'height']
                                    ],
                                    'fill-extrusion-base': [
                                        'interpolate',
                                        ['linear'],
                                        ['zoom'],
                                        15, 0,
                                        16, ['get', 'min_height']
                                    ],
                                    'fill-extrusion-opacity': 0.6
                                }}
                            }},
                            firstSymbolId
                        );
                    }}
                    
                    // Add the car model as a custom marker
                    const el = document.createElement('div');
                    el.className = 'car-marker';
                    el.style.width = '20px';
                    el.style.height = '40px';
                    el.style.backgroundImage = 'url(https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png)';
                    el.style.backgroundSize = 'contain';
                    el.style.backgroundRepeat = 'no-repeat';
                    
                    // Create a marker for the car
                    window.carMarker = new mapboxgl.Marker(el)
                        .setLngLat([{self._longitude}, {self._latitude}])
                        .addTo(map);
                    
                    // Add vehicle heading indicator (optional, more advanced implementation)
                    map.addSource('vehicle-direction', {{
                        'type': 'geojson',
                        'data': {{
                            'type': 'Feature',
                            'properties': {{}},
                            'geometry': {{
                                'type': 'LineString',
                                'coordinates': [
                                    [{self._longitude}, {self._latitude}],
                                    [{self._longitude}, {self._latitude}]  // Will be updated
                                ]
                            }}
                        }}
                    }});
                    
                    map.addLayer({{
                        'id': 'vehicle-direction-line',
                        'type': 'line',
                        'source': 'vehicle-direction',
                        'layout': {{
                            'line-cap': 'round',
                            'line-join': 'round'
                        }},
                        'paint': {{
                            'line-color': '#33ccff',
                            'line-width': 3
                        }}
                    }});
                }});
                
                // Function to update the vehicle position and orientation
                function updateVehicle(longitude, latitude, heading, pitch, roll) {{
                    // Update the car marker position
                    if (window.carMarker) {{
                        window.carMarker.setLngLat([longitude, latitude]);
                        
                        // Update the marker rotation to match the heading
                        window.carMarker.getElement().style.transform = 
                            `rotate(${{heading}}deg) rotateX(${{pitch}}deg) rotateZ(${{roll}}deg)`;
                    }}
                    
                    // Calculate the direction line end point
                    const headingRad = (heading * Math.PI) / 180;
                    const lineLength = 0.001;  // Approx. 100m at equator
                    const endLng = longitude + lineLength * Math.sin(headingRad);
                    const endLat = latitude + lineLength * Math.cos(headingRad);
                    
                    // Update the direction line
                    if (map.getSource('vehicle-direction')) {{
                        map.getSource('vehicle-direction').setData({{
                            'type': 'Feature',
                            'properties': {{}},
                            'geometry': {{
                                'type': 'LineString',
                                'coordinates': [
                                    [longitude, latitude],
                                    [endLng, endLat]
                                ]
                            }}
                        }});
                    }}
                    
                    // If following the vehicle, update the map center
                    if ({str(self._follow_vehicle).lower()}) {{
                        map.setCenter([longitude, latitude]);
                        map.setBearing(heading);
                    }}
                }}
                
                // Expose a function to call from Python
                window.updateVehicleFromPython = (longitude, latitude, heading, pitch, roll) => {{
                    updateVehicle(longitude, latitude, heading, pitch, roll);
                }};
            </script>
        </body>
        </html>
        """
        return html

    def update_position(self, latitude, longitude):
        """
        Update the vehicle position on the map.

        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
        """
        self._latitude = latitude
        self._longitude = longitude
        self._update_vehicle()

    def update_heading(self, heading):
        """
        Update the vehicle heading on the map.

        Args:
            heading: Heading in degrees (0-360)
        """
        self._heading = heading
        self._update_vehicle()

    def update_pitch(self, pitch):
        """
        Update the vehicle pitch on the map.

        Args:
            pitch: Pitch angle in degrees
        """
        self._pitch = pitch
        self._update_vehicle()

    def update_roll(self, roll):
        """
        Update the vehicle roll on the map.

        Args:
            roll: Roll angle in degrees
        """
        self._roll = roll
        self._update_vehicle()

    def update_pose(self, latitude, longitude, heading, pitch, roll):
        """
        Update all vehicle position and orientation parameters at once.

        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            heading: Heading in degrees (0-360)
            pitch: Pitch angle in degrees
            roll: Roll angle in degrees
        """
        self._latitude = latitude
        self._longitude = longitude
        self._heading = heading
        self._pitch = pitch
        self._roll = roll
        self._update_vehicle()

    def _update_vehicle(self):
        """Update the vehicle position and orientation on the map."""
        # Skip if we're showing the placeholder
        if (
            hasattr(self, "_web_view")
            and config.MAPBOX_TOKEN != "YOUR_MAPBOX_TOKEN_HERE"
        ):
            # Use JavaScript to update the vehicle
            js = f"if(window.updateVehicleFromPython) updateVehicleFromPython({self._longitude}, {self._latitude}, {self._heading}, {self._pitch}, {self._roll});"
            self._web_view.page().runJavaScript(js)

    def set_follow_vehicle(self, follow):
        """
        Set whether the map should follow the vehicle.

        Args:
            follow: True to follow the vehicle, False for fixed view
        """
        self._follow_vehicle = follow

        # Update the JavaScript variable
        if (
            hasattr(self, "_web_view")
            and config.MAPBOX_TOKEN != "YOUR_MAPBOX_TOKEN_HERE"
        ):
            js = f"window.followVehicle = {str(follow).lower()};"
            self._web_view.page().runJavaScript(js)

    def set_zoom(self, zoom):
        """
        Set the map zoom level.

        Args:
            zoom: Zoom level (higher values = closer)
        """
        self._zoom = zoom

        # Update the map zoom
        if (
            hasattr(self, "_web_view")
            and config.MAPBOX_TOKEN != "YOUR_MAPBOX_TOKEN_HERE"
        ):
            js = f"map.setZoom({zoom});"
            self._web_view.page().runJavaScript(js)
