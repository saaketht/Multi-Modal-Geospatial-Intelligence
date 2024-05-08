
# This file contains the main window of the applicaiton.

from PyQt6.QtCore import pyqtSlot, QVariant, QEasingCurve, QAbstractAnimation
from PyQt6.QtWidgets import QSplashScreen, QMainWindow, QApplication

import ctypes
import platform
import sys
from PyQt6.QtGui import QPixmap, QImageReader, QAction
from chat_history_dock import *
from chatbox_file import *
from file_explorer_dock import *
from image_preview_dock import *
from interactive_map_dock import *

# Instance of the main window, must inherit from QMainWindow
class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        # Call the parent constructor
        super().__init__()

        # Set the window title to MM-GEOINT
        self.setWindowTitle("MM-GEOINT")

        # Allows dockable windows to be overlapped and accessed using tabs, and allows dockable windows to be placed beside one another
        self.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks | QMainWindow.DockOption.AllowNestedDocks)

        # Chat Box Widgets
        # NOTE the Main window is the Chat Box.
        self.titlebar = None #The Main title bar
        self.chatbox_layout = None #This is the layout for the tabwidget
        self.tabs = None #The tabwidget for the

        # The Following are the Dockable Windows and their widgets

        # The Image Preview Dock and its Widget
        self.image_preview_dock_widget = None
        self.image_preview_label = None

        # The Chat History Dock and its Widget
        self.chat_history_list_widget = None
        self.chat_history_dock_widget = None

        # Map Dock and its Widget
        self.interactive_map = None
        self.map_dock_widget = None

        #The File Explorer Dock and Its Widgets
        self.file_explorer_widget = None
        self.file_explorer_dock_widget = None
        self.file_explorer_splitter = None

        self.explorer_image_prev = None
        self.explorer_image_prev_layout = None
        self.explorer_image_prev_label = None

        # Set the type of location/path where application data should be stored
        self.app_data_path_type = QStandardPaths.StandardLocation.AppDataLocation
        # Get the full path where application data should be written
        self.app_data_path = QStandardPaths.writableLocation(self.app_data_path_type)

        # CSS Style for the Main Window
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
                QToolTip
                {
                    background-color: #494949;
                    color:#FFFFFF;
                    border:none
                }
                ''')

        # Function call to instantiate all the widgets
        self.setup_main_window()

        # Function call to Connect all Docks to 'View' menu
        self.setup_menus()

        # Have main window open full screen
        self.showMaximized()

    # Instantiate-Widgets Method
    def setup_main_window(self):

        #Chat Box/Main Window title bar, note this is a sub-title bar for the main window
        # it does not replace the primary tile bar of the main window
        self.titlebar = TitleBar("Chat Box")
        self.titlebar.setFixedHeight(38)
        self.titlebar.titlebar_button1.clicked.connect(lambda: self.goToHelpTab()) #connect help button to help tab

        # layout for main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # First add the titlebar
        layout.addWidget(self.titlebar)

        # create QFrame for chatbox QVBoxLayout, The frame is just for styling purposes,
        # it will add a background for the tab widget
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

        #add the frame to the main window
        layout.addWidget(chatbox_frame)

        # Check and Print paths
        print("QStandardPaths::StandardLocation type: " + str(self.app_data_path_type))
        print("App Data Directory: " + str(self.app_data_path))

        # instantiate Chat History List Widget
        self.chat_history_list_widget = ChatHistoryListWidget(app_data_path=self.app_data_path)

        # instantiate ChatTabWidget (chat tabs) and pass Chat History List Widget
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
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.image_preview_dock_widget)

        # File Explorer Dock Widget
        # the file explorer has two widgets, the image preview widget and the file explorer widget,
        # the image prevew in this dock allows users to preview an image that has been uploaded to the file explorer
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

        self.file_explorer_splitter.setCollapsible(0,True)
        self.file_explorer_splitter.setCollapsible(1,False)

        self.file_explorer_splitter.moveSplitter(0,1)

        self.file_explorer_splitter.handle(1).setEnabled(False)

        self.file_explorer_dock_widget = DockWidget("File Explorer", self.file_explorer_splitter, self)

        # Animation for Image Preview drop down in the File Explorer
        self.m_animation = QVariantAnimation(
            self,
            startValue=0,
            endValue=50,
            valueChanged=self.onValueChanged,
            duration=700,
            easingCurve=QEasingCurve.Type.InOutCubic,
        )
        self.m_animation.finished.connect(lambda:self.finish_animation_funct())

        # Add the File Explorer to Main Window.
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_history_dock_widget)

        # The following connections, connect the dock widgets to the main window, so that docks can communicate to one another.
        self.file_explorer_widget.toggleImagePreviewWidget.connect(lambda image_path, list_widget_item_index, already_displayed, exists_in_file_explorer
                                                                   :self.handle_image_changed(image_path, list_widget_item_index ,already_displayed, exists_in_file_explorer))
        self.file_explorer_widget.toggleImagePreviewWidget2.connect(
            lambda image_path, list_widget_item_index, already_displayed, exists_in_file_explorer
            : self.handle_image_changed2(image_path, list_widget_item_index, already_displayed, exists_in_file_explorer))

        self.file_explorer_widget.toggleInteractiveMap.connect(
            lambda image_path, list_widget_item_index, already_displayed
            : self.handle_image_changed3(image_path, list_widget_item_index, already_displayed))

        self.image_preview_label.toggleOffFileExplorerButton.connect(lambda list_widget_item: self.file_explorer_widget.radio_reset_for_custom_list_item(list_widget_item))

        self.explorer_image_prev.toggleOffFileExplorerButton.connect(lambda list_widget_item: self.file_explorer_widget.radio_reset_for_custom_list_item2(list_widget_item))

        self.interactive_map.w3_widget.toggleOffFileExplorerButton.connect(lambda list_widget_item: self.file_explorer_widget.radio_reset_for_custom_list_item3(list_widget_item))

        self.interactive_map.screenshotTaken.connect(self.file_explorer_widget.add_new_file)

        self.tabs.currentChanged.connect(lambda: self.load_image_from_chat())

    #Method changes current tab to help tab.
    def goToHelpTab(self):
        for index in range(self.tabs.count()):
            temp_widget = self.tabs.widget(index)
            #the help tab is and will be the only tab without a list_widget
            if temp_widget.list_widget_item == None:
                self.tabs.setCurrentIndex(index)

    #This method completes the last steps  after the animation for the image preview in the file explorer window
    def finish_animation_funct(self):
        is_an_image = self.explorer_image_prev.is_an_image
        if is_an_image ==False:
            self.explorer_image_prev.lable.clear()
            self.explorer_image_prev.lable.setText(self.explorer_image_prev.lable.placeholder)
        elif is_an_image ==True:
            list_widget_item = self.explorer_image_prev.list_widget_item_index
            self.file_explorer_widget.file_list.scrollToItem(list_widget_item)

    #This method changes the animation direction depending on if the image is already displayed or not
    def toggle_image_preview_animation(self, is_up):

        if not is_up:
            self.m_animation.setStartValue(self.file_explorer_splitter.sizes()[0])
            self.m_animation.setEndValue(0)
        else:
            self.m_animation.setStartValue(0)
            self.m_animation.setEndValue(200)
        self.m_animation.start()

    #This method updates the splitter position
    def onValueChanged(self, value):
        self.file_explorer_splitter.moveSplitter(value,1)

    #This Method connects the menubar to dock widgets to reopen them when closed.
    def setup_menus(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("&View")

        self.add_view_menu_action(view_menu, "Interactive Map", self.map_dock_widget)
        self.add_view_menu_action(view_menu, "Current Image", self.image_preview_dock_widget)
        self.add_view_menu_action(view_menu, "Map File Explorer", self.file_explorer_dock_widget)
        self.add_view_menu_action(view_menu, "Chat History", self.chat_history_dock_widget)

    #This Method connects the menubar to dock widgets to reopen them when closed.
    def add_view_menu_action(self, menu, title, dock_widget):
        action = QAction(title, self, checkable=True)
        action.setChecked(dock_widget.isVisible())
        action.triggered.connect(lambda checked: dock_widget.setVisible(checked))

        dock_widget.visibilityChanged.connect(action.setChecked)

        menu.addAction(action)

    # This method gets the image associated with the current tab and displays it in the Current Image Window
    def load_image_from_chat(self):
        temp_chat = self.tabs.currentWidget()
        image_name = temp_chat.current_image_name
        image_path = temp_chat.current_image_path

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

    # This Method is the connection between the globe button in the file explorer window and the current image window,
    # when toggled the image will update the image and reset the button for the previous one, if one was already there.
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

                if(not (widget_of_item.is_preview_image_displayed or widget_of_item.is_tiff_displayed)):
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

    # This Method is the connection between the eye button in the file explorer widget and the image preview widget that are both in the file explorer window.
    # When toggled the image will update the image and reset the button for the previous one, if one was already there.
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

                if (not (widget_of_item.is_image_displayed or widget_of_item.is_tiff_displayed)):
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

    # This Method is the connection between the map button in the file explorer window and the interactive map window,
    # when toggled the image will update the image and reset the button for the previous one, if one was already there.
    def handle_image_changed3(self, image_path:str, list_widget_item, already_displayed:bool):
        #if button has not been toggled and the no image is displayed in image_preview
        if not already_displayed and not self.interactive_map.w3_widget.is_an_image:
            self.interactive_map.w3_widget.displayGeoTiff(image_path)
            self.interactive_map.w3_widget.currentImagePath = image_path
            self.interactive_map.w3_widget.list_widget_item_index = list_widget_item
            self.interactive_map.w3_widget.is_an_image = True
            self.interactive_map.tabs.setCurrentIndex(1)

            item = list_widget_item
            widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
            widget_of_item.remove_button.setEnabled(False)

        #if button has already been toggled and an image is displayed
        elif already_displayed and self.interactive_map.w3_widget.is_an_image:

            item = list_widget_item
            widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)

            if (not (widget_of_item.is_image_displayed or widget_of_item.is_preview_image_displayed)):
                widget_of_item.remove_button.setEnabled(True)

            self.interactive_map.w3_widget.resetMap()
            self.interactive_map.w3_widget.list_widget_item_index = -1
            self.interactive_map.w3_widget.is_an_image = False
            self.interactive_map.w3_widget.currentImagePath = ""

        #if button has not been toggled but there an image is displayed, untoggle that button and then toggle the new one.
        elif not already_displayed and self.interactive_map.w3_widget.is_an_image:
            self.interactive_map.w3_widget.toggleOffFileExplorerButton.emit(self.interactive_map.w3_widget.list_widget_item_index)
            print("works2")
            self.interactive_map.w3_widget.displayGeoTiff(image_path)
            self.interactive_map.w3_widget.is_an_image = True
            self.interactive_map.w3_widget.list_widget_item_index = list_widget_item
            self.interactive_map.tabs.setCurrentIndex(1)

            item = list_widget_item
            widget_of_item = self.file_explorer_widget.file_list.itemWidget(item)
            widget_of_item.remove_button.setEnabled(False)
            self.interactive_map.w3_widget.currentImagePath = image_path


# main function to run the application
def main():
    geoint_app = QApplication(sys.argv)

    #Allow somewhat large images to be loaded in applicaiton via QLabel
    QImageReader.setAllocationLimit(0)

    #Set the name for the applicaiton
    geoint_app.setApplicationName("GEOINT")

    #adjust the px for various devices
    geoint_app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if platform.system() == "Windows":
        if int(platform.release()) >= 8:
            print(platform.release())
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

    #splash screen for booting purposes.
    splashScreen = QPixmap('splashScreen/image 1@2x.png')
    splash = QSplashScreen(splashScreen)
    splash.show()
    geoint_app.processEvents()

    #show the main window.
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(geoint_app.exec())


if __name__ == "__main__":
    main()
