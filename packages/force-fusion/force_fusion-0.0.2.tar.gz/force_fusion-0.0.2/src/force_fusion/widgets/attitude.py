"""
Attitude widget for displaying vehicle pitch and roll.
"""

import math
import os

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from PyQt5.QtWidgets import QSizePolicy, QWidget

from .. import config

# Define resource paths relative to this file
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))  # widgets/
RESOURCE_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "resources")
)  # force_fusion/resources
CAR_SIDE_PATH = os.path.join(RESOURCE_DIR, "car_side.svg")
CAR_BACK_PATH = os.path.join(RESOURCE_DIR, "car_back.svg")


class AttitudeWidget(QWidget):
    """
    Widget that displays an attitude indicator showing vehicle pitch and roll.

    Similar to an aircraft artificial horizon, this displays:
    - Pitch (nose up/down angle)
    - Roll (left/right tilt angle)
    - Reference vehicle indicator
    """

    def __init__(self, parent=None):
        """
        Initialize the attitude indicator widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Current attitude values
        self._pitch = 15.0  # degrees (example value)
        self._roll = -10.0  # degrees (example value)

        # Attitude indicator settings
        self._pitch_scale_max = 40.0  # degrees
        self._roll_scale_max = 40.0  # degrees
        self._pitch_major_step = 10.0

        # Load car icons
        self._car_side_pixmap = QPixmap(CAR_SIDE_PATH)
        self._car_back_pixmap = QPixmap(CAR_BACK_PATH)

        # If images couldn't be loaded, create basic white car shapes
        if self._car_side_pixmap.isNull():
            print(f"Warning: Could not load {CAR_SIDE_PATH}. Using placeholder.")
            self._car_side_pixmap = self._create_side_car_placeholder()

        if self._car_back_pixmap.isNull():
            print(f"Warning: Could not load {CAR_BACK_PATH}. Using placeholder.")
            self._car_back_pixmap = self._create_back_car_placeholder()

        # Set widget properties
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(config.BACKGROUND_COLOR))
        self.setPalette(palette)

    def _create_side_car_placeholder(self):
        """Create a simple white car side view placeholder"""
        pixmap = QPixmap(60, 30)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a simple car side view silhouette in white
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(QColor(200, 200, 200))

        # Car body shape
        path = QPainterPath()
        path.moveTo(5, 20)
        path.lineTo(10, 20)
        path.lineTo(15, 12)
        path.lineTo(30, 12)
        path.lineTo(40, 6)
        path.lineTo(50, 6)
        path.lineTo(55, 12)
        path.lineTo(55, 20)
        path.lineTo(45, 20)
        path.lineTo(42, 25)
        path.lineTo(20, 25)
        path.lineTo(17, 25)
        path.lineTo(15, 20)
        path.lineTo(5, 20)
        painter.drawPath(path)

        # Wheels
        painter.setBrush(QColor(50, 50, 50))
        painter.drawEllipse(15, 22, 8, 8)
        painter.drawEllipse(42, 22, 8, 8)

        # Windows
        painter.setBrush(QColor(150, 150, 150))
        painter.drawRect(18, 9, 20, 8)

        painter.end()
        return pixmap

    def _create_back_car_placeholder(self):
        """Create a simple white car back view placeholder"""
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a simple car back view silhouette in white
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(QColor(200, 200, 200))

        # Car body shape
        path = QPainterPath()
        path.moveTo(8, 25)
        path.lineTo(32, 25)
        path.lineTo(32, 15)
        path.lineTo(28, 8)
        path.lineTo(12, 8)
        path.lineTo(8, 15)
        path.lineTo(8, 25)
        painter.drawPath(path)

        # Wheels
        painter.setBrush(QColor(50, 50, 50))
        painter.drawEllipse(5, 22, 8, 8)
        painter.drawEllipse(27, 22, 8, 8)

        # Window
        painter.setBrush(QColor(150, 150, 150))
        painter.drawRect(12, 10, 16, 8)

        painter.end()
        return pixmap

    def set_pitch(self, pitch):
        """
        Set the pitch angle.

        Args:
            pitch: Pitch angle in degrees
        """
        self._pitch = max(config.PITCH_MIN, min(config.PITCH_MAX, pitch))
        self.update()

    def set_roll(self, roll):
        """
        Set the roll angle.

        Args:
            roll: Roll angle in degrees
        """
        self._roll = max(config.ROLL_MIN, min(config.ROLL_MAX, roll))
        self.update()

    def paintEvent(self, event):
        """
        Paint the attitude indicator based on the reference design.

        Args:
            event: Paint event
        """
        # Create painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get widget dimensions and calculate radius/center
        width = self.width()
        height = self.height()
        diameter = min(width, height)
        radius = diameter // 2 - 10  # Padding
        center_x = width // 2
        center_y = height // 2

        # Draw static background elements
        self._draw_gauge_background(painter, center_x, center_y, radius)
        self._draw_degree_scales(painter, center_x, center_y, radius)

        # Draw dynamic elements
        self._draw_car_indicators(painter, center_x, center_y, radius)
        self._draw_value_indicators(painter, center_x, center_y, radius)

        # Draw title
        painter.setPen(QColor(config.TEXT_COLOR))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(QRectF(0, 5, width, 20), Qt.AlignCenter, "Attitude")

    def _draw_gauge_background(self, painter, center_x, center_y, radius):
        """Draw the circular background of the gauge."""
        # Draw outer circle background
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QColor(20, 20, 20))  # Dark background
        painter.drawEllipse(
            center_x - radius, center_y - radius, radius * 2, radius * 2
        )

        # Draw +/- markers at the ends of the line
        marker_size = radius * 0.1
        painter.setPen(QPen(Qt.white, 2))

        # Minus sign (left)
        minus_x = center_x - radius + marker_size * 2
        painter.drawLine(
            int(minus_x - marker_size), center_y, int(minus_x + marker_size), center_y
        )

        # Plus sign (right)
        plus_x = center_x + radius - marker_size * 2
        painter.drawLine(
            int(plus_x - marker_size), center_y, int(plus_x + marker_size), center_y
        )
        painter.drawLine(
            int(plus_x),
            int(center_y - marker_size),
            int(plus_x),
            int(center_y + marker_size),
        )

    def _draw_degree_scales(self, painter, center_x, center_y, radius):
        """Draw the pitch/roll degree scales around the periphery."""
        scale_radius = radius * 0.85  # Slightly inset from edge

        for i in range(5):  # 0, 10, 20, 30, 40 degrees
            angle_value = i * 10

            # Set color based on angle value (match reference image)
            if angle_value <= 20:
                color = Qt.white
            elif angle_value <= 30:
                color = QColor(255, 165, 0)  # Orange
            else:
                color = Qt.red

            painter.setPen(QPen(color, 1))
            painter.setFont(
                QFont("Arial", 8, QFont.Bold if angle_value >= 30 else QFont.Normal)
            )

            # Draw angle markings in all four quadrants
            for quadrant in range(4):
                # Calculate position based on quadrant
                if quadrant == 0:  # Top-right
                    angle_rad = math.radians(90 - angle_value)
                elif quadrant == 1:  # Top-left
                    angle_rad = math.radians(90 + angle_value)
                elif quadrant == 2:  # Bottom-left
                    angle_rad = math.radians(270 - angle_value)
                else:  # Bottom-right
                    angle_rad = math.radians(270 + angle_value)

                x = center_x + scale_radius * math.cos(angle_rad)
                y = center_y - scale_radius * math.sin(angle_rad)

                # Skip 0 degree marks (on horizontal line)
                if angle_value == 0:
                    continue

                # Draw the tick mark
                tick_length = 8 if angle_value % 20 == 0 else 5
                inner_x = center_x + (scale_radius - tick_length) * math.cos(angle_rad)
                inner_y = center_y - (scale_radius - tick_length) * math.sin(angle_rad)
                painter.drawLine(int(inner_x), int(inner_y), int(x), int(y))

                # Draw the text
                text_radius = scale_radius - 20
                text_x = center_x + text_radius * math.cos(angle_rad)
                text_y = center_y - text_radius * math.sin(angle_rad)

                text_rect = QRectF(text_x - 15, text_y - 15, 30, 30)
                painter.drawText(text_rect, Qt.AlignCenter, str(angle_value))

            # Remove side degree markings

    def _draw_car_indicators(self, painter, center_x, center_y, radius):
        """Draw the car indicators for pitch and roll."""
        car_size = radius * 0.25  # Size of car icons

        # Draw pitch indicator (side view car)
        painter.save()
        side_car_y = center_y + radius * 0.3  # Position below center

        # Apply pitch rotation to side car
        painter.translate(center_x, side_car_y)
        pitch_angle = self._pitch * 0.8
        painter.rotate(
            -pitch_angle
        )  # Negative to match convention (nose up = positive pitch -> counter-clockwise rotation)

        # Scale and draw the side view car
        scaled_side_car = self._car_side_pixmap.scaled(
            int(car_size * 2.3),
            int(car_size),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        painter.drawPixmap(
            int(-scaled_side_car.width() / 2),
            int(-scaled_side_car.height() / 2),
            scaled_side_car,
        )

        # Draw dynamic pitch horizon line relative to the side car
        painter.setPen(QPen(Qt.white, 1))
        horizon_width = radius * 0.5
        # Line stays horizontal in the car's rotated frame
        horizon_y_offset = 0  # Centered on the car's pivot point for simplicity
        painter.drawLine(
            int(-horizon_width / 2),
            int(horizon_y_offset),
            int(horizon_width / 2),
            int(horizon_y_offset),
        )

        painter.restore()

        # Draw pitch value (outside the rotated context)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        pitch_text = f"{int(self._pitch)}"
        text_rect = QRectF(center_x - 40, side_car_y + car_size * 0.7, 80, 30)
        painter.drawText(text_rect, Qt.AlignCenter, pitch_text)

        # Draw roll indicator (back view car)
        painter.save()
        roll_car_y = center_y - radius * 0.3  # Position above center

        # Apply rotation for roll
        painter.translate(center_x, roll_car_y)
        painter.rotate(-self._roll)  # Negative because positive roll is clockwise

        # Scale and draw the back view car
        scaled_back_car = self._car_back_pixmap.scaled(
            int(car_size * 1),
            int(car_size * 1),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        painter.drawPixmap(
            int(-scaled_back_car.width() / 2),
            int(-scaled_back_car.height() / 2),
            scaled_back_car,
        )

        # Draw dynamic roll horizon line relative to the back car
        painter.setPen(QPen(Qt.white, 1))
        roll_horizon_width = radius * 0.4  # Slightly smaller than pitch horizon
        # Line stays horizontal in the car's rotated frame
        roll_horizon_y_offset = 0  # Centered for simplicity
        painter.drawLine(
            int(-roll_horizon_width / 2),
            int(roll_horizon_y_offset),
            int(roll_horizon_width / 2),
            int(roll_horizon_y_offset),
        )

        painter.restore()

        # Draw roll value
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        roll_text = (
            f"{int(-self._roll)}"  # Negative to match reference image convention
        )
        text_rect = QRectF(center_x - 40, roll_car_y - car_size * 0.7 - 30, 80, 30)
        painter.drawText(text_rect, Qt.AlignCenter, roll_text)

    def _draw_value_indicators(self, painter, center_x, center_y, radius):
        """Draw the triangular indicators showing current pitch and roll values."""
        scale_radius = radius * 0.85
        triangle_size = radius * 0.04

        # Calculate positions for triangles based on current values
        # For pitch (orange triangle on bottom arc)
        pitch_ratio = self._pitch / self._pitch_scale_max
        pitch_ratio = max(-1.0, min(1.0, pitch_ratio))

        # For roll (blue triangle on top arc)
        roll_ratio = self._roll / self._roll_scale_max
        roll_ratio = max(-1.0, min(1.0, roll_ratio))

        # Draw roll indicator triangle on the top arc (cyan/blue)
        top_roll_angle_deg = (
            90 - roll_ratio * 70
        )  # Map ratio to degrees on top arc (range 20 to 160)
        top_roll_angle_rad = math.radians(top_roll_angle_deg)
        top_roll_x = center_x + scale_radius * math.cos(top_roll_angle_rad)
        top_roll_y = center_y - scale_radius * math.sin(top_roll_angle_rad)

        # Calculate radial angle from center to the roll indicator
        roll_radial_angle = math.degrees(
            math.atan2(top_roll_y - center_y, top_roll_x - center_x)
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 255, 255))  # Cyan (blue)
        # Rotate triangle to point downward toward center/degree marks
        self._draw_triangle_indicator(
            painter,
            int(top_roll_x),
            int(top_roll_y),
            roll_radial_angle - 180,
            triangle_size,
            True,
        )

        # Draw pitch indicator triangle on the bottom arc (orange/yellow)
        bottom_pitch_angle_deg = (
            270 + pitch_ratio * 70
        )  # Map ratio to degrees on bottom arc (range 200 to 340)
        bottom_pitch_angle_rad = math.radians(bottom_pitch_angle_deg)
        bottom_pitch_x = center_x + scale_radius * math.cos(bottom_pitch_angle_rad)
        bottom_pitch_y = center_y - scale_radius * math.sin(bottom_pitch_angle_rad)

        # Calculate radial angle from center to the pitch indicator
        pitch_radial_angle = math.degrees(
            math.atan2(bottom_pitch_y - center_y, bottom_pitch_x - center_x)
        )

        painter.setBrush(QColor(255, 165, 0))  # Orange (yellow)
        # Rotate triangle to point upward away from center/degree marks
        self._draw_triangle_indicator(
            painter,
            int(bottom_pitch_x),
            int(bottom_pitch_y),
            pitch_radial_angle + 180,
            triangle_size,
            True,
        )

    def _draw_triangle_indicator(self, painter, x, y, angle_deg, size, pointy=False):
        """Draw a triangular indicator at the given position.

        Args:
            painter: QPainter object
            x, y: Coordinates of the triangle center
            angle_deg: Angle to rotate the triangle (in degrees)
            size: Size of the triangle
            pointy: Whether to make the triangle more pointy
        """
        painter.save()
        painter.translate(x, y)
        # Rotate to the specified angle
        painter.rotate(angle_deg + 90)

        if pointy:
            # Define a more pointy triangle
            triangle = QPolygonF(
                [
                    QPointF(0, -size * 1.5),  # Tip point (extended 50% for pointiness)
                    QPointF(-size, size),  # Base corner 1
                    QPointF(size, size),  # Base corner 2
                ]
            )
        else:
            triangle = QPolygonF(
                [
                    QPointF(0, -size),  # Tip
                    QPointF(-size, size),  # Base corner 1
                    QPointF(size, size),  # Base corner 2
                ]
            )

        painter.drawPolygon(triangle)
        painter.restore()
