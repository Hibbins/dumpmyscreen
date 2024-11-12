from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QKeySequence
from draw_button_labels import DrawButtonLabels
from utils import config, screenshot_folder
import subprocess
import os
from datetime import datetime

custom_string = config.get("DEFAULT", "CUSTOM_STRING")

class ScreendumperOverlay(QWidget):
    def __init__(self, full_monitor_path, selected_area_path, exit_after_action=False):
        super().__init__()
        self.full_monitor_path = full_monitor_path
        self.selected_area_path = selected_area_path
        self.exit_after_action = exit_after_action
        self.initUI()

    def initUI(self):
        # Set window to frameless, translucent, and full-screen on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Explicitly request focus
        self.activateWindow()
        self.raise_()
        self.setFocus()

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
        self.layout.addWidget(btn_copy)

        # Shortcut label for "Copy to Clipboard"
        label_copy = DrawButtonLabels("CTRL + C", self)
        label_copy.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label_copy)

        # Save to Folder button
        btn_save = QPushButton("Save to Folder", self)
        btn_save.clicked.connect(self.save_to_folder)
        self.layout.addWidget(btn_save)

        # Shortcut label for "Save to Folder"
        label_save = DrawButtonLabels("CTRL + S", self)
        label_save.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label_save)

    def keyPressEvent(self, event):
        # Detect keyboard shortcuts and trigger the corresponding action
        if event.matches(QKeySequence.Copy):  # CTRL + C
            self.copy_to_clipboard()
        elif event.matches(QKeySequence.Save):  # CTRL + S
            self.save_to_folder()
        else:
            # Call parent event handler for any unhandled keys
            super().keyPressEvent(event)

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
        self.cleanup_and_exit()

    def paintEvent(self, _event):
        painter = QPainter(self)
        # Draw the full monitor screenshot as background
        painter.drawPixmap(self.rect(), self.background)
        
        # Draw the dimmed overlay on top
        painter.setBrush(Qt.black)
        painter.setOpacity(0.3)
        painter.drawRect(self.rect())

    def cleanup_and_exit(self):
        # Close the overlay first, then delete the background file after a short delay
        self.close()
        
        # Quit the application immediately if this is a one-shot instance
        if self.exit_after_action:
            QApplication.instance().quit

        # Delay the deletion of the full monitor screenshot to reduce flicker
        if os.path.exists(self.full_monitor_path):
            os.remove(self.full_monitor_path)
