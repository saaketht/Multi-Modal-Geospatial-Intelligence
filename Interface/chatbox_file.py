from component_file import *
from pyqtconfig import ConfigManager
from PyQt6.QtCore import QFile, QDataStream, QIODevice, Qt, QStandardPaths
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QInputDialog,
    QMessageBox,
    QListWidgetItem,
    QListWidget,
    QListView,
    QLayout,
    QAbstractScrollArea
)
import os
import sys
import shutil
from datetime import time

import json
from component_file import CustomInputDialog
from PyQt6.QtCore import QThreadPool, QObject
from PyQt6.QtGui import QPixmap
from model_runnable import ModelRunnable


class HelpWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.list_widget_item = None

        self.current_image_name = ""
        self.current_image_path = ""
        self.current_image_path_in_chat_folder = ""

        title_label = QLabel("\nGetting Started with GEOINT")
        title_label.setStyleSheet("font-weight: bold; font-size: 30px; color: #FFFFFF;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label)

        version_label = QLabel("Version: 1.0.0\nDeveloped by: L03 GEOINT TEAM\n")
        version_label.setStyleSheet("color: #FFFFFF;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(version_label)

        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget_layout = QVBoxLayout(scroll_widget)
        scroll_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget_layout.setSpacing(20)
        scroll_area.setWidget(scroll_widget)

        instructions = [
            ("feather/plus.svg", "In the Chat Box Window click the 'Plus' button to create a new converstion with Llava. A pop-up window will appear. Enter a name for the conversation and click 'Apply' to create the converation."),
            ("feather/folder.svg", "In the File Explorer Window, click the 'Folder' button to open your file system to upload  images to the File Explorer. A user can also upload an image by entering the file path in the text box located to the right of the 'Folder' button."
                                   " To add the image to the File Explorer, click the 'Plus' button, located to the right of the text box."),
            ("feather/eye.svg", "In the File Explorer Window, the 'Eye' button can be used to preview images"),
            ("feather/image.svg", "In the File Explorer, the 'Image' button can be used to delete images."),
            ("feather/globe.svg", "In the File Explorer, the 'Globe' button can be used to add an image to the conversation to be queried."),
            ("feather/map.svg", "In the File Explorer, the 'Map' button can be used to add an image to graph a tiff file to the LocalTileServer Map in the Interactive Map Window.\n"
                                "It is important to note that only properly georeferenced tiff files (Also known as GeoTiff files) can be graphed. If an uploaded tiff file is georeferenced, its label is highliged green, otherwise its label is red and its 'Map' button is disabled"),
            ("feather/arrow-up.svg", "After entering A message in the texbox in the Chat Box Window, a user can send his/her message to Llava by clicking on the  'Arrow-Up' button."),
            ("feather/message-circle.svg", "In the Chat History Window, the 'Message' button can be used used to open a previous conversation."),
            ("feather/trash-2.svg", "In the Chat History Window, the 'Trash-Can' button can be used to delete a previous conversation."),
        ]

        for icon_file_path, text in instructions:
            temp = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(15, 0, 0, 0)
            row_layout.setSpacing(20)

            icon_svg = QSvgWidget()
            icon_svg.load(icon_file_path)
            icon_svg.setFixedSize(22,22)
            row_layout.addWidget(icon_svg)

            text_label = QLabel(text)
            text_label.setFont(QFont('Arial', 14, QFont.Weight.Light.Bold))
            text_label.setStyleSheet("color: #FFFFFF;")
            text_label.setWordWrap(True)
            row_layout.addWidget(text_label, stretch=1)

            temp.setLayout(row_layout)
            scroll_widget_layout.addWidget(temp)
            # layout.addLayout(row_layout)

        # scroll_widget.setLayout(scroll_widget_layout)

        # layout.addStretch()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def setCurrentImagePath(self, path):
        # left blank to avoid image path error
        self.current_image_path = path


class UserMessage(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setMinimumWidth(1)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group1.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.username_label = QLabel("User", self)
        self.username_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        self.message_content.setContentsMargins(0,0,0,0)
        # self.message_content.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Fixed)

        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label)
        self.top_layout.addSpacing(15)

        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch()

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
        self.setMinimumWidth(1)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group2.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.username_label = QLabel("GEOINT", self)
        self.username_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        # self.message_content.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Fixed)
        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label)
        self.top_layout.addSpacing(15)

        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_layout_spacer = QSpacerItem(55, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.bottom_layout.addItem(self.bottom_layout_spacer)
        self.bottom_layout.addWidget(self.message_content, Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        self.setLayout(self.layout)


class Chat(QWidget):
    def __init__(self, title, chat_folder_path, list_widget_item, parent=None):
        super().__init__(parent=parent)
        self.index = 0
        self.title = title
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)
        self.setFont(self.font1)

        #Attributes
        self.list_widget_item = list_widget_item
        self.chat_folder_path = chat_folder_path

        self.current_image_name = ""
        self.current_image_path = ""
        self.current_image_path_in_chat_folder = ""
        self.app_data_path = os.path.dirname(self.chat_folder_path)
        self.uploads_folder = os.path.join(self.app_data_path,"uploads")

        self.json_file_name = "data.json"
        self.json_file_path = os.path.join(self.chat_folder_path , self.json_file_name)

        self.data_dict = {}
        self.messages = []

        #load history/json data if data exists

        #Widget UI setup
        self.tab_layout = QVBoxLayout()
        self.setContentsMargins(20, 20, 20, 20)
        self.tab_layout.setSpacing(20)

        self.chat_scroll_area = QScrollArea()
        # self.chat_list = QListWidget()
        # self.chat_scroll_area.setStyleSheet
        # self.chat_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        # self.chat_list.setUniformItemSizes(False)
        # self.chat_list.setResizeMode(QListView.ResizeMode.Adjust)
        # self.chat_list.setSizeAdjustPolicy(QListView.SizeAdjustPolicy.AdjustToContents)
        # self.chat_list.setSpacing(15)
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
        self.chat_scroll_layout.setSpacing(20)
        self.chat_scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
        self.send_button.setToolTip("Send")

        # self.chat_input_layout.addWidget(self.attach_icon_button)
        self.svgTest = QSvgWidget()
        self.svgTest.setFixedSize(34, 34)
        self.svgTest.load("loadingSvgs/LoadingPhase1.svg")

        test = self.svgTest.sizePolicy()
        test.setRetainSizeWhenHidden(True)
        self.svgTest.setSizePolicy(test)


        self.chat_input_layout.addWidget(self.svgTest)
        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.send_button)

        self.svgTest.setHidden(True)
        # self.tab_layout.addWidget(self.chat_list)
        self.tab_layout.addWidget(self.chat_scroll_area)
        self.tab_layout.addLayout(self.chat_input_layout)
        self.setLayout(self.tab_layout)

        self.load_chat_history()

        # tab_title = f"Tab {chat_widget.count() + 1}"
        # chat_widget.addTab(tab, QIcon('icons/worldIcon.png'), tab_title)

        self.vscrollbar = self.chat_scroll_area.verticalScrollBar()
        self.vscrollbar.rangeChanged.connect(lambda min, max: self.scrollToBottom(min,max))

    def isStreamLoadSvg(self, isStream:bool):
        if isStream:
            self.svgTest.load("loadingSvgs/LoadingPhase2.svg")
        else:
            self.svgTest.load("loadingSvgs/LoadingPhase3.svg")


    def scrollToBottom(self, min, max):
        self.vscrollbar.setValue(max)


    def setCurrentImagePath(self, image_path):
        self.current_image_path = image_path
        if image_path!= "" and self.chat_folder_path != "":
            shutil.copy(image_path, self.chat_folder_path)
            self.current_image_name = os.path.basename(image_path)
            self.current_image_path_in_chat_folder = os.path.join(self.chat_folder_path,self.current_image_name)
        self.current_image_name = os.path.basename(self.current_image_path)
        try:
            with open (self.json_file_path, "w") as file:
                self.data_dict.update({"image_url":self.current_image_path})
                json.dump(self.data_dict, file)

        except FileNotFoundError:
            pass


    def send_message(self):
        if (self.current_image_path == ""):
            QMessageBox.critical(None, "Error", "Image not found")
        else:
            message = self.chat_input.text()
            if message:
                user_message_widget = UserMessage(message)
                self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                # list_widget_item = QListWidgetItem(self.chat_list)
                # list_widget_item.setSizeHint(user_message_widget.sizeHint())
                # self.chat_list.addItem(list_widget_item)
                # self.chat_list.setItemWidget(list_widget_item, user_message_widget)
                #
                # self.chat_list.scrollToBottom()


                # self.chat_scroll_layout.insertWidget(self.index, user_message_widget, 0,Qt.AlignmentFlag.AlignLeft.AlignTop)
                self.index += 1

                # TODO: add the dictionary append area
                self.messages.append(f"User: {message}")
                print(self.messages)
                self.save_message(message, sender="User")
                self.chat_input.clear()

                # self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
                # self.update()
                chat_model_message_widget = ModelMessage('')

                # list_widget_item = QListWidgetItem(self.chat_list)
                # list_widget_item.setSizeHint(chat_model_message_widget.sizeHint())
                # self.chat_list.addItem(list_widget_item)
                # self.chat_list.setItemWidget(list_widget_item, chat_model_message_widget)

                self.send_button.setEnabled(False)
                self.svgTest.setHidden(False)
                model_runnable = ModelRunnable(message, self.current_image_path, self.messages,self.chat_scroll_layout,chat_model_message_widget)
                model_runnable.signals.response_received.connect(self.handle_model_response)
                model_runnable.signals.isStream.connect(lambda isStream: self.isStreamLoadSvg(isStream))
                QThreadPool.globalInstance().start(model_runnable)

                self.chat_input.enter_pressed.disconnect()

                # self.thread = QThread()
                # # Step 3: Create a worker object
                # self.worker = Worker(message, self.current_image_path, self.messages,chat_model_message_widget)
                # # Step 4: Move worker to the thread
                # self.worker.moveToThread(self.thread)
                # # Step 5: Connect signals and slots
                # self.thread.started.connect(self.worker.run)
                # self.worker.finished.connect(self.thread.quit)
                # self.worker.finished.connect(self.worker.deleteLater)
                #
                # self.thread.finished.connect(self.thread.deleteLater)
                # # self.worker.progress.connect(self.reportProgress)
                # # Step 6: Start the thread
                # self.thread.start()




                """
                model_output = send_and_receive(message, self.current_image_path, self.messages)
                print(model_output)
                model_message_text = ""
                for item in model_output:
                    model_message_text += item
    
    
                model_message_widget = ModelMessage(model_message_text)
                self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
                self.index += 1
                self.messages.append(f"GEOINT: {model_message_text}")
                self.save_message(model_message_text, sender="GEOINT")
                # self.chat_input.clear()
                self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
                self.update()
                """

    def save_message(self, message, sender="User"):
        try:
            with open(self.json_file_path, "w") as file:
                self.data_dict.update({"history":self.messages})
                json.dump(self.data_dict, file)

        except FileNotFoundError:
            pass

    def load_chat_history(self):
        if os.path.exists(self.json_file_path) and self.chat_folder_path!="":
            try:
                with open(self.json_file_path, "r") as file:
                    self.data_dict = json.load(file)
                    self.messages = self.data_dict["history"]
                    for message_text in self.messages:
                        if message_text.startswith("User:"):
                            user_message_text = message_text[len("User:"):].strip()
                            user_message_widget = UserMessage(user_message_text)
                            self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                            # list_widget_item = QListWidgetItem(self.chat_list)
                            # list_widget_item.setSizeHint(user_message_widget.sizeHint())
                            # self.chat_list.addItem(list_widget_item)
                            # self.chat_list.setItemWidget(list_widget_item, user_message_widget)
                            #
                            # self.chat_list.scrollToBottom()


                            self.index += 1
                        # elif message_text.startswith("GEOINT:"):
                        else:
                            # model_message_text = message_text[len("GEOINT:"):].strip()
                            model_message_text = message_text
                            model_message_widget = ModelMessage(model_message_text)
                            self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                            # list_widget_item = QListWidgetItem(self.chat_list)
                            # list_widget_item.setSizeHint(model_message_widget.sizeHint())
                            # self.chat_list.addItem(list_widget_item)
                            # self.chat_list.setItemWidget(list_widget_item, model_message_widget)
                            #
                            # self.chat_list.scrollToBottom()

                            self.index += 1
                    self.current_image_path = self.data_dict["image_url"]
                    self.current_image_name = os.path.basename(self.current_image_path)
                    self.current_image_path_in_chat_folder = os.path.join(self.chat_folder_path,self.current_image_name)


                    # self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
            except FileNotFoundError:
                pass

        elif self.chat_folder_path!="":
            try:
                with open(self.json_file_path, "x") as file:
                    self.data_dict = {
                        "chat_id":self.title,
                        "image_url": "",
                        "prompt": "",
                        "history": self.messages,
                        "model_params": {
                            "top_p": 1,
                            "max_tokens": 1024,
                            "temperature": 0.2
                        }
                    }
                    json.dump(self.data_dict, file)

            except FileNotFoundError:
                pass


            # try:
            #     with open("chat_history.json", "r") as file:
            #         self.history_dict = json.load(file)
            #         for message_text in self.history_dict:
            #             if message_text.startswith("User:"):
            #                 user_message_text = message_text[len("User:"):].strip()
            #                 user_message_widget = UserMessage(user_message_text)
            #                 self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
            #                 self.index += 1
            #             elif message_text.startswith("GEOINT:"):
            #                 model_message_text = message_text[len("GEOINT:"):].strip()
            #                 model_message_widget = ModelMessage(model_message_text)
            #                 self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
            #                 self.index += 1
            #         self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
            # except FileNotFoundError:
            #     pass

    def handle_model_response(self, model_message_text):
        self.svgTest.setHidden(True)
        self.svgTest.load("loadingSvgs/LoadingPhase1.svg")
        self.chat_input.enter_pressed.connect(self.send_message)
        self.send_button.setEnabled(True)
        # if model_message_text.startswith("GEOINT:"):
        #     model_message_text = model_message_text[len("GEOINT:"):].strip()

        # chat_model_message_widget = ModelMessage(model_message_text)
        # # self.chat_scroll_layout.addWidget(chat_model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)
        #
        # list_widget_item = QListWidgetItem(self.chat_list)
        # list_widget_item.setSizeHint(chat_model_message_widget.sizeHint())
        # self.chat_list.addItem(list_widget_item)
        # self.chat_list.setItemWidget(list_widget_item, chat_model_message_widget)

        # self.chat_list.scrollToBottom()

        self.index += 1
        # self.messages.append(f"GEOINT: {model_message_text}")
        self.messages.append(model_message_text)
        self.save_message(model_message_text, sender="GEOINT")
        # self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())
        self.update()


class ChatTabWidget(TabWidget):
    changeCloseAttribute = pyqtSignal(str)
    def __init__(self, app_data_path, chat_history_widget, parent=None):
        super().__init__(parent=parent)
        self.help_widget = HelpWidget(self)
        self.addTab2(widget=self.help_widget, title="Help")
        # self.addButton.clicked.connect(lambda: self.addTab2(widget=chat()))
        # self.app_data_path = app_data_path_type
        self.app_data_path = app_data_path
        self.chat_history_path = os.path.join(app_data_path,"chat_history")
        self.addButton.clicked.connect(lambda: self.add_new_chat())
        self.chat_history_widget = chat_history_widget
        self.tabCloseRequested.connect(self.removeTab3)

        self.chat_history_widget.loadExistingChat.connect(
            lambda tab_name, chat_folder_path, list_widget_item: self.add_existing_chat(tab_name,chat_folder_path,list_widget_item))

    def removeTab3(self,index):
        temp_widget = self.widget(index)
        list_widget_item = temp_widget.list_widget_item
        chat_list_item = self.chat_history_widget.itemWidget(list_widget_item)
        chat_list_item.is_open = False
        self.removeTab2(index)

    # this will be connected to the  add button.
    def add_new_chat(self):
        """adds new QTreeWidgetItem when 'addItemSignal' is emitted from ImportDataDialog"""
        input_dialog = CustomInputDialog(self)
        ok = input_dialog.exec()
        tab_name = input_dialog.textValue()

        if ok and tab_name:
            chat_folder_path, list_widget_item = self.chat_history_widget.create_item_from_new_chat(tab_name)
            self.tempWidget = Chat(tab_name, chat_folder_path,list_widget_item)
            self.addTab2(widget=self.tempWidget, title=tab_name)

        self.setCurrentIndex(self.count()-1)

    def add_existing_chat(self, tab_name, chat_folder_path, list_widget_item):
        chat_list_item = self.chat_history_widget.itemWidget(list_widget_item)
        if not chat_list_item.is_open:
            chat_list_item.is_open =True
            self.tempWidget = Chat(tab_name, chat_folder_path, list_widget_item)
            self.addTab2(widget=self.tempWidget, title=tab_name)
            self.setCurrentIndex(self.count()-1)

        elif chat_list_item.is_open:
            for index in range(self.count()):
                temp_chat = self.widget(index)
                temp_chat_list_widget_item = temp_chat.list_widget_item
                if temp_chat_list_widget_item == list_widget_item:
                    self.setCurrentIndex(index)





    # def action_saveworkspace_triggered(self, filename):
    #     """Saves current workspace to the selected file"""
    #     file = QFile(filename)
    #     file.open(QIODevice.WriteOnly)
    #     datastream = QDataStream(file)
    #
    #     # write the total number of items to be stored
    #     datastream.writeUInt32(root_item.childCount())
    #
    #     # write all data (= all elements of the TreeWidget) to the file
    #     for n in range(root_item.childCount()):
    #         item = root_item.child(n)
    #         item.write(datastream)
    #
    # def action_loadworkspace_triggered(self, filename, tree_widget):
    #     """Loads workspace from file"""
    #
    #     # open the file and create datastream
    #     file = QFile(filename)
    #     file.open(QIODevice.ReadOnly)
    #     datastream = QDataStream(file)
    #     root_item = tree_widget.invisibleRootItem()
    #
    #     # read all data from the file and create a TreeWidgetItem for each entry
    #     for n in range(datastream.readUInt32()):
    #         item = QTreeWidgetItem(root_item)
    #         item.read(datastream)
    #         data = item.data(1, Qt.ItemDataRole.UserRole)

class json_handler:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path



