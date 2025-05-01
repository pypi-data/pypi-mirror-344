"""
Speedometer widget for displaying speed and acceleration.
"""

import math

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QRadialGradient
from PyQt5.QtWidgets import QSizePolicy, QWidget

from .. import config


class SpeedometerWidget(QWidget):
    """
    Widget that displays a circular speedometer with speed and acceleration.

    Features:
    - Circular gauge showing speed
    - Digital speed readout
    - Acceleration indicator bar
    """

    def __init__(self, parent=None):
        """
        Initialize the speedometer widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Current values
        self._speed = 0.0  # km/h
        self._acceleration = 0.0  # m/s²

        # Cached calculated values
        self._speed_angle = 0.0

        # Gauge appearance settings
        self._min_angle = 135  # Start angle in degrees
        self._max_angle = 405  # End angle in degrees (45° past 0)
        self._min_speed = config.SPEED_MIN
        self._max_speed = config.SPEED_MAX

        # Set widget properties
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(config.BACKGROUND_COLOR))
        self.setPalette(palette)

    def update_speed(self, speed):
        """
        Update the speed value.

        Args:
            speed: Speed in km/h
        """
        self._speed = max(self._min_speed, min(self._max_speed, speed))
        self._recalculate()
        self.update()

    def update_acceleration(self, acceleration):
        """
        Update the acceleration value.

        Args:
            acceleration: Acceleration in m/s²
        """
        self._acceleration = acceleration
        self.update()

    def _recalculate(self):
        """Recalculate derived values like angles."""
        # Calculate angle based on speed
        speed_range = self._max_speed - self._min_speed
        angle_range = self._max_angle - self._min_angle

        if speed_range <= 0:
            self._speed_angle = self._min_angle
        else:
            self._speed_angle = (
                self._min_angle
                + (self._speed - self._min_speed) * angle_range / speed_range
            )

    def paintEvent(self, event):
        """
        Paint the speedometer.

        Args:
            event: Paint event
        """
        # Create painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get widget dimensions
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - 10

        # Draw background circle
        self._draw_background(painter, center_x, center_y, radius)

        # Draw gauge ticks and labels
        self._draw_ticks_and_labels(painter, center_x, center_y, radius)

        # Draw speed needle
        self._draw_needle(painter, center_x, center_y, radius)

        # Draw digital speed and acceleration readout (moved above needle)
        self._draw_digital_readout(painter, center_x, center_y, radius)

        # Draw acceleration bar (position adjusted if necessary)
        self._draw_acceleration_bar(painter, center_x, center_y, radius)

        # Draw title
        painter.setPen(QColor(config.TEXT_COLOR))
        painter.drawText(QRectF(0, 5, width, 20), Qt.AlignCenter, "Speedometer")

    def _draw_background(self, painter, center_x, center_y, radius):
        """Draw the speedometer background."""
        # Outer circle
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QColor(40, 40, 40))
        painter.drawEllipse(
            center_x - radius, center_y - radius, radius * 2, radius * 2
        )

        # Inner circle with radial gradient
        gradient = QRadialGradient(center_x, center_y, radius * 0.8)
        gradient.setColorAt(0, QColor(50, 50, 50))
        gradient.setColorAt(1, QColor(25, 25, 25))
        painter.setBrush(gradient)
        painter.drawEllipse(
            int(center_x - radius * 0.8),
            int(center_y - radius * 0.8),
            int(radius * 1.6),
            int(radius * 1.6),
        )

    def _draw_ticks_and_labels(self, painter, center_x, center_y, radius):
        """Draw the speedometer ticks and speed labels."""
        # Set up fonts
        label_font = QFont("Arial", 8)
        painter.setFont(label_font)

        # Set up pens
        major_tick_pen = QPen(QColor(200, 200, 200), 2)
        minor_tick_pen = QPen(QColor(150, 150, 150), 1)
        label_pen = QPen(QColor(config.TEXT_COLOR), 1)

        # Calculate angles and values
        angle_range = self._max_angle - self._min_angle
        speed_range = self._max_speed - self._min_speed
        major_step = 20  # Show major ticks every 20 km/h
        minor_step = 10  # Show minor ticks every 10 km/h

        # Draw arc
        arc_rect = QRectF(
            center_x - radius * 0.85,
            center_y - radius * 0.85,
            radius * 1.7,
            radius * 1.7,
        )

        # Draw gradient arc from green to red
        start_angle = self._min_angle * 16  # QPainter uses 1/16th degrees
        span_angle = (self._max_angle - self._min_angle) * 16

        # Arc colors
        green = QColor(config.SUCCESS_COLOR)
        yellow = QColor(config.WARNING_COLOR)
        red = QColor(config.DANGER_COLOR)

        # Draw arcs in segments
        segment_count = 3
        for i in range(segment_count):
            segment_start = start_angle + (span_angle * i) // segment_count
            segment_span = span_angle // segment_count

            if i == 0:
                color = green
            elif i == 1:
                color = yellow
            else:
                color = red

            painter.setPen(QPen(color, 3))
            painter.drawArc(arc_rect, segment_start, segment_span)

        # Draw ticks and labels
        for speed in range(int(self._min_speed), int(self._max_speed) + 1, minor_step):
            # Calculate angle for this speed
            angle = (
                self._min_angle + (speed - self._min_speed) * angle_range / speed_range
            )
            angle_rad = math.radians(angle)

            # Calculate tick positions
            inner_x = center_x + (radius * 0.7) * math.cos(angle_rad)
            inner_y = center_y - (radius * 0.7) * math.sin(angle_rad)

            # Determine if this is a major tick
            is_major = speed % major_step == 0

            if is_major:
                # Draw major tick
                painter.setPen(major_tick_pen)
                outer_x = center_x + (radius * 0.85) * math.cos(angle_rad)
                outer_y = center_y - (radius * 0.85) * math.sin(angle_rad)
                painter.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y))

                # Draw speed label
                painter.setPen(label_pen)
                label_x = center_x + (radius * 0.6) * math.cos(angle_rad)
                label_y = center_y - (radius * 0.6) * math.sin(angle_rad)

                # Adjust for text metrics
                text = str(speed)
                metrics = QFontMetrics(label_font)
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()

                # Center the text on the calculated position
                label_rect = QRectF(
                    label_x - text_width / 2,
                    label_y - text_height / 2,
                    text_width,
                    text_height,
                )

                painter.drawText(label_rect, Qt.AlignCenter, text)
            else:
                # Draw minor tick
                painter.setPen(minor_tick_pen)
                outer_x = center_x + (radius * 0.8) * math.cos(angle_rad)
                outer_y = center_y - (radius * 0.8) * math.sin(angle_rad)
                painter.drawLine(int(inner_x), int(inner_y), int(outer_x), int(outer_y))

    def _draw_needle(self, painter, center_x, center_y, radius):
        """Draw the speed needle."""
        # Convert speed angle to radians
        angle_rad = math.radians(self._speed_angle)

        # Calculate needle end point
        needle_length = radius * 0.75
        end_x = center_x + needle_length * math.cos(angle_rad)
        end_y = center_y - needle_length * math.sin(angle_rad)

        # Draw needle
        painter.setPen(QPen(Qt.red, 2))
        painter.drawLine(center_x, center_y, int(end_x), int(end_y))

        # Draw center hub
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.setBrush(QColor(100, 100, 100))
        painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)

    def _draw_digital_readout(self, painter, center_x, center_y, radius):
        """Draw the digital speed readout and acceleration in G's."""
        # --- Speed ---
        # Convert speed to mi/h
        speed_mph = self._speed * 0.621371
        speed_text = f"{speed_mph:.1f} mi/h"

        # Set up font for speed
        speed_font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(speed_font)
        speed_metrics = QFontMetrics(speed_font)
        speed_text_width = speed_metrics.horizontalAdvance(speed_text)
        speed_text_height = speed_metrics.height()

        # --- Acceleration ---
        # Convert acceleration to g's (clamped 0-1)
        accel_g = max(0.0, min(1.0, abs(self._acceleration / 9.81)))
        accel_text = f"{accel_g:.2f} g"

        # Set up font for acceleration
        accel_font = QFont("Arial", 10)
        painter.setFont(accel_font)
        accel_metrics = QFontMetrics(accel_font)
        accel_text_width = accel_metrics.horizontalAdvance(accel_text)
        accel_text_height = accel_metrics.height()

        # --- Layout ---
        # Define overall box dimensions needed for both lines
        total_text_height = speed_text_height + accel_text_height + 5  # Add padding
        max_text_width = max(speed_text_width, accel_text_width)
        readout_width = max(radius * 0.7, max_text_width + 20)  # Ensure box fits text
        readout_height = total_text_height + 10  # Add padding

        # Position the box above the center hub, slightly higher
        readout_rect = QRectF(
            center_x - readout_width / 2,
            center_y - radius * 0.3 - readout_height,
            readout_width,
            readout_height,
        )

        # Draw background for the text block
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QColor(30, 30, 30))
        painter.drawRoundedRect(readout_rect, 5, 5)

        # Draw speed text centered horizontally, at the top of the box
        speed_rect = QRectF(
            readout_rect.x(),
            readout_rect.y() + 5,  # Padding from top
            readout_rect.width(),
            speed_text_height,
        )
        painter.setFont(speed_font)
        painter.setPen(QColor(config.TEXT_COLOR))
        painter.drawText(speed_rect, Qt.AlignCenter, speed_text)

        # Draw acceleration text centered horizontally, below the speed text
        accel_rect = QRectF(
            readout_rect.x(),
            speed_rect.bottom() + 5,  # Padding between lines
            readout_rect.width(),
            accel_text_height,
        )
        painter.setFont(accel_font)
        painter.setPen(QColor(config.TEXT_COLOR))
        painter.drawText(accel_rect, Qt.AlignCenter, accel_text)

    def _draw_acceleration_bar(self, painter, center_x, center_y, radius):
        """Draw the acceleration indicator bar."""
        # Define bar dimensions (shorter width)
        bar_width = radius * 0.8  # Reduced width
        bar_height = radius * 0.15
        # Position bar further down but slightly higher than before
        bar_rect = QRectF(
            center_x - bar_width / 2,
            center_y + radius * 0.2,  # Adjusted position
            bar_width,
            bar_height,
        )

        # Draw bar background
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QColor(30, 30, 30))
        painter.drawRoundedRect(bar_rect, 3, 3)

        # Draw center line
        center_line_x = center_x
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        painter.drawLine(
            center_line_x, int(bar_rect.top()), center_line_x, int(bar_rect.bottom())
        )

        # Calculate acceleration value position
        accel_limit = 5.0  # m/s²
        normalized_accel = (
            max(-accel_limit, min(accel_limit, self._acceleration)) / accel_limit
        )
        accel_pos_x = center_x + normalized_accel * (bar_width / 2 - 2)

        # Draw acceleration indicator
        indicator_width = 6
        indicator_rect = QRectF(
            accel_pos_x - indicator_width / 2,
            bar_rect.top() + 2,
            indicator_width,
            bar_rect.height() - 4,
        )

        # Set color based on acceleration direction
        if self._acceleration > 0:
            accel_color = QColor(config.ACCEL_COLOR_POSITIVE)
        else:
            accel_color = QColor(config.ACCEL_COLOR_NEGATIVE)

        painter.setPen(Qt.NoPen)
        painter.setBrush(accel_color)
        painter.drawRoundedRect(indicator_rect, 2, 2)

        # Draw acceleration label
        painter.setPen(QColor(config.TEXT_COLOR))
        accel_text = f"{self._acceleration:.1f} m/s²"

        # Draw text below bar
        label_rect = QRectF(
            bar_rect.left(), bar_rect.bottom() + 2, bar_rect.width(), 20
        )
        painter.setFont(QFont("Arial", 8))
        painter.drawText(label_rect, Qt.AlignCenter, accel_text)
