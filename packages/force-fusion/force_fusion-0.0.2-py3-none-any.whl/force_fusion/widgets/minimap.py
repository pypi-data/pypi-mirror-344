"""
Minimap widget that displays a 2D trajectory of the vehicle's path.
"""

import math

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from .. import config


class MinimapWidget(QWidget):
    """
    Widget that displays a 2D trajectory of the vehicle's path.

    Features:
    - Scrolling/zooming 2D map showing the vehicle's trajectory
    - Current position marker
    - Direction indicator
    """

    def __init__(self, parent=None):
        """
        Initialize the minimap widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Current position
        self._latitude = 0.0
        self._longitude = 0.0

        # Trajectory history (list of lat/lon points)
        self._trajectory = []
        self._max_points = config.TRAJECTORY_HISTORY_LENGTH

        # Map view settings
        self._zoom = 1.0  # Zoom level
        self._center_on_vehicle = True  # Whether to keep vehicle centered

        # Cached data for efficient rendering
        self._map_scale = 0.0001  # Degrees per pixel
        self._centerx = 0
        self._centery = 0

        # Set widget properties
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(config.BACKGROUND_COLOR))
        self.setPalette(palette)

    def update_position(self, latitude, longitude):
        """
        Update the current position and add it to the trajectory.

        Args:
            latitude: Current latitude in degrees
            longitude: Current longitude in degrees
        """
        self._latitude = latitude
        self._longitude = longitude

        # Add to trajectory
        self._trajectory.append((latitude, longitude))

        # Limit number of trajectory points
        if len(self._trajectory) > self._max_points:
            self._trajectory.pop(0)

        # Request a repaint
        self.update()

    def clear_trajectory(self):
        """Clear the trajectory history."""
        self._trajectory = []
        self.update()

    def set_zoom(self, zoom):
        """
        Set the zoom level.

        Args:
            zoom: Zoom level (1.0 = standard zoom)
        """
        self._zoom = max(0.1, min(10.0, zoom))
        self.update()

    def set_center_on_vehicle(self, center):
        """
        Set whether to keep the vehicle centered in the view.

        Args:
            center: True to center on vehicle, False to allow free panning
        """
        self._center_on_vehicle = center
        self.update()

    def paintEvent(self, event):
        """
        Paint the minimap.

        Args:
            event: Paint event
        """
        # Create painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get widget dimensions and calculate drawing area
        width = self.width()
        height = self.height()
        # Use the smaller dimension to define the diameter for a perfect circle
        diameter = min(width, height)
        radius = diameter // 2 - 10  # Subtract padding

        # Calculate the center based on the actual widget size
        widget_center_x = width // 2
        widget_center_y = height // 2

        # Define the drawing area (square centered in the widget)
        draw_rect = QRectF(
            widget_center_x - radius - 5,
            widget_center_y - radius - 5,
            diameter - 10,
            diameter - 10,
        )
        self._centerx = draw_rect.center().x()
        self._centery = draw_rect.center().y()

        # Draw background circle using the calculated square area
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QColor(40, 40, 40))
        painter.drawEllipse(draw_rect)

        # Draw coordinate grid within the circle
        self._draw_grid(painter, self._centerx, self._centery, radius)

        # Calculate map scale based on zoom
        self._map_scale = 0.0001 / self._zoom

        # Draw trajectory
        self._draw_trajectory(painter, width, height)

        # Draw current position marker
        self._draw_position_marker(painter, width, height)

        # Draw title
        painter.setPen(QColor(config.TEXT_COLOR))
        painter.drawText(QRectF(0, 5, width, 20), Qt.AlignCenter, "2D Minimap")

    def _draw_grid(self, painter, center_x, center_y, radius):
        """Draw the coordinate grid."""
        painter.setPen(QPen(QColor(80, 80, 80), 0.5))

        # Draw concentric circles
        # Use the passed radius which is based on min dimension
        radius_step = radius / 5  # Divide the actual radius into steps
        for i in range(1, 5):
            current_radius = i * radius_step
            painter.drawEllipse(
                int(center_x - current_radius),
                int(center_y - current_radius),
                int(current_radius * 2),
                int(current_radius * 2),
            )

        # Draw crosshairs based on the calculated center and radius
        painter.drawLine(
            int(center_x), int(center_y - radius), int(center_x), int(center_y + radius)
        )
        painter.drawLine(
            int(center_x - radius), int(center_y), int(center_x + radius), int(center_y)
        )

    def _draw_trajectory(self, painter, width, height):
        """Draw the vehicle's trajectory path."""
        if len(self._trajectory) < 2:
            return

        # Create path for the trajectory
        path = QPainterPath()

        # Get reference point (either current position or first trajectory point)
        ref_lat = self._latitude if self._center_on_vehicle else self._trajectory[0][0]
        ref_lon = self._longitude if self._center_on_vehicle else self._trajectory[0][1]

        # Start the path
        first_point = self._trajectory[0]
        x, y = self._geo_to_screen(first_point[0], first_point[1], ref_lat, ref_lon)
        path.moveTo(x, y)

        # Add all points to the path
        for point in self._trajectory[1:]:
            x, y = self._geo_to_screen(point[0], point[1], ref_lat, ref_lon)
            path.lineTo(x, y)

        # Draw the path
        pen = QPen(QColor(config.ACCENT_COLOR), config.TRAJECTORY_LINE_WIDTH)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_position_marker(self, painter, width, height):
        """Draw the current position marker."""
        if self._center_on_vehicle:
            x, y = self._centerx, self._centery
        else:
            x, y = self._geo_to_screen(
                self._latitude,
                self._longitude,
                self._trajectory[0][0] if self._trajectory else self._latitude,
                self._trajectory[0][1] if self._trajectory else self._longitude,
            )

        # Draw vehicle marker
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QColor(config.ACCENT_COLOR))
        painter.drawEllipse(int(x - 5), int(y - 5), 10, 10)

        # Draw direction indicator (simple triangle)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)

        # Draw direction indicator
        if len(self._trajectory) >= 2:
            # Calculate heading from last two points
            last = self._trajectory[-1]
            prev = self._trajectory[-2]

            # Calculate heading
            dx = last[1] - prev[1]
            dy = last[0] - prev[0]
            heading = math.degrees(math.atan2(dx, dy))

            # Convert heading to radians
            heading_rad = math.radians(heading)

            # Define triangle points
            triangle = [
                QPointF(x + 10 * math.sin(heading_rad), y + 10 * math.cos(heading_rad)),
                QPointF(
                    x + 5 * math.sin(heading_rad + 2.5),
                    y + 5 * math.cos(heading_rad + 2.5),
                ),
                QPointF(
                    x + 5 * math.sin(heading_rad - 2.5),
                    y + 5 * math.cos(heading_rad - 2.5),
                ),
            ]

            # Draw triangle
            painter.drawPolygon(triangle)

    def _geo_to_screen(self, lat, lon, ref_lat, ref_lon):
        """
        Convert geographic coordinates to screen coordinates.

        Args:
            lat: Latitude to convert
            lon: Longitude to convert
            ref_lat: Reference latitude (center of view)
            ref_lon: Reference longitude (center of view)

        Returns:
            (x, y) tuple of screen coordinates
        """
        # Convert lat/lon to x/y
        # Note: This is a simplified projection, not accurate for large areas
        x = self._centerx + (lon - ref_lon) / self._map_scale
        y = self._centery - (lat - ref_lat) / self._map_scale

        return x, y
