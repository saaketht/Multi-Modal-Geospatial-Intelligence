
# This file contains widgets related to the Interactive Map Window

import io
from datetime import datetime
from PyQt6 import QtWebEngineWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import QPainter
from  folium import Map, TileLayer
from localtileserver import get_folium_tile_layer, TileClient
from file_explorer_dock import *

# This widget encapsulates the local tiler server repo/program from Bane Sullivan
class localTileServer (QWidget):
    # Signal turns off button in File Explorer window when another tiff/tif image has been
    # prompted to be graphed
    toggleOffFileExplorerButton = pyqtSignal(QListWidgetItem)

    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Attributes
        self.list_widget_item_index = -1  # Holds the List widget item, NOT the index, its functionality changed
        self.currentImagePath = ""  # Holds the current image path
        self.currentImage = None  # Holds the QPixmap of the image
        self.is_an_image = False   # Bool val of whether an image has been graphed
        self.t = None  # Client for tiff images

        # Widget has a layout to nest a widget within
        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(10,10,10,10)
        self.Layout.setSpacing(0)

        # Create a Folium Map from localtileserver module
        self.m = Map()

        # Data storage for map
        self.data = io.BytesIO()

        # Save the map's data
        self.m.save(self.data, close_file=False)

        # Create a QtWebEngineWidgets.QWebEngineView to view the Folium map
        self.w = QtWebEngineWidgets.QWebEngineView(self)

        # Decode the folium map onto the QtWebEngineWidgets.QWebEngineView widget
        self.w.setHtml(self.data.getvalue().decode())

        # Add the QtWebEngineWidgets.QWebEngineView widget to the layout
        self.Layout.addWidget(self.w)

        # Set the layout for this widget
        self.setLayout(self.Layout)

    # This method will update the map with a tiff image graphed
    def displayGeoTiff(self, file_path):
        # Get the client of the tiff file
        client = TileClient(file_path)

        # Create the layer of the tiff client
        self.t = get_folium_tile_layer(client)

        # Create a Folium Map from localtileserver module the map and set the coordinates
        # to the center of the layer
        self.m = Map(location=client.center(), zoom_start=16)

        # add the layer
        self.m.add_child(self.t)

        # Save the data
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)

        # Decode the folium map onto the QtWebEngineWidgets.QWebEngineView widget
        self.w.setHtml(self.data.getvalue().decode())

    # This method resets the map to the original view when the tiff image has been ungraphed.
    def resetMap(self):
        # Create a Folium Map from localtileserver module
        self.m = Map()

        # Data storage for map
        self.data = io.BytesIO()

        # Save the map's data
        self.m.save(self.data, close_file=False)

        # Decode the folium map onto the QtWebEngineWidgets.QWebEngineView widget
        self.w.setHtml(self.data.getvalue().decode())

# This widget creates a frame that is overlaid over the map to screenshot geospatial data from the
# map
class CaptureFrame(QFrame):
    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Here we set the window settings
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # Set stylesheet for frame
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border: 2px dotted white;")

        # make window slightly opaque to view what is being captured
        self.setWindowOpacity(0.5)

        # make frame size 300 by 200
        self.resize(300, 200)
        self.setMouseTracking(True)  
        self.mouse_pressed = False

    # Here we override the paint event to draw the frame
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

