#!/usr/bin/env python3
import sys
from .screendumper_app import ScreendumperApp

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
