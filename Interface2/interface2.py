import ctypes
import platform

from chat_history_dock import *
from chatbox_file import *
from file_explorer_dock import *
from image_preview_dock import *
from interactive_map_dock import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MM-GEOINT")
        self.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks | QMainWindow.DockOption.AllowNestedDocks)

        # chatbox/dock attributes - subject to change
        self.titlebar = None
        self.chatbox_layout = None
        self.image_preview_label = None
        # widget attributes - subject to change
        self.chat_history_list_widget = None
        self.tabs = None
        self.chat_history_dock_widget = None
        self.map_dock_widget = None
        self.image_preview_dock_widget = None
        self.file_explorer_widget = None
        self.file_explorer_dock_widget = None

        # Set the type of location/path where application data should be stored
        self.app_data_path_type = QStandardPaths.StandardLocation.AppDataLocation
        # Get the full path where application data should be written
        # uncommented below
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
        self.titlebar = TitleBar("Chat Box")
        self.titlebar.setFixedHeight(38)

        # layout for main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.titlebar)

        # create QFrame for chatbox QVBoxLayout
        chatbox_frame = QFrame()
        self.chatbox_layout = QVBoxLayout(chatbox_frame)
        chatbox_frame.setLayout(self.chatbox_layout)
        chatbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chatbox_layout.setContentsMargins(0, 12, 0, 0)
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

        # instantiate Chat History List Widget
        # chat_history_dock.py
        self.chat_history_list_widget = ChatHistoryListWidget(app_data_path=self.app_data_path)

        # instantiate ChatTabWidget (chat tabs) and pass Chat History List Widget
        # chatbox_file.py
        self.tabs = ChatTabWidget(parent=None, app_data_path=self.app_data_path,
                                  chat_history_widget=self.chat_history_list_widget)
        # add ChatTabWidget to chatbox QVBoxLayout
        self.chatbox_layout.addWidget(self.tabs)

        # access ChatTabWidget from Chat History List Widget
        self.chat_history_list_widget.setChatTabWidget(self.tabs)
        # instantiate Chat History DockWidget to display Chat History List Widget
        self.chat_history_dock_widget = DockWidget("Chat History", self.chat_history_list_widget, self)

        # create central_widget
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        # Interactive Map Dock Widget
        map_placeholder = QLabel("Interactive Map Placeholder")
        map_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.interactive_map = interactive_map_widget()

        # map_placeholder.setStyleSheet("border: none; background-color: #202020;")
        self.map_dock_widget = DockWidget("Interactive Map", self.interactive_map, self)
        self.map_dock_widget.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)

        # Image Preview Dock Widget
        self.image_preview_label = image_preview_widget("Image Preview/Selection")
        self.image_preview_dock_widget = DockWidget("Image Preview", self.image_preview_label, self)

        # The following 2 lines of code add these QDockWidgets to MainWindow
        # (the map_dock_widget and image_preview_dock_widget)
        # self.splitDockWidget(self.map_dock_widget, self.image_preview_dock_widget, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.image_preview_dock_widget)

        # File Explorer Dock Widget
        self.file_explorer_widget = file_explorer(self.image_preview_label, self.tabs, self.app_data_path)
        self.file_explorer_dock_widget = DockWidget("File Explorer", self.file_explorer_widget, self)

        # Add the self.file_explorer_dock_widget to main window.
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_history_dock_widget)

        #connections
        self.file_explorer_widget.toggleImagePreviewWidget.connect(lambda image_path, list_widget_item_index, already_displayed, exists_in_file_explorer
                                                                   :self.handle_image_changed(image_path, list_widget_item_index ,already_displayed, exists_in_file_explorer))
        self.image_preview_label.toggleOffFileExplorerButton.connect(lambda list_widget_item_index: self.file_explorer_widget.radio_reset_for_custom_list_item(list_widget_item_index))

        self.interactive_map.screenshotTaken.connect(self.file_explorer_widget.add_new_file)
        # Dock configuration settings
        # self.setDockNestingEnabled(True)
        # self.resizeDocks([self.map_dock_widget, self.image_preview_dock_widget], [1, 1], Qt.Orientation.Vertical)

    def setup_menus(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("&View")

        self.add_view_menu_action(view_menu, "Interactive Map", self.map_dock_widget)
        self.add_view_menu_action(view_menu, "Image Preview", self.image_preview_dock_widget)
        self.add_view_menu_action(view_menu, "Map File Explorer", self.file_explorer_dock_widget)

    def add_view_menu_action(self, menu, title, dock_widget):
        action = QAction(title, self, checkable=True)
        action.setChecked(dock_widget.isVisible())
        action.triggered.connect(lambda checked: dock_widget.setVisible(checked))

        dock_widget.visibilityChanged.connect(action.setChecked)

        menu.addAction(action)

    def handle_image_changed(self, image_path:str, list_widget_item_index, already_displayed:bool, exists_in_file_explorer:bool):
        if exists_in_file_explorer:
            #if button has not been toggled and the no image is displayed in image_preview
            if not already_displayed and not self.image_preview_label.is_an_image:
                image = QPixmap(image_path)
                self.image_preview_label.setPixmap2(image)
                self.image_preview_label.currentImagePath = image_path
                self.image_preview_label.list_widget_item_index = list_widget_item_index
                self.image_preview_label.is_an_image = True
                self.tabs.currentWidget().setCurrentImagePath(image_path)

            #if button has already been toggled and an image is displayed
            elif already_displayed and self.image_preview_label.is_an_image:
                self.image_preview_label.clear()
                self.image_preview_label.setText(self.image_preview_label.placeholder)
                self.image_preview_label.list_widget_item_index = -1
                self.tabs.currentWidget().setCurrentImagePath("")
                self.image_preview_label.is_an_image = False
                self.image_preview_label.currentImagePath = ""

            #if button has not been toggled but there an image is displayed, untoggle that button and then toggle the new one.
            elif not already_displayed and self.image_preview_label.is_an_image:
                self.image_preview_label.toggleOffFileExplorerButton.emit(self.image_preview_label.list_widget_item_index)
                image = QPixmap(image_path)
                self.image_preview_label.setPixmap2(image)
                self.image_preview_label.is_an_image = True
                self.image_preview_label.list_widget_item_index =list_widget_item_index
                self.image_preview_label.currentImagePath = image_path
                self.tabs.currentWidget().setCurrentImagePath(image_path)




def main():
    geoint_app = QApplication(sys.argv)
    geoint_app.setApplicationName("GEOINT")
    geoint_app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if platform.system() == "Windows":
        if int(platform.release()) >= 8:
            print(platform.release())
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
    window = MainWindow()
    window.show()
    sys.exit(geoint_app.exec())


if __name__ == "__main__":
    main()