# This is the interactive map widget that will be displayed in the Interactive Map Window
class interactive_map_widget(QWidget):
    # This signal notifies the file explorer that a screenshot has been taken so
    # the image can be appended to file explorer
    screenshotTaken = pyqtSignal(str)

    # Constructor, the app_data_path parameter is the path to the application's folder
    def __init__(self, app_data_path):
        # Call the Parent Constructor
        super().__init__()

        # Get the uploads folder path from the application's folder, if the folder does not
        # exist create one
        self.uploads_folder = os.path.join(app_data_path, "uploads")
        if not os.path.exists(self.uploads_folder):
                os.makedirs(self.uploads_folder)

        # Create a map from Folium module, center it at the University of Central Florida
        # let basemap be the openstreetmaps
        self.m = Map(
            location=[28.598, -81.1974], tiles="openstreetmap",
            zoom_start=15)

        # The widget will consists of tabs to switch between the localtileserver widget and
        # a custom tile layer
        self.tabs = TabWidget(parent=None)
        self.tabs.setTabsClosable(False)

        # Create a widget to host two corner buttons for screenshotting
        corner_widget = QWidget()
        corner_widget_layout = QHBoxLayout()
        corner_widget_layout.setContentsMargins(0, 0, 4, 4)
        corner_widget_layout.setSpacing(2)
        button = icon_button(initial_icon="feather/eye.svg")
        button2 = icon_button(initial_icon="feather/camera.svg")
        corner_widget_layout.addWidget(button2)
        corner_widget_layout.addWidget(button)
        corner_widget.setLayout(corner_widget_layout)

        # Create an instance of the Capture Frame widget
        self.capture_frame = CaptureFrame(self)
        self.capture_frame.hide() # Make it hidden at first

        # Connect the corner buttons for screen shotting
        button.clicked.connect(self.show_capture_frame)
        button2.clicked.connect(self.take_screenshot)

        # Set the corner widget to the tab widget
        self.tabs.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)
        self.tabs.setUsesScrollButtons(False) # Deactivate scroll button feature to streamline design

        # The following links are map tile layers.
        # https://geoint-bucket.s3.amazonaws.com/tileserv/{z}/{x}/{y}.png
        # https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
        TileLayer(attr="<a href=''></a>",
                         tiles="https://geoint-bucket.s3.amazonaws.com/tileserv/{z}/{x}/{y}.png").add_to(self.m)
        self.data = io.BytesIO()

        # Save the map's data
        self.m.save(self.data, close_file=False)

        # Create a QtWebEngineWidgets.QWebEngineView to view the Folium map
        self.w = QtWebEngineWidgets.QWebEngineView(self)

        # Decode the folium map onto the QtWebEngineWidgets.QWebEngineView widget
        self.w.setHtml(self.data.getvalue().decode())

        # Layout fo the QtWebEngineWidget
        self.w_layout = QVBoxLayout()
        self.w_layout.setContentsMargins(10, 10, 10, 10)
        self.w_layout.addWidget(self.w)

        # Create a widget to host the layout that hosts the QtWebEngineWidgets.QWebEngineView
        self.w_widget = QWidget()
        self.w_widget.setLayout(self.w_layout)

        # Create a layout for this widget to host the tabs widget
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,12,0,0)
        self.layout.addWidget(self.tabs)

        # Set this widget's layout
        self.setLayout(self.layout)

        # Initialize the localTileServer widget
        self.w3_widget = localTileServer()

        # Creat two tabs, one with the map layer and the other with the localTileServer widget
        self.tabs.addTab2( self.w_widget,"Tile Server")
        self.tabs.addTab2(self.w3_widget, "LocalTileServer")

        # Disable tab mobility
        self.tabs.setMovable(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    # This method displays Qframe on the map
    def show_capture_frame(self):
        # If the frame is already visible toggle OFF QFrame's visibility
        if self.capture_frame.isVisible():
            self.capture_frame.hide()

        # If the frame is NOT already visible toggle ON QFrame's visibility
        else:
            self.capture_frame.show()
            self.capture_frame.raise_()
            self.center_capture_frame()

    # This method screenshots the image and saves it
    def take_screenshot(self):
            # Get the current widget
            widget = self.tabs.currentWidget()

            # Capture the content of that widget from frame
            pixmap = widget.grab(self.capture_frame.geometry())

            # Store the filename as the time it was taken
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  
            screenshot_filename = f"screenshot_{timestamp}.png"

            # Add that image to the file explorer.
            file_path = os.path.join(self.uploads_folder, screenshot_filename)

            # If save was successful, then emit the file path to append the file to the File Explorer
            if pixmap.save(file_path, "PNG"):
                self.screenshotTaken.emit(file_path)

            # After screenshot hide the Frame
            self.capture_frame.hide()

    # This method actually determines what to capture in the screenshot
    # based off the QFrame's location
    def center_capture_frame(self):
        map_widget_rect = self.w.geometry()
        map_widget_center = map_widget_rect.center()
        capture_frame_size = self.capture_frame.size()
        capture_frame_x = map_widget_center.x() - capture_frame_size.width() // 2
        capture_frame_y = map_widget_center.y() - capture_frame_size.height() // 2
        self.capture_frame.move(capture_frame_x, capture_frame_y)

