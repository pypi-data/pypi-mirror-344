"""
Dashboard widget package.

This package contains all the custom widgets used by the Force-Fusion dashboard:
- MinimapWidget: 2D trajectory display
- SpeedometerWidget: Speed and acceleration display
- AttitudeWidget: Pitch and roll indicator
- HeadingWidget: Course-over-ground compass
- TireForceWidget: Tire normal force display
- MapboxView: 3D map with vehicle model
"""

from .attitude import AttitudeWidget
from .heading import HeadingWidget
from .mapbox_view import MapboxView
from .minimap import MinimapWidget
from .speedometer import SpeedometerWidget
from .tire_force import TireForceWidget

__all__ = [
    "MinimapWidget",
    "SpeedometerWidget",
    "AttitudeWidget",
    "HeadingWidget",
    "TireForceWidget",
    "MapboxView",
]
