import configparser
import os

# Configuration file path and loading
config_path = os.path.expanduser("~/.config/dumpmyscreen/config.conf")
config = configparser.ConfigParser()
config.read(config_path)

# Get the screenshot folder path
screenshot_folder = os.path.expanduser(config.get("DEFAULT", "SCREENSHOT_FOLDER"))
# Get the custom string to be appended to clipboard
custom_string = config.get("DEFAULT", "CUSTOM_STRING")
# Get the boolean value that determines if systray is displayed
show_in_systray = config.getboolean("DEFAULT", "SHOW_IN_SYSTRAY")
# Get the region coordinates from the latest selection
selected_region_coordinates = config.get("DEFAULT", "SELECTED_REGION_COORDINATES", fallback="")
# Get the boolean that determines wheter to run no compositor mode or not
no_compositor_mode = config.getboolean("DEFAULT", "NO_COMPOSITOR_MODE")
