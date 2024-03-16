from component_file import *
from PyQt6.QtWidgets import (
    QLabel
)
class image_preview_widget(QLabel):
    def __init__(self, text=None):
        super().__init__(text=text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(True)
        self.setMaximumSize(315, 317)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.currentImage = None
        self.currentImagePath = None