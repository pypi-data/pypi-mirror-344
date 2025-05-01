"""
Sensor data provider that emits signals for all dashboard data channels.
"""

import math
import random
from datetime import datetime

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class SensorProvider(QObject):
    """
    Provides sensor data to the dashboard by emitting Qt signals.

    In a real application, this would connect to actual vehicle sensors.
    For demonstration purposes, it generates simulated data.
    """

    # Define signals for each data channel
    position_changed = pyqtSignal(float, float)  # lat, lon
    speed_changed = pyqtSignal(float)  # km/h
    acceleration_changed = pyqtSignal(float)  # m/s²
    pitch_changed = pyqtSignal(float)  # degrees
    roll_changed = pyqtSignal(float)  # degrees
    heading_changed = pyqtSignal(float)  # degrees (0-360)
    tire_forces_changed = pyqtSignal(
        dict
    )  # {"FL": force, "FR": force, "RL": force, "RR": force} in N

    # Time signals
    current_time_changed = pyqtSignal(str)  # formatted time string
    elapsed_time_changed = pyqtSignal(str)  # formatted time string

    def __init__(self, data_source="simulated"):
        """
        Initialize the sensor provider.

        Args:
            data_source: Source of sensor data. Options:
                - "simulated": Generate fake data (default)
                - "file": Read from log file (not implemented)
                - "can": Read from CAN bus (not implemented)
        """
        super().__init__()

        self.data_source = data_source

        # Initialize simulated sensor values
        self._latitude = 37.7749  # San Francisco
        self._longitude = -122.4194
        self._speed = 0.0  # km/h
        self._acceleration = 0.0  # m/s²
        self._pitch = 0.0  # degrees
        self._roll = 0.0  # degrees
        self._heading = 0.0  # degrees
        self._tire_forces = {
            "FL": 2500.0,  # N
            "FR": 2500.0,
            "RL": 2500.0,
            "RR": 2500.0,
        }

        # Start time tracking
        self._start_time = datetime.now()

        # Set up timer for each data channel
        self._position_timer = QTimer(self)
        self._speed_timer = QTimer(self)
        self._attitude_timer = QTimer(self)
        self._tire_force_timer = QTimer(self)
        self._time_timer = QTimer(self)

        # Connect timers to update methods
        self._position_timer.timeout.connect(self._update_position)
        self._speed_timer.timeout.connect(self._update_speed)
        self._attitude_timer.timeout.connect(self._update_attitude)
        self._tire_force_timer.timeout.connect(self._update_tire_forces)
        self._time_timer.timeout.connect(self._update_time)

    def start(self):
        """Start all sensor update timers."""
        from . import config

        # Start timers with configured intervals
        self._position_timer.start(config.GPS_UPDATE_INTERVAL)
        self._speed_timer.start(config.SPEED_UPDATE_INTERVAL)
        self._attitude_timer.start(config.ATTITUDE_UPDATE_INTERVAL)
        self._tire_force_timer.start(config.TIRE_FORCE_UPDATE_INTERVAL)
        self._time_timer.start(100)  # Update time display every 100ms

        # Initial update to populate values
        self._update_position()
        self._update_speed()
        self._update_attitude()
        self._update_tire_forces()
        self._update_time()

    def stop(self):
        """Stop all sensor update timers."""
        self._position_timer.stop()
        self._speed_timer.stop()
        self._attitude_timer.stop()
        self._tire_force_timer.stop()
        self._time_timer.stop()

    def _update_position(self):
        """Update GPS position and emit signal."""
        if self.data_source == "simulated":
            # Simulate vehicle movement based on current heading and speed
            speed_mps = self._speed / 3.6  # Convert km/h to m/s

            # Calculate distance moved since last update (m)
            distance = speed_mps * (self._position_timer.interval() / 1000.0)

            # Convert heading to radians
            heading_rad = math.radians(self._heading)

            # Calculate changes in longitude and latitude
            # Simplified model, not accounting for Earth's curvature accurately
            lat_change = (
                distance * math.cos(heading_rad) / 111000
            )  # 1 degree lat ≈ 111 km
            # Longitude distance depends on latitude
            lon_change = (
                distance
                * math.sin(heading_rad)
                / (111000 * math.cos(math.radians(self._latitude)))
            )

            # Update position
            self._latitude += lat_change
            self._longitude += lon_change

        # Emit the position signal
        self.position_changed.emit(self._latitude, self._longitude)

        # Also update heading as we move
        self.heading_changed.emit(self._heading)

    def _update_speed(self):
        """Update speed and acceleration values and emit signals."""
        if self.data_source == "simulated":
            # Simulate realistic vehicle dynamics

            # Randomly adjust acceleration within realistic bounds
            self._acceleration += random.uniform(-0.5, 0.5)
            # Limit acceleration to realistic values
            self._acceleration = max(-5.0, min(5.0, self._acceleration))

            # Update speed based on acceleration
            speed_change = (
                self._acceleration * (self._speed_timer.interval() / 1000.0) * 3.6
            )  # m/s² to km/h
            self._speed += speed_change

            # Ensure speed is positive or zero (no reverse for simplicity)
            self._speed = max(0.0, self._speed)

            # Cap the speed at a maximum value
            self._speed = min(200.0, self._speed)

        # Emit the signals
        self.speed_changed.emit(self._speed)
        self.acceleration_changed.emit(self._acceleration)

    def _update_attitude(self):
        """Update pitch and roll values and emit signals."""
        if self.data_source == "simulated":
            # Simulate vehicle attitude changes
            # In reality, this would depend on acceleration, turning, and road grade

            # Update pitch (affected by acceleration and road grade)
            pitch_change = random.uniform(-0.5, 0.5)
            if self._acceleration > 1.0:
                pitch_change -= self._acceleration * 0.2  # Nose up during acceleration
            elif self._acceleration < -1.0:
                pitch_change += (
                    abs(self._acceleration) * 0.2
                )  # Nose down during braking

            self._pitch += pitch_change
            self._pitch = max(-20.0, min(20.0, self._pitch))  # Limit pitch range

            # Update roll (affected by turning)
            # Simulate turning by changing heading and corresponding roll
            heading_change = random.uniform(-1.0, 1.0)
            self._heading = (self._heading + heading_change) % 360.0

            # Roll is proportional to rate of heading change
            self._roll = heading_change * 5.0
            self._roll = max(-30.0, min(30.0, self._roll))  # Limit roll range

        # Emit the signals
        self.pitch_changed.emit(self._pitch)
        self.roll_changed.emit(self._roll)

    def _update_tire_forces(self):
        """Update tire normal forces and emit signal."""
        if self.data_source == "simulated":
            # Simulate tire load changes based on vehicle dynamics

            # Calculate weight transfer based on acceleration, pitch, and roll
            lateral_transfer = self._roll * 50.0  # Roll affects left-right distribution
            longitudinal_transfer = (
                self._acceleration * 100.0
            )  # Acceleration affects front-rear distribution

            # Base normal force per tire (vehicle weight / 4)
            base_force = 2500.0

            # Apply weight transfers
            self._tire_forces["FL"] = (
                base_force - longitudinal_transfer + lateral_transfer
            )
            self._tire_forces["FR"] = (
                base_force - longitudinal_transfer - lateral_transfer
            )
            self._tire_forces["RL"] = (
                base_force + longitudinal_transfer + lateral_transfer
            )
            self._tire_forces["RR"] = (
                base_force + longitudinal_transfer - lateral_transfer
            )

            # Add some random variation
            for tire in self._tire_forces:
                self._tire_forces[tire] += random.uniform(-50.0, 50.0)
                # Ensure forces stay within realistic bounds
                self._tire_forces[tire] = max(
                    500.0, min(4500.0, self._tire_forces[tire])
                )

        # Emit the signal
        self.tire_forces_changed.emit(self._tire_forces.copy())

    def _update_time(self):
        """Update time displays and emit signals."""
        # Get current time
        current_time = datetime.now()

        # Format current time
        current_time_str = current_time.strftime("%Hh:%Mmin:%Ssec")

        # Calculate elapsed time
        elapsed = current_time - self._start_time
        total_seconds = int(elapsed.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time_str = f"{hours:02d}h:{minutes:02d}min:{seconds:02d}sec"

        # Emit signals
        self.current_time_changed.emit(current_time_str)
        self.elapsed_time_changed.emit(elapsed_time_str)

    def set_data_source(self, source):
        """
        Change the data source.

        Args:
            source: New data source ("simulated", "file", or "can")
        """
        self.stop()
        self.data_source = source
        self.start()
