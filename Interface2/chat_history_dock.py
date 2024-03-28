import PyQt6.QtCore

from component_file import *
from chatbox_file import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QDockWidget, QTabWidget, QListWidget,
    QPlainTextEdit, QFileDialog, QMessageBox, QGridLayout, QToolBar, QListWidgetItem, QScrollArea, QSizePolicy
)
# from PyQt6.QtCore import PYQT_SIGNAL
import os, sys, shutil
from datetime import datetime
class ChatHistoryListWidget(QListWidget):
    def __init__(self, app_data_path_type, parent=None):
        super().__init__(parent=parent)

        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.tabs = None

        self.app_data_path_type = app_data_path_type
        temp = QStandardPaths.writableLocation(app_data_path_type)
        self.app_data_path = os.path.join(temp, "chat_history")
        if not os.path.exists(self.app_data_path):
            os.makedirs(self.app_data_path)

        self.setStyleSheet('''
        QListWidget 
        {
            border-top: 2px solid #494949;
            border-bottom: 2px solid #494949;
            border-right: 0;
            border-left: 0;
            border-radius:0;
        }
        QListWidget::item
        {
            background: #202020; 
            padding:0;
        }
        QListWidget::item:hover
        {
            background: #2d2d2d;
        }
        QListWidget::item:selected
        {
            background: #03B5A9;
        }

        QScrollBar:vertical 
        {
             border: 2px solid transparent;
             background: transparent;
             width: 15px;
             margin: 22px 0 22px 0;
             border-radius:6px;
         }
         QScrollBar::handle:vertical {
             background: #494949;
             border:2px solid transparent;
             min-height: 20px;
             border-radius:5px;
         }

         QScrollBar::add-line:vertical {
             border: 2px solid transparent;
             background: transparent;
             height: 20px;
             border-radius:5px;
             subcontrol-position: bottom;
             subcontrol-origin: margin;
         }

         QScrollBar::sub-line:vertical {
             border: 2px solid transparent;
             background: transparent;
             height: 20px;
             border-radius:5px;
             subcontrol-position: top;
             subcontrol-origin: margin;
         }
         QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
             border: 2px solid transparent;
             width: 3px;
             height: 3px;
             border-radius:3px;
             background: transparent;
         }

         QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
             background: none;
         }

         QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical 
         {
             background: none;
         }
        ''')

        # return docks("Map File Explorer", file_explorer_widget, self)
    def setChatTabWidget (self, tabs):
        self.tabs = tabs

    def add_new_item(self, title_prompt):
        now = datetime.now()
        chat_folder_name = now.strftime("%m-%d-%Y_%H-%M-%f")

        custom_list_item_widget = ChatListItem(title_prompt)

        list_widget_item = QListWidgetItem(self, type=QListWidgetItem.ItemType.UserType)
        list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

        self.addItem(list_widget_item)
        self.setItemWidget(list_widget_item, custom_list_item_widget)

        chat_folder_name_path = os.path.join(self.app_data_path, chat_folder_name)

        custom_list_item_widget.remove_button.clicked.connect(lambda: self.remove_item(list_widget_item,chat_folder_name_path))
        custom_list_item_widget.list_widget_item = list_widget_item


        if not os.path.exists(chat_folder_name_path):
            os.makedirs(chat_folder_name_path)
        else:
            chat_folder_name_path = chat_folder_name_path +"1"
            os.makedirs(chat_folder_name_path)

        return chat_folder_name_path

    def remove_item(self, list_widget_item, path):
        try:
            row = self.row(list_widget_item)
            self.takeItem(row)
        except Exception as e:
            print(f"Error removing item: {e}")
        shutil.rmtree(path)




class ChatListItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(5)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.open_button = icon_button(initial_icon="feather/eye.svg", icon_square_len=22, button_square_len=34)


        self.remove_button = icon_button(exit=True, icon_square_len=22, button_square_len=34)
        self.remove_button.setIcon(QIcon("feather/trash-2.svg"))

        self.label = Label(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Fixed)

        layout.addWidget(self.open_button)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.remove_button)
