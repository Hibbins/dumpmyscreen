#!/usr/bin/env python3
import sys
import os
from .screendumper_app import ScreendumperApp

# Configuration directory
config_dir = os.path.expanduser("~/.config/dumpmyscreen")

# Path to screenshot directory
screenshot_dir = os.path.join(config_dir, "screenshots")

# Ensure the configuration & screenshot directory exists
os.makedirs(config_dir, exist_ok=True)
os.makedirs(screenshot_dir, exist_ok=True)

def main():
    """Entry point for the application."""
    if "--screenshot" in sys.argv:
        app = ScreendumperApp(sys.argv, systray_enabled=False)
        app.take_screenshot()
        app.setQuitOnLastWindowClosed(True)
        sys.exit(app.exec_())
    else:
        app = ScreendumperApp(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        sys.exit(app.exec_())

# Main block
if __name__ == "__main__":
    main()
