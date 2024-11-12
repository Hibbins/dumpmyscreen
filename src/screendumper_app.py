from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from datetime import datetime
import os
import subprocess
from screendumper_overlay import ScreendumperOverlay
from utils import config, get_active_monitor_geometry

# Load configuration values
screenshot_folder = os.path.expanduser(config.get("DEFAULT", "SCREENSHOT_FOLDER"))
show_in_systray = config.getboolean("DEFAULT", "SHOW_IN_SYSTRAY")

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
        start_action = QAction("Take Screenshot", self)
        start_action.triggered.connect(self.take_screenshot)
        tray_menu.addAction(start_action)
        
        # Add exit action to tray menu
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        selected_area_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        full_monitor_path = os.path.join(screenshot_folder, "full_monitor_screenshot.png")
        
        # Start scrot in selection mode to let user select an area
        result = subprocess.run(["scrot", "-s", selected_area_path])

        if result.returncode == 0 and os.path.exists(selected_area_path):
            # Get the active monitor geometry
            monitor_geometry = get_active_monitor_geometry()
            if monitor_geometry:
                width, height, x_offset, y_offset = monitor_geometry
                # Take a full monitor screenshot after selection
                subprocess.run(["scrot", "-a", f"{x_offset},{y_offset},{width},{height}", full_monitor_path])

                # Show the overlay window with buttons
                self.overlay_window = ScreendumperOverlay(full_monitor_path, selected_area_path, exit_after_action=(not show_in_systray))
                self.overlay_window.show()

    def exit_app(self):
        # Hide the tray icon and quit the app
        if self.tray_icon:
            self.tray_icon.hide()
        self.quit()
