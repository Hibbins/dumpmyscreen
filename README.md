<div align="center">
  <img src="https://github.com/user-attachments/assets/75d0b65f-60b5-4af7-8f4b-fec657ced9b4" />
  <br />
  <h1 align="center">Dump My Screen</h1>
  <p align="center">All those screenshots, no longer lost in time like tears in rain.</p>
  <p>
    <a href="https://github.com/Hibbins/dumpmyscreen/stargazers" target="_blank"><img src="https://img.shields.io/github/stars/Hibbins/dumpmyscreen.svg" alt="GitHub Stars"/></a>
    <a href="https://github.com/Hibbins/dumpmyscreen/forks" target="_blank"><img src="https://img.shields.io/github/forks/Hibbins/dumpmyscreen.svg" alt="GitHub Forks"/></a>
    <a href="https://github.com/Hibbins/dumpmyscreen/releases" target="_blank"><img src="https://img.shields.io/github/release/Hibbins/dumpmyscreen.svg" alt="Releases"/></a>
    <a href="https://aur.archlinux.org/packages/dumpmyscreen" target="_blank"><img src="https://img.shields.io/aur/version/dumpmyscreen" alt="AUR Version"/></a>
    <a href="https://github.com/Hibbins/dumpmyscreen/issues" target="_blank"><img src="https://img.shields.io/github/issues/Hibbins/dumpmyscreen.svg" alt="GitHub Issues"/></a>
    <a href="https://github.com/Hibbins/dumpmyscreen/releases" target="_blank"><img src="https://img.shields.io/github/downloads/Hibbins/dumpmyscreen/total.svg" alt="Package Downloads"/></a>
    <a href="https://github.com/Hibbins/dumpmyscreen/blob/master/LICENSE" target="_blank"><img src="https://img.shields.io/github/license/Hibbins/dumpmyscreen.svg" alt="License"/></a>
  </p>
</div>
<br />
<div align="center">
  <a href="https://ko-fi.com/M4M615Y5RB" target="_blank"><img width="200" src="https://github.com/user-attachments/assets/91dc5e85-3b94-4424-920c-497b32fc30a4" alt='Buy Me a Coffee at ko-fi.com' /></a>
</div>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Linux](#linux)
    - [Arch Linux](#arch-linux)
- [Usage Guide](#usage-guide)
  - [Functions](#functions)
    - [Take Screenshot](#take-screenshot)
    - [Take Screenshot with Previous Region](#take-screenshot-with-previous-region)
    - [Executing application using flags](executing-application-using-flags)
  - [Options to Save or Copy File](#options-to-save-or-copy-file)
    - [Image to Clipboard](#image-to-clipboard)
    - [Save to Folder](#image-to-clipboard)
    - [Custom to Clipboard](#image-to-clipboard)
  - [Flags](#flags)
    - [Screenshot](#screenshot)
- [Configuration](#configuration)
  - [Options](#options)
    - [Screenshot folder](#screenshot-folder)
    - [Custom string](#custom-string)
    - [Show in systray](#show-in-systray)
    - [Selected region coordinates](#selected-region-coordinates)
    - [No compositor mode](#no-compositor-mode)

## Features

- Lightweight
- Possibility to copy custom command/string to clipboard, together with image path
- Remembers previously selected region, enables taking a new screenshot with same region again
- Configurable
- Can be executed with flags

## Installation

### Linux

#### Arch Linux

[Link to AUR](https://aur.archlinux.org/packages/dumpmyscreen)

Pacman:
```sh
sudo pacman -S dumpmyscreen
```

Yay:
```sh
yay -S dumpmyscreen
```

## Usage Guide
As the application is very lightweight and simple, there is not much to be said here.
But lets do a quick rundown of the main functionality at least.

### Functions

#### Take Screenshot
This function will trigger the crosshair the you can then use to select an area to screenshot.

#### Take Screenshot with Previous Region
Takes a screenshot using the coordinates from the previously selected region, when the last screenshot was taken.

#### Executing application using flags
You can execute the application using flags, currently there is only one flag, but there is a high chance that there will be more in the future.

See the [Flags](#flags) section for further information and examples on how to use it.

## Options to Save or Copy File

### Image to Clipboard
Saves the image to clipboard, you can then simply paste it into any application that can handle images directly from clipboard.

### Save to Folder
This option saves the screenshot to the directory chosen in the configuration, more info on screenshot folder can be found here [Screenshot folder](#screenshot-folder)

### Custom to Clipboard

## Flags

### Screenshot
The screenshot flag can be used to trigger the "Take screenshot" function directly. This can be useful if you want to take a screenshot using a script or for example bind it to a key in your Window Manager.

Usage:
```sh
dumpmyscreen --screenshot
```

Usage example using i3:
```sh
bindsym Print exec dumpmyscreen --screenshot
```

## Configuration
The configuration file is located here:
```sh
~/.config/dumpmyscreen/config.conf
```

### Options

#### Screenshot folder
The folder where all the screenshots will end up.

Default value:
```sh
Screenshotfolder = ~/.config/dumpmyscreen/screenshots
```

#### Custom string
Whenever "Custom to clipboard" or "CTRL + X" is pressed after taking a screenshot, the string that is saved in the config file, will be used together with the file path of the screenshot.

Example config value:
```sh
CustomString = /upload
```

Will yield:
```sh
/upload /home/username/.config/dumpmyscreen/screenshots/screenshot_YYYYMMDD_HHMMSS.png
```

#### Show in systray
This option defaults to true, whenever it is set to false, it will hide the icon from the system tray.

Default value:
```sh
ShowInSystray = true
```

#### Selected region coordinates
This option defaults to empty string, whenever you take a screenshot it will get populated with the coordinates of from the selected area when the user took the screenshot. These coordinates are then used for the "Take Screenshot with Previous Region" function.

This option is not something that needs to be manually configured, but simply a choice by me to use instead of having to store it in a temp file.

Default value:
```sh
SelectedRegionCoordinates = ""
```

#### No compositor mode
This option defaults to false. Whenever it is set to true, it will mimic the look of what the application would look like after taking a screenshot, on a system that actually has a compositor. So if you for example run a WM without a compositor, after taking a screenshot everything behind the floating window showing the screenshot preview would just be black. Set this to true and it will now show the desktop behind the floating window again. It is a little bit of a hack, so you can choose for yourself if this is for you or not.

If you have a compositor, just leave this at false.

Default value:
```sh
NoCompositorMode = false
```
