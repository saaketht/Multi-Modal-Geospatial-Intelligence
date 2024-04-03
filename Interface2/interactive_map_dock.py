import sys
import json
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtWebEngineWidgets
from ipyleaflet import Map, Marker, LayersControl, basemaps
from ipywidgets import HTML, IntSlider
from ipywidgets.embed import embed_data
import folium
import io
from pathlib import Path

from file_explorer_dock import *


class interactive_map_widget(QWidget):
    screenshotTaken = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.m = folium.Map(
            location=[28.598, -81.1974], tiles="openstreetmap",
            zoom_start=15)

        self.tabs = TabWidget(parent=None)
        self.tabs.setTabsClosable(False)
        self.tabs.setCornerWidget(None, Qt.Corner.TopRightCorner)
        self.tabs.setUsesScrollButtons(False)


        folium.TileLayer(attr="<a href=''></a>",
                         tiles="https://geoint-bucket.s3.amazonaws.com/tileserv/{z}/{x}/{y}.png").add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)

        self.w = QtWebEngineWidgets.QWebEngineView(self)

        self.w.setHtml(self.data.getvalue().decode())
        self.w1 = QtWebEngineWidgets.QWebEngineView(self)
        self.w1.setUrl(QUrl("https://earth.google.com/web/"))

        self.w1_layout = QVBoxLayout()
        self.w1_layout.setContentsMargins(10,10,10,10)
        self.w1_layout.addWidget(self.w1)

        self.w1_widget = QWidget()
        self.w1_widget.setLayout(self.w1_layout)

        self.w_layout = QVBoxLayout()
        self.w_layout.setContentsMargins(10, 10, 10, 10)
        self.w_layout.addWidget(self.w)

        self.w_widget = QWidget()
        self.w_widget.setLayout(self.w_layout)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,12,0,0)
        self.layout.addWidget(self.tabs)
        # self.map_dock_layout.addWidget(self.tabs)
        # self.setLayout(self.map_dock_layout)
        self.setLayout(self.layout)

        self.tabs.addTab2(self.w1_widget,"Google Earth")
        self.tabs.addTab2( self.w_widget,"Tile Server")
        self.tabs.setMovable(False)

        # self.analyzeButton = QPushButton('Analyze', self)
        # globe_icon = QIcon('feather/globe.svg')
        # self.analyzeButton.setIcon(globe_icon)
        # self.analyzeButton.setIconSize(QSize(20, 20))
        # self.analyzeButton.setFixedSize(QSize(109, 32))
        # self.analyzeButton.setStyleSheet("""
        #     QPushButton {
        #         padding: 6px 8px 6px 8px;
        #         border-radius: 10px;
        #         background-color: #202020;
        #         color: white;
        #         border: none;
        #         text-align: center;
        #         font-weight: bold;
        #         font-size: 14px;
        #         font-family: Arial;
        #     }
        #     QPushButton:hover {
        #         background:#494949;
        #     }
        #     QPushButton:pressed {
        #         background-color: #03B5A9;
        #     }
        # """)
        #
        # self.analyzeButton.clicked.connect(lambda: self.take_screenshot("uploads/screenshot.png"))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # button_width = self.analyzeButton.width()
        # button_height = self.analyzeButton.height()
        # new_x_position = int((self.width() - button_width) // 2)
        # new_y_position = int(self.height() - button_height - 10)
        # self.analyzeButton.move(new_x_position, new_y_position)

    def take_screenshot(self, file_path):
        pixmap = self.w.grab()
        if pixmap.save(file_path, "PNG"):
            self.screenshotTaken.emit(file_path)
