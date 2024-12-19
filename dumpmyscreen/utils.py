import configparser
import os

# Configuration file path
config_dir = os.path.expanduser("~/.config/dumpmyscreen")
config_path = os.path.join(config_dir, "config.conf")

# Path to screenshot directory
screenshot_dir = os.path.join(config_dir, "screenshots")

# Initialize the ConfigParser
config = configparser.ConfigParser()
config.read(config_path)

# Check if the config file exists, if it doesn't, create it
if not os.path.exists(config_path):
    # Manually write the configuration
    with open(config_path, "w") as configfile:
        configfile.write("""\
            [DEFAULT]
            Screenshotfolder = ~/.config/dumpmyscreen/screenshots
            CustomString = ""
            ShowInSystray = true
            SelectedRegionCoordinates = ""
            NoCompositorMode = false
        """)

# Utility functions
def get_config_value(key):
    """Fetch a configuration value by key."""
    try:
        return config.get("DEFAULT", key)
    except configparser.NoOptionError:
        print(f"Key {key} not found in config.")
        return None


def update_config(key, value):
    """Update a configuration value and write it to the config file."""
    config.set("DEFAULT", key, value)
    with open(config_path, "w") as configfile:
        config.write(configfile)
