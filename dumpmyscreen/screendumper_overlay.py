from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QKeySequence, QGuiApplication
from .draw_button_labels import DrawButtonLabels
from .utils import get_config_value
import subprocess
import os
from datetime import datetime

class ScreendumperOverlay(QWidget):
    def __init__(self, full_monitor_pixmap, selected_pixmap, selected_area_path, exit_after_action=False):
        super().__init__()
        self.screenshot_folder = os.path.expanduser(get_config_value("ScreenshotFolder"))
        self.custom_string = get_config_value("CustomString")
        self.full_monitor_pixmap = full_monitor_pixmap  # full screen pixmap
        self.selected_pixmap = selected_pixmap  # selected area pixmap
        self.selected_area_path = selected_area_path  # For file path usage in custom string & save to folder
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

        # Main layout for the preview and buttons
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Add the selected area preview to the layout
        self.add_selected_area_preview()

        # Add action buttons below the preview
        self.add_action_buttons()

        self.setLayout(self.layout)

    def add_selected_area_preview(self):
        # Create a QLabel to display the selected area preview from the in-memory pixmap
        self.preview_label = QLabel(self)
        self.preview_label.setPixmap(self.selected_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.preview_label.setAlignment(Qt.AlignCenter)

        # Add the preview to the layout
        self.layout.addWidget(self.preview_label)

    def add_action_buttons(self):
        # Copy to Clipboard button
        btn_copy = QPushButton("Image to Clipboard", self)
        btn_copy.clicked.connect(self.copy_image_to_clipboard)
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

        # Copy custom string to clipboard
        btn_custom = QPushButton("Custom to clipboard", self)
        btn_custom.clicked.connect(self.copy_custom_string_to_clipboard)
        self.layout.addWidget(btn_custom)

        # Shortcut label for "Save to Folder"
        label_custom = DrawButtonLabels("CTRL + X", self)
        label_custom.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label_custom)

    def keyPressEvent(self, event):
        # Detect keyboard shortcuts and trigger the corresponding action
        if event.matches(QKeySequence.Copy):  # CTRL + C
            self.copy_image_to_clipboard()
        elif event.matches(QKeySequence.Save):  # CTRL + S
            self.save_to_folder()
        elif event.key() == Qt.Key_Escape:  # Pressing ESC key exits the app
            print("Escape key pressed. Exiting overlay.")
            self.cleanup_and_exit()
        else:
            # Call parent event handler for any unhandled keys
            super().keyPressEvent(event)

    def copy_image_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setPixmap(self.selected_pixmap)  # Use the QPixmap directly

        # Close the overlay or exit if this is a single-use instance
        self.cleanup_and_exit(remove_file=True)

    def copy_custom_string_to_clipboard(self):
        if self.custom_string:
            # Save selected_pixmap to file only if selected_area_path is empty
            if not self.selected_area_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.selected_area_path = os.path.join(self.screenshot_folder, f"screenshot_{timestamp}.png")
                self.selected_pixmap.save(self.selected_area_path)

            # Prepare clipboard content with custom string and file path
            clipboard_content = f"{self.custom_string} {self.selected_area_path}"
            subprocess.run(["xclip", "-selection", "clipboard"], input=clipboard_content, text=True)
        else:
            # If CUSTOM_STRING is not populated, copy only the path (or notify if path is empty)
            clipboard_content = self.selected_area_path or "No screenshot path available."
            subprocess.run(["xclip", "-selection", "clipboard"], input=clipboard_content, text=True)
            print("Warning: CUSTOM_STRING is not defined. Only screenshot path will be copied.")

        self.cleanup_and_exit()

    def save_to_folder(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.screenshot_folder, f"screenshot_{timestamp}.png")

        self.selected_pixmap.save(save_path)  # Save the selected area directly from pixmap

        if self.selected_area_path != save_path:
            self.cleanup_and_exit(remove_file=True)

    def paintEvent(self, _event):
        painter = QPainter(self)

        if self.full_monitor_pixmap:
            # Draw the full monitor screenshot from in-memory pixmap as background
            painter.drawPixmap(self.rect(), self.full_monitor_pixmap)
        
        # Draw the dimmed overlay on top
        painter.setBrush(Qt.black)
        painter.setOpacity(0.3)
        painter.drawRect(self.rect())

    def cleanup_and_exit(self, remove_file=False):
        # Close the overlay first
        self.close()

        # Remove file from disk
        if os.path.exists(self.selected_area_path) and remove_file:
            os.remove(self.selected_area_path)
        
        # Quit the application immediately if this is a one-shot instance
        if self.exit_after_action:
            QApplication.instance().quit()
