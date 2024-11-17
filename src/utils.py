import configparser
import os

# Configuration file path and loading
config_path = os.path.expanduser("~/.config/dumpmyscreen/config.conf")
config = configparser.ConfigParser()
config.read(config_path)

# Get the screenshot folder path
screenshot_folder = os.path.expanduser(config.get("DEFAULT", "SCREENSHOT_FOLDER"))
# Get the boolean value that determines if systray is displayed
show_in_systray = config.getboolean("DEFAULT", "SHOW_IN_SYSTRAY")
# Get the region coordinates from the latest selection
selected_region_coordinates = config.get("DEFAULT", "SELECTED_REGION_COORDINATES", fallback="")
