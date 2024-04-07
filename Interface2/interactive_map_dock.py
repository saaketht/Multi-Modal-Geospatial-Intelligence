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
from datetime import datetime
from file_explorer_dock import *

class CaptureFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: 2px solid white;")
        self.setWindowOpacity(0.5)
        self.resize(300, 200)  
        self.setMouseTracking(True)  
        self.mouse_pressed = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.BrushStyle.NoBrush)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.mouse_press_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            new_pos = event.globalPosition().toPoint() - self.mouse_press_pos
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False

class interactive_map_widget(QWidget):
    screenshotTaken = pyqtSignal(str)

    def __init__(self, app_data_path):
        super().__init__()

        #ADDED BC FILE_PATH PARAMETER NOT WORKING IN TAKE SCREENSHOT
        self.uploads_folder = os.path.join(app_data_path, "uploads")
        if not os.path.exists(self.uploads_folder):
                os.makedirs(self.uploads_folder)

        self.m = folium.Map(
            location=[28.598, -81.1974], tiles="openstreetmap",
            zoom_start=15)

        self.tabs = TabWidget(parent=None)
        self.tabs.setTabsClosable(False)

        testwidget = QWidget()
        testlayout = QHBoxLayout()
        testlayout.setContentsMargins(0,0,4,4)
        testlayout.setSpacing(2)
        testbutton = icon_button(initial_icon="feather/eye.svg")
        testbutton2 = icon_button(initial_icon="feather/camera.svg")
        testlayout.addWidget(testbutton2)
        testlayout.addWidget(testbutton)
        testwidget.setLayout(testlayout)

        #for qframe
        self.capture_frame = CaptureFrame(self)
        self.capture_frame.hide()
        testbutton.clicked.connect(self.show_capture_frame)
        testbutton2.clicked.connect(self.take_screenshot)

        self.tabs.setCornerWidget(testwidget, Qt.Corner.TopRightCorner)
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

    #displays qframe on the map
    def show_capture_frame(self):
        if self.capture_frame.isVisible():
            self.capture_frame.hide()
        else:
            self.capture_frame.show()
            self.capture_frame.raise_()
            self.center_capture_frame()

    def take_screenshot(self):
            pixmap = self.w.grab(self.capture_frame.geometry())
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  
            screenshot_filename = f"screenshot_{timestamp}.png"  
            file_path = os.path.join(self.uploads_folder, screenshot_filename)
            if pixmap.save(file_path, "PNG"):
                self.screenshotTaken.emit(file_path)
            self.capture_frame.hide()
    
    def center_capture_frame(self):
        map_widget_rect = self.w.geometry()
        map_widget_center = map_widget_rect.center()
        capture_frame_size = self.capture_frame.size()
        capture_frame_x = map_widget_center.x() - capture_frame_size.width() // 2
        capture_frame_y = map_widget_center.y() - capture_frame_size.height() // 2
        self.capture_frame.move(capture_frame_x, capture_frame_y)
        '''
    def take_screenshot(self, file_path):
        pixmap = self.w.grab()
        if pixmap.save(file_path, "PNG"):
            self.screenshotTaken.emit(file_path)
    '''
