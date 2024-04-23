import ctypes
import platform
import shutil

from PyQt6.QtCore import pyqtSlot, QVariant,QEasingCurve, QAbstractAnimation

from chat_history_dock import *
from chatbox_file import *
from file_explorer_dock import *
from image_preview_dock import *
from interactive_map_dock import *
from PyQt6.QtWidgets import QSplashScreen


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
        self.file_explorer_splitter = None
        self.explorer_image_prev = None
        self.explorer_image_prev_layout = None
        self.explorer_image_prev_label = None




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

        # instantiate Chat History DockWidget to display Chat History List Widget
        self.chat_history_dock_widget = DockWidget("Chat History", self.chat_history_list_widget, self)

        # create central_widget
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        # Interactive Map Dock Widget
        self.interactive_map = interactive_map_widget(self.app_data_path)

        # map_placeholder.setStyleSheet("border: none; background-color: #202020;")
        self.map_dock_widget = DockWidget("Interactive Map", self.interactive_map, self)
        self.map_dock_widget.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)

        # Image Preview Dock Widget
        self.image_preview_label = image_preview_widget("Image Selection")
        self.image_preview_dock_widget = DockWidget("Current Image", self.image_preview_label, self)

        # The following 2 lines of code add these QDockWidgets to MainWindow
        # (the map_dock_widget and image_preview_dock_widget)
        # self.splitDockWidget(self.map_dock_widget, self.image_preview_dock_widget, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.image_preview_dock_widget)

        # File Explorer Dock Widget
        # self.file_explorer_splitter = Splitter()
        # self.file_explorer_splitter.setOrientation(Qt.Orientation.Vertical)

        self.explorer_image_prev = image_preview_widget("Image Preview")

        self.explorer_image_prev_frame = QFrame()
        self.explorer_image_prev_frame.setObjectName("explorerpreview")
        self.explorer_image_prev_frame.setStyleSheet('''
             QFrame
             {
                background: #202020;
                border: 2px solid #494949;
                border-radius:10px;
            }
            ''')

        self.explorer_image_prev_frame_l = QHBoxLayout(self.explorer_image_prev_frame)
        self.explorer_image_prev_frame_l.setContentsMargins(10,10,10,10)
        self.explorer_image_prev_frame_l.setSpacing(0)

        self.explorer_image_prev_frame_l.addWidget(self.explorer_image_prev)

        self.explorer_image_prev_frame.setLayout(self.explorer_image_prev_frame_l)


        self.file_explorer_widget = file_explorer(self.app_data_path)

        self.file_explorer_splitter = FileExplorerSplitter(self.explorer_image_prev_frame,self.file_explorer_widget)
        # self.file_explorer_splitter.setOrientation(Qt.Orientation.Vertical)

        # self.file_explorer_splitter.addWidget(self.explorer_image_prev_frame)
        # self.file_explorer_splitter.addWidget(self.file_explorer_widget)

        self.file_explorer_splitter.setCollapsible(0,True)
        self.file_explorer_splitter.setCollapsible(1,False)

        self.file_explorer_splitter.moveSplitter(0,1)

        self.file_explorer_splitter.handle(1).setEnabled(False)

        self.file_explorer_dock_widget = DockWidget("File Explorer", self.file_explorer_splitter, self)

        self.m_animation = QVariantAnimation(
            self,
            startValue=0,
            endValue=50,
            valueChanged=self.onValueChanged,
            duration=700,
            easingCurve=QEasingCurve.Type.InOutCubic,
        )
        self.m_animation.finished.connect(lambda:self.finish_animation_funct())


        # Add the self.file_explorer_dock_widget to main window.
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_history_dock_widget)

        #connections
        self.file_explorer_widget.toggleImagePreviewWidget.connect(lambda image_path, list_widget_item_index, already_displayed, exists_in_file_explorer
                                                                   :self.handle_image_changed(image_path, list_widget_item_index ,already_displayed, exists_in_file_explorer))
        self.file_explorer_widget.toggleImagePreviewWidget2.connect(
            lambda image_path, list_widget_item_index, already_displayed, exists_in_file_explorer
            : self.handle_image_changed2(image_path, list_widget_item_index, already_displayed, exists_in_file_explorer))

        self.image_preview_label.toggleOffFileExplorerButton.connect(lambda list_widget_item: self.file_explorer_widget.radio_reset_for_custom_list_item(list_widget_item))

        self.explorer_image_prev.toggleOffFileExplorerButton.connect(lambda list_widget_item: self.file_explorer_widget.radio_reset_for_custom_list_item2(list_widget_item))

        self.interactive_map.screenshotTaken.connect(self.file_explorer_widget.add_new_file)

        self.tabs.currentChanged.connect(lambda: self.load_image_from_chat())
        # Dock configuration settings
        # self.setDockNestingEnabled(True)
        # self.resizeDocks([self.map_dock_widget, self.image_preview_dock_widget], [1, 1], Qt.Orientation.Vertical)

    def toggle_image_preview_animation(self, is_up):

        if not is_up:
            self.m_animation.setStartValue(self.file_explorer_splitter.sizes()[0])
            self.m_animation.setEndValue(0)
        else:
            self.m_animation.setStartValue(0)
            self.m_animation.setEndValue(200)
        self.m_animation.start()
    def onValueChanged(self, value):
        self.file_explorer_splitter.moveSplitter(value,1)

    def setup_menus(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("&View")

        self.add_view_menu_action(view_menu, "Interactive Map", self.map_dock_widget)
        self.add_view_menu_action(view_menu, "Current Image", self.image_preview_dock_widget)
        self.add_view_menu_action(view_menu, "Map File Explorer", self.file_explorer_dock_widget)
        self.add_view_menu_action(view_menu, "Chat History", self.chat_history_dock_widget)

    def add_view_menu_action(self, menu, title, dock_widget):
        action = QAction(title, self, checkable=True)
        action.setChecked(dock_widget.isVisible())
        action.triggered.connect(lambda checked: dock_widget.setVisible(checked))

        dock_widget.visibilityChanged.connect(action.setChecked)

        menu.addAction(action)

    def load_image_from_chat(self):
        #TODO: AVOID ABOUT TAB!!!!
        temp_chat = self.tabs.currentWidget()
        image_name = temp_chat.current_image_name
        image_path = temp_chat.current_image_path
        # if not isinstance(temp_chat, AboutWidget):
        #     image_name = temp_chat.current_image_name
        #     image_path = temp_chat.current_image_path

        if image_path == self.image_preview_label.currentImagePath:
            test="DO NOTHING"

        elif os.path.isfile(image_path) and image_path != "":
            list_widget_item = self.file_explorer_widget.get_list_widget_item(image_path)
            custom_list_item_widget = self.file_explorer_widget.file_list.itemWidget(list_widget_item)

            self.file_explorer_widget.world_button_signal(custom_list_item_widget,list_widget_item)

        elif temp_chat.current_image_name != "" and not os.path.isfile(image_path):
            # image_path_in_chat_folder = os.path.join(temp_chat.chat_folder_path, image_name)
            image_path_in_chat_folder = temp_chat.current_image_path_in_chat_folder
            print("image_path_in_chat_folder  :",image_path_in_chat_folder)
            print("self.file_explorer_widget  :",self.file_explorer_widget)
            image_path_in_uploads_folder= shutil.copy(image_path_in_chat_folder,self.file_explorer_widget.uploads_folder)
            self.file_explorer_widget.add_new_file(image_path_in_uploads_folder)

            list_widget_item = self.file_explorer_widget.get_list_widget_item(image_path)
            custom_list_item_widget = self.file_explorer_widget.file_list.itemWidget(list_widget_item)

            self.file_explorer_widget.world_button_signal(custom_list_item_widget,list_widget_item)

        elif image_path == "" and self.image_preview_label.list_widget_item_index != -1:
            list_widget_item =  self.image_preview_label.list_widget_item_index
            custom_list_item_widget = self.file_explorer_widget.file_list.itemWidget(list_widget_item)
            self.file_explorer_widget.world_button_signal(custom_list_item_widget,list_widget_item)


    def handle_image_changed(self, image_path:str, list_widget_item, already_displayed:bool, exists_in_file_explorer:bool):
        #if the file exists in the uploads folder
        if exists_in_file_explorer:
            #if button has not been toggled and the no image is displayed in image_preview
            if not already_displayed and not self.image_preview_label.is_an_image:
                image = QPixmap(image_path)
                self.image_preview_label.setPixmap2(image)
                self.image_preview_label.currentImagePath = image_path
                self.image_preview_label.list_widget_item_index = list_widget_item
                self.image_preview_label.is_an_image = True

                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
                widget_of_item.remove_button.setEnabled(False)

                self.tabs.currentWidget().setCurrentImagePath(image_path)

            #if button has already been toggled and an image is displayed
            elif already_displayed and self.image_preview_label.is_an_image:
                self.image_preview_label.lable.clear()
                self.image_preview_label.lable.setText(self.image_preview_label.lable.placeholder)

                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)

                if(not widget_of_item.is_preview_image_displayed):
                    widget_of_item.remove_button.setEnabled(True)

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
                self.image_preview_label.list_widget_item_index =list_widget_item

                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
                widget_of_item.remove_button.setEnabled(False)

                self.image_preview_label.currentImagePath = image_path
                self.tabs.currentWidget().setCurrentImagePath(image_path)

    #this is for image preview within the file explorer
    def handle_image_changed2(self, image_path:str, list_widget_item, already_displayed:bool, exists_in_file_explorer:bool):
        #if the file exists in the uploads folder
        if exists_in_file_explorer:
            #if button has not been toggled and the no image is displayed in image_preview
            if not already_displayed and not self.explorer_image_prev.is_an_image:
                image = QPixmap(image_path)
                self.explorer_image_prev.setPixmap2(image)
                self.explorer_image_prev.currentImagePath = image_path
                self.explorer_image_prev.list_widget_item_index = list_widget_item
                self.explorer_image_prev.is_an_image = True
                self.file_explorer_splitter.handle(1).setEnabled(True)
                self.toggle_image_preview_animation(True)

                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
                widget_of_item.remove_button.setEnabled(False)

            #if button has already been toggled and an image is displayed
            elif already_displayed and self.explorer_image_prev.is_an_image:


                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)

                if (not widget_of_item.is_image_displayed):
                    widget_of_item.remove_button.setEnabled(True)

                self.file_explorer_splitter.handle(1).setEnabled(False)

                self.toggle_image_preview_animation(False)

                self.explorer_image_prev.list_widget_item_index = -1
                self.explorer_image_prev.is_an_image = False
                self.explorer_image_prev.currentImagePath = ""


            #if button has not been toggled but there an image is displayed, untoggle that button and then toggle the new one.
            elif not already_displayed and self.explorer_image_prev.is_an_image:
                self.explorer_image_prev.toggleOffFileExplorerButton.emit(self.explorer_image_prev.list_widget_item_index)
                image = QPixmap(image_path)
                self.explorer_image_prev.setPixmap2(image)
                self.explorer_image_prev.is_an_image = True
                self.explorer_image_prev.list_widget_item_index =list_widget_item

                item = list_widget_item
                widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
                widget_of_item.remove_button.setEnabled(False)

                self.explorer_image_prev.currentImagePath = image_path
    def finish_animation_funct(self):
        is_an_image = self.explorer_image_prev.is_an_image
        if is_an_image ==False:
            self.explorer_image_prev.lable.clear()
            self.explorer_image_prev.lable.setText(self.explorer_image_prev.lable.placeholder)
        elif is_an_image ==True:
            list_widget_item = self.explorer_image_prev.list_widget_item_index
            self.file_explorer_widget.file_list.scrollToItem(list_widget_item)

def main():
    geoint_app = QApplication(sys.argv)
    geoint_app.setApplicationName("GEOINT")
    geoint_app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    splashScreen = QPixmap('image 1@2x.png')
    splash = QSplashScreen(splashScreen)
    splash.show()
    geoint_app.processEvents()

    if platform.system() == "Windows":
        if int(platform.release()) >= 8:
            print(platform.release())
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(geoint_app.exec())


if __name__ == "__main__":
    main()
