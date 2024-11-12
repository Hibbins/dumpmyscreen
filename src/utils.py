import configparser
import os
import re
import subprocess

# Configuration file path and loading
config_path = os.path.expanduser("~/.config/dumpmyscreen/config.conf")
config = configparser.ConfigParser()
config.read(config_path)

# Get the screenshot folder path
screenshot_folder = os.path.expanduser(config.get("DEFAULT", "SCREENSHOT_FOLDER"))

def get_active_monitor_geometry():
    try:
        xrandr_output = subprocess.check_output("xrandr --query", shell=True).decode()
        
        primary_monitor_name_match = re.search(r"(\w+-\d+)\sconnected\sprimary", xrandr_output)
        if primary_monitor_name_match:
            primary_monitor_name = primary_monitor_name_match.group(1)
            primary_monitor_geometry_match = re.search(
                rf"{primary_monitor_name}\sconnected\sprimary\s(\d+)x(\d+)\+(\d+)\+(\d+)",
                xrandr_output
            )
            if primary_monitor_geometry_match:
                return map(int, primary_monitor_geometry_match.groups())

        first_connected_monitor_match = re.search(r"(\w+-\d+)\sconnected\s(\d+)x(\d+)\+(\d+)\+(\d+)", xrandr_output)
        if first_connected_monitor_match:
            return map(int, first_connected_monitor_match.groups()[1:])
        
        print("Error: No active monitor detected.")
        return None

    except subprocess.CalledProcessError:
        print("Error: Failed to execute xrandr command.")
        return None
