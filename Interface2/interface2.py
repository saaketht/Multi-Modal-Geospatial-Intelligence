import sys
import os
import shutil
from component_file import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QDockWidget, QTabWidget, QListWidget,
    QPlainTextEdit, QFileDialog, QMessageBox, QGridLayout, QToolBar, QListWidgetItem, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QEvent, QTimer, QDataStream, QIODevice, QFile
from PyQt6.QtGui import QPixmap, QIcon, QAction, QFontDatabase, QFontMetrics
import platform, ctypes
from file_explorer_dock import *
from image_preview_dock import *
from interactive_map_dock import *
from chatbox_file import *
from chat_history_dock import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MM-GEOINT")
        self.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks | QMainWindow.DockOption.AllowNestedDocks)

        # chatbox attributes
        self.titlebar = None
        self.chatbox_layout = None

        # Set the type of location/path where application data should be stored
        self.app_data_path_type = QStandardPaths.StandardLocation.AppDataLocation
        # Get the full path where application data should be written
        # uncommented by saaketh
        self.app_data_path = QStandardPaths.writableLocation(self.app_data_path_type)

        # css styles
        self.setStyleSheet('''
                QMainWindow
                {
                    background-color: #494949;
                }
                QMainWindow::separator 
                {
                    width:1px;
                    background-color: #494949;
                }
                ''')

        self.setup_main_window()
        # self.load_chat_history()
        self.setup_menus()
        self.showMaximized()

    def setup_main_window(self):
        layout = QVBoxLayout()
        self.titlebar = TitleBar("Chat Box")
        self.titlebar.setFixedHeight(38)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.titlebar)

        chatbox_frame = QFrame()
        self.chatbox_layout = QVBoxLayout(chatbox_frame)
        chatbox_frame.setLayout(self.chatbox_layout)
        chatbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chatbox_layout.setContentsMargins(0, 14, 0, 0)
        self.chatbox_layout.setSpacing(0)
        chatbox_frame.setStyleSheet('''
                QFrame {
                    background: #202020;
                    border: 2px solid #494949;
                    border-radius:10px;
                }
                ''')

        layout.addWidget(chatbox_frame)

        # check paths
        print("QStandardPaths::StandardLocation type: " + str(self.app_data_path_type))
        print("App Data Directory: " + str(self.app_data_path))

        # from chat_history_dock.py
        self.chat_history_widget = ChatHistoryListWidget(app_data_path=self.app_data_path)

        # from chatbox_file.py
        self.tabs = ChatTabWidget(parent=None, app_data_path=self.app_data_path,
                                  chat_history_widget=self.chat_history_widget)
        self.chatbox_layout.addWidget(self.tabs)

        self.chat_history_widget.setChatTabWidget(self.tabs)

        self.chat_history_widget_dock = DockWidget("Chat History", self.chat_history_widget, self)

        # layout.addWidget(chatbox_frame)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        # Interactive Map Dock Widget
        map_placeholder = QLabel("Interactive Map Placeholder")
        map_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        interactive_map = interactive_map_widget()

        # map_placeholder.setStyleSheet("border: none; background-color: #202020;")
        self.map_dock_widget = DockWidget("Interactive Map", interactive_map, self)
        self.map_dock_widget.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)

        # Image Preview Dock Widget
        self.image_preview_label = image_preview_widget("Image Preview/Selection")
        self.image_preview_dock_widget = DockWidget("Image Preview", self.image_preview_label, self)

        # The following 2 lines of code add the QDockWidget (the  self.map_dock_widget and self.image_preview_dock_widget) to the Main Window
        # self.splitDockWidget(self.map_dock_widget, self.image_preview_dock_widget, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.image_preview_dock_widget)

        # File Explorer Dock Widget
        # self.file_explorer_dock_widget = self.createFileExplorerWidget()
        self.file_explorer_widget = file_explorer(self.image_preview_label, self.tabs)
        self.file_explorer_dock_widget = DockWidget("File Explorer", self.file_explorer_widget, self)

        # Add the self.file_explorer_dock_widget to main window.
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_history_widget_dock)

        interactive_map.screenshotTaken.connect(self.file_explorer_widget.add_new_file)
        # Dock configuration settings
        # self.setDockNestingEnabled(True)
        # self.resizeDocks([self.map_dock_widget, self.image_preview_dock_widget], [1, 1], Qt.Orientation.Vertical)

    def setup_menus(self):
        menubar = self.menuBar()

        viewMenu = menubar.addMenu("&View")

        self.add_view_menu_action(viewMenu, "Interactive Map", self.map_dock_widget)
        self.add_view_menu_action(viewMenu, "Image Preview", self.image_preview_dock_widget)
        self.add_view_menu_action(viewMenu, "Map File Explorer", self.file_explorer_dock_widget)

    def add_view_menu_action(self, menu, title, dock_widget):
        action = QAction(title, self, checkable=True)

        action.setChecked(dock_widget.isVisible())

        action.triggered.connect(lambda checked: dock_widget.setVisible(checked))

        dock_widget.visibilityChanged.connect(action.setChecked)

        menu.addAction(action)


# def main():
app = QApplication(sys.argv)
app.setApplicationName("GEOINT")
app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
if platform.system() == "Windows":
    if int(platform.release()) >= 8:
        print(platform.release())
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
window = MainWindow()
window.show()
sys.exit(app.exec())
# if __name__ == "__main__":
#     main()
