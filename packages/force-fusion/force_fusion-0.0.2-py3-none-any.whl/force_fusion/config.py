"""
Configuration settings for Force-Fusion dashboard.
Contains constants for display ranges, units, update intervals, and styling.
"""

# Sensor update intervals (milliseconds)
GPS_UPDATE_INTERVAL = 1000
SPEED_UPDATE_INTERVAL = 100
ATTITUDE_UPDATE_INTERVAL = 100
TIRE_FORCE_UPDATE_INTERVAL = 200
MAP_UPDATE_INTERVAL = 1000

# Display ranges
SPEED_MIN = 0
SPEED_MAX = 240  # km/h
ACCEL_MIN = -10  # m/s²
ACCEL_MAX = 10  # m/s²
PITCH_MIN = -45  # degrees
PITCH_MAX = 45  # degrees
ROLL_MIN = -45  # degrees
ROLL_MAX = 45  # degrees
TIRE_FORCE_MIN = 0  # N
TIRE_FORCE_MAX = 5000  # N
TIRE_FORCE_NORMAL = 2500  # N

# Mapbox configuration
# Replace with your actual token when using the application
MAPBOX_TOKEN = "YOUR_MAPBOX_TOKEN_HERE"
MAPBOX_STYLE = "mapbox://styles/mapbox/streets-v11"
DEFAULT_CENTER = [0, 0]  # [longitude, latitude]
DEFAULT_ZOOM = 15

# Minimap configuration
TRAJECTORY_HISTORY_LENGTH = 1000  # Maximum number of points to keep
TRAJECTORY_LINE_WIDTH = 2

# UI colors
BACKGROUND_COLOR = "#212121"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#2196F3"
WARNING_COLOR = "#FFC107"
DANGER_COLOR = "#F44336"
SUCCESS_COLOR = "#4CAF50"

# Gauge colors
SPEED_COLOR = "#4CAF50"
ACCEL_COLOR_POSITIVE = "#4CAF50"
ACCEL_COLOR_NEGATIVE = "#F44336"
HEADING_COLOR = "#2196F3"
TIRE_FORCE_COLOR_NORMAL = "#4CAF50"
TIRE_FORCE_COLOR_HIGH = "#F44336"
TIRE_FORCE_COLOR_LOW = "#FFC107"
