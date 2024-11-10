#!/usr/bin/env python3
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
from datetime import datetime
import sys
import os
import configparser

# Configuration file path
config_path = os.path.expanduser("~/.config/dumpmyscreen/config.conf")

# Parse the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get configuration values
screenshot_folder = os.path.expanduser(config.get("DEFAULT", "SCREENSHOT_FOLDER"))
custom_string = config.get("DEFAULT", "CUSTOM_STRING")
listen_for_keystroke = config.getboolean("DEFAULT", "LISTEN_FOR_KEYSTROKE")
trigger_key = config.get("DEFAULT", "TRIGGER_KEY")

# Ensure screenshot folder exists
os.makedirs(screenshot_folder, exist_ok=True)

class ScreenshotOverlay(QWidget):
    def __init__(self, full_monitor_path, selected_area_path):
        super().__init__()
        self.full_monitor_path = full_monitor_path
        self.selected_area_path = selected_area_path
        self.initUI()

    def initUI(self):
        # Set window to frameless, translucent, and full-screen on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Load the full monitor screenshot into a pixmap for display
        self.background = QPixmap(self.full_monitor_path)
        
        # Main layout for the preview and buttons
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Add the selected area preview to the layout
        self.add_selected_area_preview()

        # Add action buttons below the preview
        self.add_action_buttons()
        
        self.setLayout(self.layout)

    def add_selected_area_preview(self):
        # Create a QLabel to display the selected area preview
        self.preview_label = QLabel(self)
        self.preview_label.setPixmap(QPixmap(self.selected_area_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.preview_label.setAlignment(Qt.AlignCenter)

        # Add the preview to the layout
        self.layout.addWidget(self.preview_label)

    def add_action_buttons(self):
        # Copy to Clipboard button
        btn_copy = QPushButton("Copy to Clipboard", self)
        btn_copy.clicked.connect(self.copy_to_clipboard)
        
        # Save to folder button
        btn_save = QPushButton("Save to Folder", self)
        btn_save.clicked.connect(self.save_to_folder)

        # Add buttons to layout
        self.layout.addWidget(btn_copy)
        self.layout.addWidget(btn_save)

    def copy_to_clipboard(self):
        if custom_string:
            # If CUSTOM_STRING is populated, copy string and screenshot path to clipboard
            clipboard_content = f"{custom_string} {self.selected_area_path}"
            subprocess.run(["echo", clipboard_content], check=True, text=True, stdout=subprocess.PIPE)
            subprocess.run(["xclip", "-selection", "clipboard"], input=clipboard_content, text=True)
        else:
            # If CUSTOM_STRING is not populated or defined, copy the image itself to the clipboard instead
            subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", self.selected_area_path])
        
        self.cleanup_and_exit()

    def save_to_folder(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        QPixmap(self.selected_area_path).save(save_path)
        print(f"Selected area saved to {save_path}")
        self.cleanup_and_exit()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw the full monitor screenshot as background
        painter.drawPixmap(self.rect(), self.background)
        
        # Draw the dimmed overlay on top
        painter.setBrush(Qt.black)
        painter.setOpacity(0.3)
        painter.drawRect(self.rect())

    def cleanup_and_exit(self):
        # Remove the temporary full monitor screenshot file
        if os.path.exists(self.full_monitor_path):
            os.remove(self.full_monitor_path)
        self.close()
        QApplication.instance().quit()

def get_active_monitor_geometry():
    try:
        # Query xrandr for monitor information
        xrandr_output = subprocess.check_output("xrandr --query", shell=True).decode()
        
        # Search for the primary monitor's name
        primary_monitor_name_match = re.search(r"(\w+-\d+)\sconnected\sprimary", xrandr_output)
        
        if primary_monitor_name_match:
            primary_monitor_name = primary_monitor_name_match.group(1)
            
            # Search for the primary monitor's geometry and offset
            primary_monitor_geometry_match = re.search(
                rf"{primary_monitor_name}\sconnected\sprimary\s(\d+)x(\d+)\+(\d+)\+(\d+)",
                xrandr_output
            )
            
            if primary_monitor_geometry_match:
                width, height, x_offset, y_offset = map(int, primary_monitor_geometry_match.groups())
                return width, height, x_offset, y_offset

        # If no primary monitor, fall back to the first connected monitor
        first_connected_monitor_match = re.search(r"(\w+-\d+)\sconnected\s(\d+)x(\d+)\+(\d+)\+(\d+)", xrandr_output)
        if first_connected_monitor_match:
            width, height, x_offset, y_offset = map(int, first_connected_monitor_match.groups()[1:])
            return width, height, x_offset, y_offset
        
        # Log an error if no active monitor is detected
        print("Error: No active monitor detected.")
        return None

    except subprocess.CalledProcessError:
        print("Error: Failed to execute xrandr command.")
        return None

def take_screenshot():
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
            
            # Launch the overlay window with the full monitor screenshot as background and buttons
            app = QApplication(sys.argv)
            overlay_window = ScreenshotOverlay(full_monitor_path, selected_area_path)
            overlay_window.show()
            sys.exit(app.exec_())
    else:
        print("Screenshot canceled or no area selected.")

if __name__ == "__main__":
    take_screenshot()
