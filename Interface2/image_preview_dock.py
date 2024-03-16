from component_file import *
from PyQt6.QtWidgets import (
    QLabel
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QPoint
class image_preview_widget(QWidget):
    def __init__(self, text=None):
        super().__init__()
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setScaledContents(True)
        # #self.setMaximumSize(315, 317)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.currentImage = None
        self.currentImagePath = None
        self.p = QPixmap()
    def setPixmap(self, p):
        self.p = p
        self.update()
    def clear(self):
        self.p = QPixmap()
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)