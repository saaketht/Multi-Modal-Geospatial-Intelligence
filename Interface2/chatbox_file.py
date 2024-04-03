from component_file import *
from pyqtconfig import ConfigManager
from PyQt6.QtCore import QFile, QDataStream, QIODevice, Qt, QStandardPaths
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QInputDialog
)
import os
import sys
from datetime import time

import json
from component_file import CustomInputDialog
from PyQt6.QtCore import QThreadPool
from model_runnable import ModelRunnable
from send import send_and_receive


# class AddNewTabDialog(QDialog):
#     def __init__(self):
#         super().__init__()

class UserMessage(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group1.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.username_label = QLabel("User", self)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label)
        self.top_layout.addSpacing(15)

        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)
        # self.top_layout.addStretch()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_layout_spacer = QSpacerItem(55, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.bottom_layout.addItem(self.bottom_layout_spacer)
        self.bottom_layout.addWidget(self.message_content, Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)
        # self.layout.addWidget(self.message_content)

        self.setLayout(self.layout)


class ModelMessage(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group2.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.username_label = QLabel("GEOINT", self)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label)
        self.top_layout.addSpacing(15)

        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_layout_spacer = QSpacerItem(55, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.bottom_layout.addItem(self.bottom_layout_spacer)
        self.bottom_layout.addWidget(self.message_content, Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        self.setLayout(self.layout)


class Chat(QWidget):
    def __init__(self, chat_folder_path_name, parent=None):
        super().__init__(parent=parent)
        self.index = 0

        self.title_prompt = "Untitled"
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)
        self.setFont(self.font1)

        # model inputs
        self.current_image_path = ""
        self.history_dict = []

        self.tab_layout = QVBoxLayout()
        self.setContentsMargins(20, 20, 20, 20)
        self.tab_layout.setSpacing(20)

        # self.chat_box = PlainTextEdit()
        # self.chat_box.setReadOnly(True)
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setStyleSheet('''
                QScrollArea
                {
                    padding:0;
                    background: #202020;
                    border-top: 2px solid #494949;
                    border-bottom: 2px solid #494949;
                    border-radius:0;
                    margin:0;
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
                ''')
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_widget = QWidget()
        self.chat_scroll_layout = QVBoxLayout(self.chat_scroll_widget)
        self.chat_scroll_layout.setContentsMargins(0, 15, 0, 15)
        self.chat_scroll_layout.setSpacing(10)
        # self.chat_scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop.AlignLeft)
        self.chat_scroll_layout.addStretch()

        # self.chat_scroll_layout.addWidget(self.chat_box)
        self.chat_scroll_area.setWidget(self.chat_scroll_widget)

        self.chat_input_layout = QHBoxLayout()
        self.chat_input_layout.setAlignment(Qt.AlignmentFlag.AlignTop.AlignLeft)
        self.chat_input_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_input_layout.setSpacing(5)

        self.attach_icon_button = icon_button(initial_icon='feather/paperclip.svg', button_square_len=34,
                                              icon_square_len=22)

        self.chat_input = LineEdit()
        self.chat_input.enter_pressed.connect(self.send_message)
        self.chat_input.setPlaceholderText("Type here!")
        self.send_button = icon_button(initial_icon='feather/arrow-up.svg', icon_square_len=22, button_square_len=34)
        self.send_button.clicked.connect(self.send_message)

        # self.chat_input_layout.addWidget(self.attach_icon_button)
        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.send_button)

        self.tab_layout.addWidget(self.chat_scroll_area)
        self.tab_layout.addLayout(self.chat_input_layout)
        self.setLayout(self.tab_layout)
        #
        # tab_title = f"Tab {chat_widget.count() + 1}"
        # chat_widget.addTab(tab, QIcon('icons/worldIcon.png'), tab_title)

        self.load_chat_history()

        self.messages = []

    def setCurrentImagePath(self, image_path):
        self.current_image_path = image_path
        #TODO:"Copy image to the chat folder when a new image is being added"
        print(self.current_image_path)

    def send_message(self):
        message = self.chat_input.text()
        if message:
            user_message_widget = UserMessage(message)
            self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
            # self.chat_scroll_layout.insertWidget(self.index, user_message_widget, 0,Qt.AlignmentFlag.AlignLeft.AlignTop)
            self.index += 1

            # TODO: add the dictionary append area
            self.history_dict.append(f"User: {message}")
            self.save_message(message, sender="User")
            self.chat_input.clear()

            self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
            self.update()

            model_runnable = ModelRunnable(message, self.current_image_path, self.history_dict)
            model_runnable.signals.response_received.connect(self.handle_model_response)
            QThreadPool.globalInstance().start(model_runnable)

            """
            model_output = send_and_receive(message, self.current_image_path, self.history_dict)
            print(model_output)
            model_message_text = ""
            for item in model_output:
                model_message_text += item
            
            
            model_message_widget = ModelMessage(model_message_text)
            self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
            self.index += 1
            self.history_dict.append(f"GEOINT: {model_message_text}")
            self.save_message(model_message_text, sender="GEOINT")
            # self.chat_input.clear()
            self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
            self.update()
            """

    def receive_message(self, message):
        self.chat_box.appendPlainText(message)
        self.save_message(message)

    def save_message(self, message, sender="User"):
        with open("chat_history.json", "w") as file:
            json.dump(self.history_dict, file)

    def load_chat_history(self):
        try:
            with open("chat_history.json", "r") as file:
                self.history_dict = json.load(file)
                for message_text in self.history_dict:
                    if message_text.startswith("User:"):
                        user_message_text = message_text[len("User:"):].strip()
                        user_message_widget = UserMessage(user_message_text)
                        self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
                        self.index += 1
                    elif message_text.startswith("GEOINT:"):
                        model_message_text = message_text[len("GEOINT:"):].strip()
                        model_message_widget = ModelMessage(model_message_text)
                        self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
                        self.index += 1
                self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
        except FileNotFoundError:
            pass

    def handle_model_response(self, model_message_text):
        if model_message_text.startswith("GEOINT:"):
            model_message_text = model_message_text[len("GEOINT:"):].strip()

        chat_model_message_widget = ModelMessage(model_message_text)
        self.chat_scroll_layout.addWidget(chat_model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
        self.index += 1
        self.history_dict.append(f"GEOINT: {model_message_text}")
        self.save_message(model_message_text, sender="GEOINT")
        self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
        self.update()


class ChatTabWidget(TabWidget):
    def __init__(self, app_data_path, chat_history_widget, parent=None):
        super().__init__(parent=parent)
        self.addTab2(widget=Chat(""))
        # self.addButton.clicked.connect(lambda: self.addTab2(widget=chat()))
        # self.app_data_path = app_data_path_type
        self.addButton.clicked.connect(lambda: self.add_new_chat())
        self.chat_history_widget = chat_history_widget

    # this will be connected to the  add button.
    def add_new_chat(self):
        """adds new QTreeWidgetItem when 'addItemSignal' is emitted from ImportDataDialog"""
        input_dialog = CustomInputDialog(self)
        ok = input_dialog.exec()
        tab_name = input_dialog.textValue()

        if ok and tab_name:
            chat_folder_path_name = self.chat_history_widget.add_new_item(tab_name)
            self.tempWidget = Chat(chat_folder_path_name)
            self.addTab2(widget=self.tempWidget, title=tab_name)

    def action_saveworkspace_triggered(self, filename):
        """Saves current workspace to the selected file"""
        file = QFile(filename)
        file.open(QIODevice.WriteOnly)
        datastream = QDataStream(file)

        # write the total number of items to be stored
        datastream.writeUInt32(root_item.childCount())

        # write all data (= all elements of the TreeWidget) to the file
        for n in range(root_item.childCount()):
            item = root_item.child(n)
            item.write(datastream)

    def action_loadworkspace_triggered(self, filename, tree_widget):
        """Loads workspace from file"""

        # open the file and create datastream
        file = QFile(filename)
        file.open(QIODevice.ReadOnly)
        datastream = QDataStream(file)
        root_item = tree_widget.invisibleRootItem()

        # read all data from the file and create a TreeWidgetItem for each entry
        for n in range(datastream.readUInt32()):
            item = QTreeWidgetItem(root_item)
            item.read(datastream)
            data = item.data(1, Qt.ItemDataRole.UserRole)
