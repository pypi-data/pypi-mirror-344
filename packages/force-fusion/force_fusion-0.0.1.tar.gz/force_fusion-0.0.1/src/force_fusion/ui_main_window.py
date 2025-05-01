"""
Main window UI definition for Force-Fusion dashboard.
"""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from . import config
from .widgets.attitude import AttitudeWidget
from .widgets.heading import HeadingWidget
from .widgets.mapbox_view import MapboxView
from .widgets.minimap import MinimapWidget
from .widgets.speedometer import SpeedometerWidget
from .widgets.tire_force import TireForceWidget


class Ui_MainWindow:
    """Main window UI definition for Force-Fusion dashboard."""

    def setupUi(self, MainWindow):
        """Set up the UI components for the main window."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setWindowTitle("Force-Fusion Dashboard")

        # Set up central widget
        self.centralWidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)

        # Main layout is vertical
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # Top section - Horizontal layout for circular widgets
        self.topFrame = QFrame()
        self.topFrame.setFrameShape(QFrame.StyledPanel)
        self.topLayout = QHBoxLayout(self.topFrame)

        # Bottom section - horizontal layout for tire forces and map
        self.bottomFrame = QFrame()
        self.bottomFrame.setFrameShape(QFrame.StyledPanel)
        self.bottomLayout = QHBoxLayout(self.bottomFrame)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame, 3)
        self.mainLayout.addWidget(self.bottomFrame, 2)

        # Create widgets
        self.setupTopWidgets()
        self.setupBottomWidgets()

        # Set styles
        self.applyStyles()

    def setupTopWidgets(self):
        """Create and place the four circular widgets in the top grid."""
        # Create circular widgets with fixed size policy
        self.minimapWidget = MinimapWidget()
        self.speedometerWidget = SpeedometerWidget()
        self.attitudeWidget = AttitudeWidget()
        self.headingWidget = HeadingWidget()

        # Set size policies for consistent sizing
        for widget in [
            self.minimapWidget,
            self.speedometerWidget,
            self.attitudeWidget,
            self.headingWidget,
        ]:
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setMinimumSize(QSize(200, 200))

        # Add widgets to horizontal layout (order: Minimap, Speedometer, Attitude, Heading)
        self.topLayout.addWidget(self.minimapWidget)
        self.topLayout.addWidget(self.speedometerWidget)
        self.topLayout.addWidget(self.attitudeWidget)
        self.topLayout.addWidget(self.headingWidget)

    def setupBottomWidgets(self):
        """Create and place the tire force widgets and mapbox view."""
        # Left side for tire forces in a 2x2 grid
        self.tireForceFrame = QFrame()
        self.tireForceLayout = QGridLayout(self.tireForceFrame)

        # Create tire force widgets
        self.tireForceFrontLeft = TireForceWidget("FL")
        self.tireForceFrontRight = TireForceWidget("FR")
        self.tireForceRearLeft = TireForceWidget("RL")
        self.tireForceRearRight = TireForceWidget("RR")

        # Set size policies
        for widget in [
            self.tireForceFrontLeft,
            self.tireForceFrontRight,
            self.tireForceRearLeft,
            self.tireForceRearRight,
        ]:
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setMinimumSize(QSize(150, 150))

        # Add tire force widgets to grid
        self.tireForceLayout.addWidget(self.tireForceFrontLeft, 0, 0)
        self.tireForceLayout.addWidget(self.tireForceFrontRight, 0, 1)
        self.tireForceLayout.addWidget(self.tireForceRearLeft, 1, 0)
        self.tireForceLayout.addWidget(self.tireForceRearRight, 1, 1)

        # Right side for Mapbox view and GPS/time info
        self.mapFrame = QFrame()
        self.mapLayout = QVBoxLayout(self.mapFrame)

        # Info section on top of map
        self.infoFrame = QFrame()
        self.infoLayout = QVBoxLayout(self.infoFrame)

        # GPS label
        self.gpsLabel = QLabel("GPS: Lat, Lon in degrees")
        self.gpsLabel.setAlignment(Qt.AlignLeft)

        # Time labels
        self.currentTimeLabel = QLabel("Current Time: 00h:00min:00sec")
        self.currentTimeLabel.setAlignment(Qt.AlignLeft)

        self.elapsedTimeLabel = QLabel("Time Elapsed: 00h:00min:00sec")
        self.elapsedTimeLabel.setAlignment(Qt.AlignLeft)

        # Add labels to info layout
        self.infoLayout.addWidget(self.gpsLabel)
        self.infoLayout.addWidget(self.currentTimeLabel)
        self.infoLayout.addWidget(self.elapsedTimeLabel)

        # Create Mapbox view
        self.mapboxView = MapboxView()
        self.mapboxView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add info and map to map layout
        self.mapLayout.addWidget(self.infoFrame)
        self.mapLayout.addWidget(self.mapboxView)

        # Add frames to bottom layout
        self.bottomLayout.addWidget(self.tireForceFrame, 1)
        self.bottomLayout.addWidget(self.mapFrame, 2)

    def applyStyles(self):
        """Apply QSS styles to widgets."""
        # Set background color for the main window
        self.centralWidget.setStyleSheet(
            f"background-color: {config.BACKGROUND_COLOR};"
        )

        # Style labels
        for label in [self.gpsLabel, self.currentTimeLabel, self.elapsedTimeLabel]:
            label.setStyleSheet(f"color: {config.TEXT_COLOR}; font-size: 14px;")

        # Style frames
        for frame in [
            self.topFrame,
            self.bottomFrame,
            self.tireForceFrame,
            self.mapFrame,
            self.infoFrame,
        ]:
            frame.setStyleSheet("border: none;")


class MainWindow(QMainWindow):
    """Main application window containing all dashboard widgets."""

    def __init__(self):
        """Initialize the main window and set up the UI."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Store widget references for easier access from controller
        self.minimap = self.ui.minimapWidget
        self.speedometer = self.ui.speedometerWidget
        self.attitude = self.ui.attitudeWidget
        self.heading = self.ui.headingWidget
        self.tire_forces = {
            "FL": self.ui.tireForceFrontLeft,
            "FR": self.ui.tireForceFrontRight,
            "RL": self.ui.tireForceRearLeft,
            "RR": self.ui.tireForceRearRight,
        }
        self.mapbox = self.ui.mapboxView
        self.gps_label = self.ui.gpsLabel
        self.current_time_label = self.ui.currentTimeLabel
        self.elapsed_time_label = self.ui.elapsedTimeLabel
