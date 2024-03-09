import sys
import os
from component_file import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QDockWidget, QTabWidget, QListWidget,
    QPlainTextEdit, QFileDialog, QMessageBox, QGridLayout, QToolBar, QListWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt, QSize, QEvent, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QAction, QFontDatabase, QFont
import platform, ctypes

# class DockableWidget(QDockWidget):
#     def __init__(self, title, widget_to_dock, parent=None):
#         super().__init__(title, parent)
#         self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
#         self.setWidget(widget_to_dock)
#
#         self.setFloating(False)

class CustomListItem(QWidget):
    def __init__(self, text, image_preview_label, list_widget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,11,0,11)
        layout.setSpacing(5)

        self.remove_button = icon_button(initial_icon='feather/image.svg',icon_square_len=22, button_square_len=34)
        # self.remove_button = QPushButton()
        # self.remove_button.setIcon(QIcon('icons/imageIcon.png'))
        # self.remove_button.setFlat(True)
        self.label = Label(text)
        # self.eye_button = QPushButton()
        # self.eye_button.setIcon(QIcon('icons/eyeIcon.png'))
        self.eye_button = icon_button(initial_icon='feather/eye.svg', icon_square_len=22, button_square_len=34)
        # self.world_button = QPushButton()
        # self.world_button.setIcon(QIcon('icons/worldIcon.png'))
        self.world_button = icon_button(initial_icon='feather/globe.svg', icon_square_len=22, button_square_len=34)

        self.image_preview_label = image_preview_label
        self.list_widget = list_widget

        self.eye_button.clicked.connect(self.toggle_eye_icon)
        self.is_eye_icon = True

        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.installEventFilter(self) 

        self.world_button.clicked.connect(self.toggle_image_preview)
        self.is_image_displayed = False

        layout.addWidget(self.remove_button)
        layout.addWidget(self.label)
        # layout.addStretch()
        layout.addWidget(self.eye_button)
        layout.addWidget(self.world_button)

    def preview_image(self):
        file_path = self.label.text()
        if os.path.isfile(file_path):
            self.image_preview_label.setPixmap(QPixmap(file_path))
    
    def remove_item(self):
        try:
            row = self.list_widget.row(self.list_widget_item)
            self.list_widget.takeItem(row)
        except Exception as e:
            print(f"Error removing item: {e}") 
    
    def eventFilter(self, source, event):
        if source == self.remove_button:
            if event.type() == QEvent.Type.HoverEnter:
                self.remove_button.setIcon(QIcon('feather/trash-2.svg'))
            elif event.type() == QEvent.Type.HoverLeave:
                self.remove_button.setIcon(QIcon('feather/image.svg'))
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.remove_button.setStyleSheet("border:0px; background-color: red;")
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.remove_button.setStyleSheet("border:0px;")
        return super().eventFilter(source, event)
    
    def toggle_image_preview(self):
        file_path = self.label.text()
        if self.is_image_displayed:
            self.image_preview_label.clear()
            self.world_button.setIcon(QIcon('feather/globe.svg'))
            self.is_image_displayed = False
        elif os.path.isfile(file_path):
            self.image_preview_label.setPixmap(QPixmap(file_path))
            self.world_button.setIcon(QIcon('feather/x.svg'))
            self.is_image_displayed = True

    def toggle_eye_icon(self):
        if self.is_eye_icon:
            self.eye_button.setIcon(QIcon('feather/eye-off.svg'))
            self.is_eye_icon = False
        else:
            self.eye_button.setIcon(QIcon('feather/eye.svg'))
            self.is_eye_icon = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEOINT")
        self.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks | QMainWindow.DockOption.AllowNestedDocks)
    #     self.setStyleSheet("""
    #     QMainWindow {
    #         background-color: #494949;
    #     }
    #     QMainWindow::title {
    #         background-color: gray;
    #         color: #ffffff;
    #         }
    #     QLabel, QPushButton, QLineEdit, QListWidget, QTabWidget, QDockWidget {
    #         color: #ffffff;
    #     }
    #     QTabWidget {
    #         border: none;
    #     }
    #     QPushButton {
    #         padding: 5px;
    #         border-radius: 2px;
    #         background-color: #202020;
    #     }
    #     QPushButton:hover {
    #         background-color: #555555;
    #     }
    #     QLineEdit, QListWidget {
    #         background-color: #202020;
    #         border-radius: 2px;
    #         padding: 5px;
    #     }
    #     QDockWidget::title {
    #         text-align: center;
    #         background: #3e3e3e;
    #         padding: 3px;
    #     }
    #     QDockWidget {
    #         border: none;
    #         titlebar-close-icon: url(icons/xIcon.png);
    #         titlebar-normal-icon: url(icons/undockIcon.png);
    #     }
    #     QTabWidget::pane {
    #         border: none;
    #         background-color: #202020;
    #     }
    #     QTabWidget::tab-bar {
    #         alignment: center;
    #     }
    #     QTabBar::tab {
    #         background: gray;
    #         color: #ffffff;
    #         border: none;
    #         border-bottom-color: #202020;
    #         border-radius: 2px;
    #         min-width: 8ex;
    #         padding: 5px;
    #     }
    #     QTabBar::tab:selected, QTabBar::tab:hover {
    #         background: #202020;
    #         color: #ffffff;
    #     }
    #     QDockWidget::floatable {
    #         border: none;
    #     }
    #     QTabWidget::tab {
    #         border: none;
    #     }
    #     QPlainTextEdit {
    #         background-color: #202020;
    #         color: #ffffff;
    #         border: none;
    #         padding: 5px;
    #     }
    #     QToolBar {
    #         border: none;
    #         background-color: #202020;
    #     }
    #     QPushButton:pressed {
    #         background-color: #03B5A9;
    #     }
    #     QToolBar::handle {
    #         image: url(icons/handleIcon.png);
    #     }
    # """)
        self.setStyleSheet('''
                QMainWindow
                {
                    background-color: #494949;
                }
                QMainWindow::separator 
                {
                background-color: #494949;
                }
                ''')
        
        # font_path = "font/Roboto/Roboto-Bold.ttf"
        # font_id = QFontDatabase.addApplicationFont(font_path)
        # if font_id != -1:
        #     font_families = QFontDatabase.applicationFontFamilies(font_id)
        #     print("Loaded font families:", font_families)
        #     app_font = QFont(font_families[0], 10)
        #     QApplication.setFont(app_font)
        # else:
        #     print("Failed to load font from", font_path)

        self.setup_ui()
        #self.load_chat_history()
        self.setup_menus()
        self.showMaximized()
    
    def setup_ui(self):
        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)
        # main_layout = QHBoxLayout(self.central_widget)
        #
        # chat_container_widget = QWidget()
        # chat_container_layout = QVBoxLayout(chat_container_widget)
        #
        # title_layout = QHBoxLayout()
        # title_layout.addStretch(1)
        # title_label = QLabel("Chat Box")
        # title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # title_label.setStyleSheet("color: #ffffff; font-size: 13px; padding: 5px; background-color: #333333;")
        # title_layout.addWidget(title_label)
        #
        # title_layout.addStretch()
        #
        # help_button = QPushButton()
        # help_button.setIcon(QIcon('icons/helpIcon.png'))
        # sliders_button = QPushButton()
        # sliders_button.setIcon(QIcon('icons/slidersIcon.png'))
        # settings_button = QPushButton()
        # settings_button.setIcon(QIcon('icons/settingsIcon.png'))
        #
        # title_layout.addWidget(help_button)
        # title_layout.addWidget(sliders_button)
        # title_layout.addWidget(settings_button)
        #
        # chat_container_layout.addLayout(title_layout)
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
        self.tabs = TabWidget(parent=None)
        self.chatbox_layout.addWidget(self.tabs)
        #layout.addWidget(chatbox_frame)


        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        # chat_widget = QTabWidget()
        # self.add_tab(chat_widget)
        # add_tab_button = QPushButton("+")
        # add_tab_button.clicked.connect(lambda: self.add_tab(chat_widget))
        # chat_widget.setCornerWidget(add_tab_button, Qt.Corner.TopRightCorner)
        # chat_container_layout.addWidget(chat_widget)
        #
        # main_layout.addWidget(chat_container_widget)

        # Interactive Map Dock Widget
        map_placeholder = QLabel("Interactive Map Placeholder")
        map_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #map_placeholder.setStyleSheet("border: none; background-color: #202020;")
        self.map_dock_widget = docks("Interactive Map", map_placeholder, self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)

        # Image Preview Dock Widget
        self.image_preview_label = QLabel("Image Preview/Selection")
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setScaledContents(True)
        self.image_preview_label.setStyleSheet("background-color: #202020;")
        self.image_preview_dock_widget = docks("Image Preview", self.image_preview_label, self)
        #self.splitDockWidget(self.map_dock_widget, self.image_preview_dock_widget, Qt.Orientation.Vertical)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.map_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.image_preview_dock_widget)

        # File Explorer Dock Widget
        self.file_explorer_dock_widget = self.createFileExplorerWidget()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer_dock_widget)

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

    #Please integrate this into a widget using INHERITANCE
    def createFileExplorerWidget(self):
        self.file_list = QListWidget()
        self.file_path_line_edit = LineEdit()
        
        file_explorer_layout = QHBoxLayout()
        file_explorer_layout.setContentsMargins(0,0,0,0)
        file_explorer_layout.setSpacing(5)
        self.file_list.setStyleSheet('''
        QListWidget 
        {
            border-top: 2px solid #494949;
            border-bottom: 2px solid #494949;
            border-right: 0;
            border-left: 0;
            border-radius:0;
        }
        ''')
        
        # open_folder_action = QAction(QIcon('icons/folderIcon.png'), 'Open Folder', self)
        # open_folder_action.triggered.connect(self.open_file_dialog)
        #
        # add_file_action = QAction(QIcon('icons/plusIcon.png'), 'Add File', self)
        # add_file_action.triggered.connect(self.add_file_to_list)
        
        open_folder_button = icon_button(initial_icon='feather/folder.svg',icon_square_len=22, button_square_len=34)
        open_folder_button.clicked.connect(self.open_file_dialog)
        
        add_file_button = icon_button(initial_icon='feather/plus.svg',icon_square_len=22, button_square_len=34)
        add_file_button.clicked.connect(self.add_file_to_list)

        file_explorer_layout.addWidget(open_folder_button)
        file_explorer_layout.addWidget(self.file_path_line_edit)
        file_explorer_layout.addWidget(add_file_button)
        
        file_explorer_vertical_layout = QVBoxLayout()
        file_explorer_vertical_layout.addLayout(file_explorer_layout)
        file_explorer_vertical_layout.addWidget(self.file_list)
        
        file_explorer_widget = QWidget()
        file_explorer_widget.setLayout(file_explorer_vertical_layout)

        return docks("Map File Explorer", file_explorer_widget, self)

    # def add_tab(self, chat_widget):
    #     tab = QWidget()
    #     tab_layout = QVBoxLayout(tab)
    #
    #     self.chat_box = QPlainTextEdit()
    #     self.chat_box.setReadOnly(True)
    #     chat_scroll_area = QScrollArea()
    #     chat_scroll_area.setWidgetResizable(True)
    #     chat_scroll_widget = QWidget()
    #     chat_scroll_layout = QVBoxLayout(chat_scroll_widget)
    #     chat_scroll_layout.addWidget(self.chat_box)
    #     chat_scroll_area.setWidget(chat_scroll_widget)
    #
    #     chat_input_layout = QHBoxLayout()
    #
    #     attach_icon_button = QPushButton()
    #     attach_icon_button.setIcon(QIcon('icons/attachIcon.png'))
    #     attach_icon_button.setIconSize(QSize(24, 24))
    #     attach_icon_button.setFlat(True)
    #     attach_icon_button.setStyleSheet("QPushButton:pressed { background-color: #03B5A9; }")
    #
    #     self.chat_input = QLineEdit()
    #     self.chat_input.setPlaceholderText("Type here!")
    #     send_button = QPushButton("Send")
    #     send_button.clicked.connect(self.send_message)
    #     self.chat_input.setStyleSheet("border: 1px solid #767676;")
    #     send_button.setIcon(QIcon('icons/activity.svg'))
    #     send_button.setIconSize(QSize(24, 24))
    #     send_button.setFlat(True)
    #     send_button.setStyleSheet("QPushButton:pressed { background-color: #03B5A9; }")
    #
    #     chat_input_layout.addWidget(attach_icon_button)
    #     chat_input_layout.addWidget(self.chat_input)
    #     chat_input_layout.addWidget(send_button)
    #
    #     tab_layout.addWidget(chat_scroll_area)
    #     tab_layout.addLayout(chat_input_layout)
    #
    #     tab_title = f"Tab {chat_widget.count() + 1}"
    #     chat_widget.addTab(tab, QIcon('icons/worldIcon.png'), tab_title)
    #
    # def send_message(self):
    #     message = self.chat_input.text()
    #     if message:
    #         self.chat_box.appendPlainText(message)
    #         self.save_message(message)
    #         self.chat_input.clear()
    #
    #     # TODO: Integrate with model
    #     # self.receive_message("Model response here...")
    #
    # # TODO: Method for recieving model response
    # # def receive_message(self, message):
    # #     self.chat_box.appendPlainText(message)
    # #     self.save_message(message)
    #
    # def save_message(self, message):
    #     with open("chat_history.txt", "a") as file:
    #         file.write(f"{message}\n")
    #
    # def load_chat_history(self):
    #     try:
    #         with open("chat_history.txt", "r") as file:
    #             for line in file:
    #                 self.chat_box.appendPlainText(line.strip())
    #     except FileNotFoundError:
    #         pass

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select TIFF file", "", "TIFF files (*.tiff *.tif)")
        if file_path:
            self.file_path_line_edit.setText(file_path)
    
    def add_file_to_list(self):
        file_path = self.file_path_line_edit.text()
        try:
            if file_path and os.path.isfile(file_path):
                custom_list_item_widget = CustomListItem(file_path, self.image_preview_label, self.file_list)
                list_widget_item = QListWidgetItem(self.file_list)
                list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())
                
                self.file_list.addItem(list_widget_item)
                self.file_list.setItemWidget(list_widget_item, custom_list_item_widget)

                custom_list_item_widget.list_widget_item = list_widget_item

                self.file_path_line_edit.clear()
            else:
                QMessageBox.information(self, "Error", "Invalid file path.")
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

# def main():
app = QApplication(sys.argv)
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

