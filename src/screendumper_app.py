from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QGuiApplication
from datetime import datetime
import os
import subprocess
from screendumper_overlay import ScreendumperOverlay
from utils import screenshot_folder, show_in_systray, selected_region_coordinates

class ScreendumperApp(QApplication):
    def __init__(self, sys_argv, systray_enabled=True):
        super().__init__(sys_argv)
        self.tray_icon = None
        if systray_enabled and show_in_systray:
            self.init_systray()

    def init_systray(self):
        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("../assets/icon.png"), self)

        # Set up tray menu
        tray_menu = QMenu()
        
        # Select region and take screenshot
        start_action = QAction("Take Screenshot", self)
        start_action.triggered.connect(self.take_screenshot)
        tray_menu.addAction(start_action)
        
        # Take screenshot with previous selected region
        previous_region_action = QAction("Take Screenshot with Previous Region", self)
        previous_region_action.triggered.connect(self.take_screenshot_with_previous_region)
        tray_menu.addAction(previous_region_action)

        # Exit the app
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def save_coordinates(self, x, y, w, h):
        """Save the selected region coordinates to the config file."""
        with open(selected_region_coordinates, "w") as coordinates:
            coordinates.write(f"{x},{y},{w},{h}")

    def load_coordinates(self):
        """Load the coordinates from the config file."""
        try:
            with open(selected_region_coordinates, "r") as coordinates:
                x, y, w, h = coordinates.read().strip().split(",")
                return x, y, w, h
        except (FileNotFoundError, ValueError):
            return None

    def get_selection_coordinates(self):
        # Run `slop` to let the user select a region and return its coordinates
        try:
            output = subprocess.check_output(["slop", "-f", "%x,%y,%w,%h"])
            x, y, w, h = output.decode().strip().split(",")

            self.save_coordinates(x, y, w, h)  # Save coordinates for reuse

            return x, y, w, h
        except subprocess.CalledProcessError:
            print("Error capturing selection coordinates.")
            return None

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        selected_area_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        
        # Use `slop` to get the selection coordinates
        coords = self.get_selection_coordinates()
        
        if coords:
            # Capture the selected region with `scrot` using the obtained coordinates
            result = subprocess.run(["scrot", "-a", ",".join(coords), selected_area_path])

            if result.returncode == 0 and os.path.exists(selected_area_path):
                
                screen = QGuiApplication.primaryScreen()
                full_monitor_pixmap = screen.grabWindow(0)

                # Load the selected area QPixmap for clipboard use
                selected_area_pixmap = QPixmap(selected_area_path)

                # Display the overlay window, passing both the pixmap and the path
                self.overlay_window = ScreendumperOverlay(full_monitor_pixmap, selected_area_pixmap, selected_area_path, exit_after_action=(not show_in_systray))
                self.overlay_window.show()

    def take_screenshot_with_previous_region(self):
        """Take screenshot using the last saved region."""
        coords = self.load_coordinates()
        if not coords:
            print("No previous region saved.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        selected_area_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        
        # Use saved coordinates with `scrot`
        result = subprocess.run(["scrot", "-a", ",".join(coords), selected_area_path])

        if result.returncode == 0 and os.path.exists(selected_area_path):
            # Capture the full monitor screenshot and save in memory as a QPixmap
            screen = QGuiApplication.primaryScreen()
            full_monitor_pixmap = screen.grabWindow(0)

            # Load the selected area QPixmap for clipboard use
            selected_area_pixmap = QPixmap(selected_area_path)

            # Display the overlay window, passing both the pixmap and the screenshot path
            self.overlay_window = ScreendumperOverlay(full_monitor_pixmap, selected_area_pixmap, selected_area_path, exit_after_action=(not show_in_systray))
            self.overlay_window.show()

    def exit_app(self):
        # Hide the tray icon and quit the app
        if self.tray_icon:
            self.tray_icon.hide()
        self.quit()
