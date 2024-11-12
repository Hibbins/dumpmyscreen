from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class DrawButtonLabels(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.text = text

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        outline_color = QColor(Qt.black)
        text_color = QColor(Qt.white)

        painter.setPen(outline_color)
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            painter.drawText(self.rect().adjusted(dx, dy, dx, dy), Qt.AlignCenter, self.text)

        painter.setPen(text_color)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
