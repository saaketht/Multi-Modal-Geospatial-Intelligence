
# This file contains widgets related to the ChatBox, this is the center of the application.

import os
import shutil
from component_file import *
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QMessageBox
)
import json
from component_file import CustomInputDialog
from PyQt6.QtCore import QThreadPool
from model_runnable import ModelRunnable

# This is a custom widget that is displayed in the first tab of the TabWidget,
# The purpose of this widget is to display a list of instructions of how to use/navigate the application
class HelpWidget(QWidget):
    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Layout of widget
        layout = QVBoxLayout(self)

        # The following attributes are used to set the image when the globe button in the file explorer is pressed
        # The list_widget_item here is always set to none, so its used, TEMPORARILY, to differentiate between the
        # the help widget and the chat widget
        self.list_widget_item = None
        self.current_image_name = ""
        self.current_image_path = ""
        self.current_image_path_in_chat_folder = ""

        # The Following label is the Getting Started Title
        title_label = QLabel("\nGetting Started with GEOINT")
        title_label.setStyleSheet("font-weight: bold; font-size: 30px; color: #FFFFFF;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label)

        # The Following label is the Version label
        version_label = QLabel("Version: 1.0.0\nDeveloped by: L03 GEOINT TEAM\n")
        version_label.setStyleSheet("color: #FFFFFF;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(version_label)

        # The list of instructions will be stored in a ScrollArea widget
        scroll_area = ScrollArea()

        # Let scroll area resize the instructions if needed
        scroll_area.setWidgetResizable(True)

        # Create a widget to store the instructions
        scroll_widget = QWidget()

        # Layout for the widget that will store the instructions
        scroll_widget_layout = QVBoxLayout(scroll_widget)

        # let the widgets be added from the top down.
        scroll_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set layout spacing and set the widget to the scroll area
        scroll_widget_layout.setSpacing(20)
        scroll_area.setWidget(scroll_widget)

        # The instructions, consists of an icon and a set of text
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

        # For loop is used to add the instructions to the scroll area.
        for icon_file_path, text in instructions:
            # Temporary widget for each instruction
            temp = QWidget()

            # Layout for the temp widget, it will hold the icon and the label
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(15, 0, 0, 0)
            row_layout.setSpacing(20)

            # Prepare the Icon
            icon_svg = QSvgWidget()
            icon_svg.load(icon_file_path)
            icon_svg.setFixedSize(22,22)
            # Add the icon to the layout
            row_layout.addWidget(icon_svg)

            # Prepare the label
            text_label = QLabel(text)
            text_label.setFont(QFont('Arial', 14, QFont.Weight.Light.Bold))
            text_label.setStyleSheet("color: #FFFFFF;")
            text_label.setWordWrap(True)
            # Add the label to the layout
            row_layout.addWidget(text_label, stretch=1)

            # Set the layout for the tem widget
            temp.setLayout(row_layout)

            # Add temp widget to the scroll area widget
            scroll_widget_layout.addWidget(temp)

        # Add the scroll area to the general layout of the HelpWidget, and set the layout to the HelpWidget
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    # Method needed to se the image path.
    def setCurrentImagePath(self, path):
        # left blank to avoid image path error
        self.current_image_path = path

# This is the widget that encapsulates the user's message
class UserMessage(QWidget):
    # Constructor, message var is used to set the label of the widget
    def __init__(self, message, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Set the widget's contents margins to 0
        self.setContentsMargins(0, 0, 0, 0)

        # Layout for the widget, set spacing and contents to 0
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set the min width to 1
        self.setMinimumWidth(1)

        # Set widget's size polity to preferred
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # This is the user's profile picture, and its specifications
        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group1.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # This is the user's label, and its specifications
        self.username_label = QLabel("User", self)
        self.username_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        # This is the message label, and its specifications
        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        self.message_content.setContentsMargins(0,0,0,0)
        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        # This widget consists of two horizontal layouts nested within the vertical layout, self.layout
        # The first horizontal layout, self.top_layout, will have the user's label and the user's profile picture
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label)  # Add the profile picture to layout
        self.top_layout.addSpacing(15)

        # Add the user's label to layout
        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch() # Stretch is needed to make widgets align left.

        # The second horizontal layout, self.bottom_layout, will have the user's message
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Create a spacer to make message align, vertically, with the user's label
        # Note that the spacer is 55px because the profile is 40px and the spacing is 15px, so we need a spacer of 55px
        # in width to align the user's label with the user's message
        self.bottom_layout_spacer = QSpacerItem(55, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # add spacer and the message
        self.bottom_layout.addItem(self.bottom_layout_spacer)
        self.bottom_layout.addWidget(self.message_content, Qt.AlignmentFlag.AlignLeft)

        # Add both horizontal layout to the vertical layout.
        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        # Set the widget's layout to the vertical layout.
        self.setLayout(self.layout)

# This is the widget that encapsulates the model's message
class ModelMessage(QWidget):
    # Constructor, message var is used to set the label of the widget
    def __init__(self, message, parent=None):
        super().__init__(parent=parent)
        # Set the widget's contents margins to 0
        self.setContentsMargins(0, 0, 0, 0)

        # Layout for the widget, set spacing and contents to 0
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set the min width to 1
        self.setMinimumWidth(1)

        # Set widget's size polity to preferred
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # This is the model's profile picture, and its specifications
        self.icon_label = QLabel(self)
        icon_pixmap = QIcon('feather/group2.svg').pixmap(QSize(40, 40))
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # This is the model's label, and its specifications
        self.username_label = QLabel("GEOINT", self)
        self.username_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.username_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.username_label.setStyleSheet("color: #FFFFFF;")

        # This is the message label, and its specifications
        self.message_content = QLabel(message, self)
        self.message_content.setFont(QFont('Arial', 14, QFont.Weight.ExtraLight))
        self.message_content.setContentsMargins(0,0,0,0)
        self.message_content.setWordWrap(True)
        self.message_content.setStyleSheet("color: #FFFFFF;")

        # This widget consists of two horizontal layouts nested within the vertical layout, self.layout
        # The first horizontal layout, self.top_layout, will have the model's label and the model's profile picture
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.addWidget(self.icon_label) # Add the profile picture to layout
        self.top_layout.addSpacing(15)

        # Add the user's label to layout
        self.top_layout.addWidget(self.username_label, Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch() # Stretch is needed to make widgets align left

        # The second horizontal layout, self.bottom_layout, will have the model's message
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Create a spacer to make message align, vertically, with the model's label
        # Note that the spacer is 55px because the profile is 40px and the spacing is 15px, so we need a spacer of 55px
        # in width to align the model's label with the model's message
        self.bottom_layout_spacer = QSpacerItem(55, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # add spacer and the message
        self.bottom_layout.addItem(self.bottom_layout_spacer)
        self.bottom_layout.addWidget(self.message_content, Qt.AlignmentFlag.AlignLeft)

        # Add both horizontal layout to the vertical layout.
        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        # Set the widget's layout to the vertical layout.
        self.setLayout(self.layout)

# This is the chat widget, it is the messaging widget that will be hosted in the TabWidget in the chat box.
# The chat widget has a message box, send button, and a list of all the previous messages from that particular
# conversation.
# NOTE that a chat widget is created when a conversation is either opened or created
class Chat(QWidget):
    # Constructor, parameters includes the title of the chat, the path to that conversation folder,
    # the list widget that it corresponds to (the list widget from that chat history window)
    def __init__(self, title, chat_folder_path, list_widget_item, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        self.index = 0
        self.title = title

        # Create QFont and set it for the widget.
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)
        self.setFont(self.font1)

        # Store list item for opening and deleting conversation functionality from chat history window
        self.list_widget_item = list_widget_item

        # Store conversation folder pah
        self.chat_folder_path = chat_folder_path

        # store image path, name, and etc. associated with conversation
        self.current_image_name = ""
        self.current_image_path = ""
        self.current_image_path_in_chat_folder = ""

        # Get the application's folder path from the conversation path
        self.app_data_path = os.path.dirname(self.chat_folder_path)

        # Get the path to the uploads folder, the uploads folder holds all the images that have been uploaded
        # to the application's file explorer window.
        self.uploads_folder = os.path.join(self.app_data_path,"uploads")

        # Get the name and path of the json file, the json file in each conversation folder is named data.json
        self.json_file_name = "data.json"
        self.json_file_path = os.path.join(self.chat_folder_path , self.json_file_name)

        # data_dict is the dictionary that will be stored in the json file
        self.data_dict = {}

        # the self.messages array will store the list of the previous messages associated with the conversation,
        # this will be added to  data_dict under the "history" definition. As of right now the messages must
        # alternate between the user's messages and the model's message, users messages will be
        # alternating roles, starting with user input.
        self.messages = []

        # The layout for the widget, self.tab_layout
        self.tab_layout = QVBoxLayout()
        self.tab_layout.setSpacing(20)

        # Set widget's content margins
        self.setContentsMargins(20, 20, 20, 20)

        # Scroll area widget is needed to list all the previous messages
        self.chat_scroll_area = QScrollArea()

        # Set scroll area stylesheet
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

        # Let scroll area resize the widgets that it contains
        self.chat_scroll_area.setWidgetResizable(True)

        # self.chat_scroll_widget is the inner widget for the scroll area
        self.chat_scroll_widget = QWidget()

        # chat_scroll_layout is the layout for the chat_scroll_widget, will hold all the message widgets,
        # message widgets will be the UserMessage and ModelMessage widgets
        self.chat_scroll_layout = QVBoxLayout(self.chat_scroll_widget)
        self.chat_scroll_layout.setContentsMargins(0, 15, 0, 15)
        self.chat_scroll_layout.setSpacing(20)

        # Let messages be added from the top of the widget
        self.chat_scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_scroll_layout.addStretch() # Stretch is added for resizibility

        # Set the scroll area widget to the self.chat_scroll_widget
        self.chat_scroll_area.setWidget(self.chat_scroll_widget)

        # Below the list of messages for the conversations is the input textbox/lineedit, and the send button,
        # We will organize these widgets in a horizontal layout.
        self.chat_input_layout = QHBoxLayout()
        self.chat_input_layout.setAlignment(Qt.AlignmentFlag.AlignTop.AlignLeft)
        self.chat_input_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_input_layout.setSpacing(5)

        # LineEdit allows user to input text message
        self.chat_input = LineEdit()
        self.chat_input.enter_pressed.connect(self.send_message) # allow user to send messages by pressing enter button
        self.chat_input.setPlaceholderText("Type here!")

        # self.send button allows user to send message after typing in a prompt
        self.send_button = icon_button(initial_icon='feather/arrow-up.svg', icon_square_len=22, button_square_len=34)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setToolTip("Send")

        # Loading animation that appears when model is responding
        self.svgLoad = QSvgWidget()
        self.svgLoad.setFixedSize(34, 34)
        self.svgLoad.load("loadingSvgs/LoadingPhase1.svg")

        # Add animation, input, and send button to horizontal layout
        self.chat_input_layout.addWidget(self.svgLoad)
        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.send_button)

        # Make animation hidden until model is prompted to respond
        temp = self.svgLoad.sizePolicy()
        temp.setRetainSizeWhenHidden(True)
        self.svgLoad.setSizePolicy(temp)
        self.svgLoad.setHidden(True)

        # Add teh scroll area and the input layout to the tab_layout
        self.tab_layout.addWidget(self.chat_scroll_area)
        self.tab_layout.addLayout(self.chat_input_layout)

        # Make the tab_layout as layout of this widget
        self.setLayout(self.tab_layout)

        # Load all the previous messages, if this is an existing conversation
        self.load_chat_history()

        # Get scrollbar from scroll area, and when a new widget/message is added, scroll to bottom of page
        # to see the latest messages.
        self.vscrollbar = self.chat_scroll_area.verticalScrollBar()
        self.vscrollbar.rangeChanged.connect(lambda min, max: self.scrollToBottom(min,max))

    # This method changes the color of loading animation to notify the user if the streaming feature is working
    def isStreamLoadSvg(self, isStream:bool):
        # If the streaming feature is working then load the BLUE variant of the animation
        if isStream:
            self.svgLoad.load("loadingSvgs/LoadingPhase2.svg")

        # If the streaming feature is NOT working then load the RED variant of the animation
        else:
            self.svgLoad.load("loadingSvgs/LoadingPhase3.svg")

    # Scroll to bottom of the scroll area function
    def scrollToBottom(self, min, max):
        self.vscrollbar.setValue(max)

    # This method sets the image that is associated with the conversation
    # It will add the image to the conversation folder and add the name to the json file
    def setCurrentImagePath(self, image_path):
        # set current image path to the image path passed to the constructor
        self.current_image_path = image_path

        # If the image path exists and the folder path exists copy the selected image from the
        # path to the conversation folder
        if image_path != "" and self.chat_folder_path != "":
            # copy the image from the path to the conversation folder
            shutil.copy(image_path, self.chat_folder_path)

            # Set self.current_image_name to the image name
            self.current_image_name = os.path.basename(image_path)

            # Set self.current_image_path_in_chat_folder to the path of the image in the conversation folder
            self.current_image_path_in_chat_folder = os.path.join(self.chat_folder_path,self.current_image_name)

        # Set self.current_image_name to the image name
        self.current_image_name = os.path.basename(self.current_image_path)

        # Add the image path to the json file in the conversation folder
        try:
            with open (self.json_file_path, "w") as file:
                self.data_dict.update({"image_url":self.current_image_path})
                json.dump(self.data_dict, file)

        except FileNotFoundError:
            pass

    # This method will perform all the necessary steps to send a message to the model
    def send_message(self):
        # If there is no image associated with the conversation, report error, the model
        # MUST have an image and prompt.
        if (self.current_image_path == ""):
            # Report message in message box
            QMessageBox.critical(None, "Error", "Image not found")

        # If there is an image associated with the conversation
        else:
            # If a message is in the chat line edit
            message = self.chat_input.text()
            if message:
                # Create a user message to package the message
                user_message_widget = UserMessage(message)

                # Add that widget to the scroll area layout.
                self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                # Update the index of the latest widget
                self.index += 1

                # TODO: add the dictionary append area
                # Add the messages to the history list. User messages have a "User: "
                # appended to the beginning of the message
                self.messages.append(f"User: {message}")
                print(self.messages)

                # save the message
                self.save_message()

                # clear the input so user can add another message
                self.chat_input.clear()

                # Create an empty model message
                chat_model_message_widget = ModelMessage('')

                # Prevent user from adding more messages by disabling send button
                # and the enter_button_pressed
                self.send_button.setEnabled(False)
                self.chat_input.enter_pressed.disconnect()

                # Make the animation appear
                self.svgLoad.setHidden(False)

                # Send message to model via modelrunnable worker, which is a QRunnable object
                model_runnable = ModelRunnable(message, self.current_image_path, self.messages,self.chat_scroll_layout,chat_model_message_widget)

                # Connect ModelRunnable finished signal to handle model response funcition
                model_runnable.signals.response_received.connect(self.handle_model_response)

                # Connect ModelRunnable isStream signal to isStreamLoadSvg method to change animation
                model_runnable.signals.isStream.connect(lambda isStream: self.isStreamLoadSvg(isStream))

                # Start the model_runnable QRunnable object to recive the model response
                # We add this to the global QThreadPool
                QThreadPool.globalInstance().start(model_runnable)

    # This method will save/update the data.json file's history definition
    def save_message(self):

        # Try to open dictionary and rewrite/update the history definition with the current self.messages array
        try:
            with open(self.json_file_path, "w") as file:
                self.data_dict.update({"history":self.messages})
                json.dump(self.data_dict, file)

        except FileNotFoundError:
            pass

    # This method will load the chat history if there is messages stored in the history dictionary
    # in the data.json file
    def load_chat_history(self):
        # Check to see if a data.json, if one already exists  this is an existing conversation
        if os.path.exists(self.json_file_path) and self.chat_folder_path!="":
            try:
                # Read the data.json file
                with open(self.json_file_path, "r") as file:
                    # load json dictionary in self.data_dict
                    self.data_dict = json.load(file)

                    # load history definition array in self.messages
                    self.messages = self.data_dict["history"]

                    # traverse the message array and parse them as widgets (ModelMessage and/or UserMessage widgets)
                    # to be displayed in the scroll area
                    for message_text in self.messages:
                        # If message is a user message
                        if message_text.startswith("User:"):
                            # Remove 'User:' part from message
                            user_message_text = message_text[len("User:"):].strip()

                            # Create UserMessage widget with extracted text, and publish it to chat_scroll_layout
                            user_message_widget = UserMessage(user_message_text)
                            self.chat_scroll_layout.addWidget(user_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                            # Update the index of the latest widget/message
                            self.index += 1
                        # If message is a model message
                        else:
                            # model_message_text = message_text[len("GEOINT:"):].strip()

                            # Create Model Message widget with extracted text, and publish it to chat_scroll_layout
                            model_message_text = message_text
                            model_message_widget = ModelMessage(model_message_text)
                            self.chat_scroll_layout.addWidget(model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

                            # Update the index of the latest widget/message
                            self.index += 1

                    # Read the image url dictionary, and set the image attributes within this object
                    self.current_image_path = self.data_dict["image_url"]
                    self.current_image_name = os.path.basename(self.current_image_path)
                    self.current_image_path_in_chat_folder = os.path.join(self.chat_folder_path,self.current_image_name)

            except FileNotFoundError:
                pass

        # If the conversation is a new conversation, create a data.json file
        elif self.chat_folder_path != "":
            try:
                # Create and open a data.json file
                with open(self.json_file_path, "x") as file:
                    # This is the schema for the data.json file
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
                    # Add this dictionary to the fil
                    json.dump(self.data_dict, file)

            except FileNotFoundError:
                pass

    # This method will handle the model's response, and will only be called when the model responds
    def handle_model_response(self, model_message_text):
        # Hide the loading animation, and reset the loading color
        self.svgLoad.setHidden(True)
        self.svgLoad.load("loadingSvgs/LoadingPhase1.svg")

        # Reconnect the send button and the enter_pressed
        self.chat_input.enter_pressed.connect(self.send_message)
        self.send_button.setEnabled(True)

        # Update the index of the latest message/widget
        self.index += 1

        # Append the model's response to the message array and update the dictionary in the data.json file via
        # save_message function
        self.messages.append(model_message_text)
        self.save_message()

        self.update()

# This is the Tab Widget that will allow users to hold multiple conversations and create conversations
class ChatTabWidget(TabWidget):
    # Signal emits a signal to change the isOpen attribute in the chat history widget
    changeCloseAttribute = pyqtSignal(str)

    # Constructor, app_data_path is the path to the application's data, chat_history_widget is the chat history widget
    # Not necessarily a good way of connecting widgets, but doing it without passing it would require multiple
    # signals and connections between them.
    def __init__(self, app_data_path, chat_history_widget, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Set the first tab as the help widget
        self.help_widget = HelpWidget(self)
        self.addTab2(widget=self.help_widget, title="Help")

        # Set the app data path to the
        self.app_data_path = app_data_path

        # Get chat_history folder path from self.app_data_path
        self.chat_history_path = os.path.join(app_data_path,"chat_history")

        # Connect addButton from TabWidget to self.add_new_chat() to add a new tab
        self.addButton.clicked.connect(lambda: self.add_new_chat())

        # Pass chat_history_widget to local var
        self.chat_history_widget = chat_history_widget

        # Connect close requrest signal to removeTab3 function
        self.tabCloseRequested.connect(self.removeTab3)

        # Connect the loadExistingChat signal to the add_existing_chat method within this widget
        self.chat_history_widget.loadExistingChat.connect(
            lambda tab_name, chat_folder_path, list_widget_item: self.add_existing_chat(tab_name,chat_folder_path,list_widget_item))

    # This method will remove the tab, and update the list_widget_item's attribute
    # is_open to False
    def removeTab3(self,index):
        # Get the widget at the index requested to be deleted
        temp_widget = self.widget(index)

        # Get the list_widget_item from the widget
        list_widget_item = temp_widget.list_widget_item

        # Get the custom widget of the list_widget_item
        chat_list_item = self.chat_history_widget.itemWidget(list_widget_item)

        # Set the custom list item's is_open attribute to false
        chat_list_item.is_open = False

        # Remove the tab at the requested index
        self.removeTab2(index)

    # This method will create a new tab for a new conversation
    def add_new_chat(self):
        # Load an input dialog to allow user to input a name for the conversation
        input_dialog = CustomInputDialog(self)
        ok = input_dialog.exec()
        tab_name = input_dialog.textValue()

        # If a name is added and the ok button has been pressed
        if ok and tab_name:
            # Create a new chat_history_widget in the Chat History Window, it
            # will return the conversation folder and the list widget item
            chat_folder_path, list_widget_item = self.chat_history_widget.create_item_from_new_chat(tab_name)
            self.tempWidget = Chat(tab_name, chat_folder_path,list_widget_item)
            self.addTab2(widget=self.tempWidget, title=tab_name)

        # After creating the widget go to that tab, usually the end tab
        self.setCurrentIndex(self.count()-1)

    # THis method is used to create a new tab when an existing conversation is
    # signaled to be opened
    def add_existing_chat(self, tab_name, chat_folder_path, list_widget_item):

        # Get the custom chat list item from list_widget_item in chat_history_widget
        chat_list_item = self.chat_history_widget.itemWidget(list_widget_item)

        # If the conversation is not already opened
        if not chat_list_item.is_open:
            # Set chat_list_item.is_open to true
            chat_list_item.is_open =True

            # Create the chat widget from the contents of the conversation
            # folder (the tab name, chat folder path, and list widget item)
            self.tempWidget = Chat(tab_name, chat_folder_path, list_widget_item)
            self.addTab2(widget=self.tempWidget, title=tab_name)

            # After creating the widget go to that tab, usually the end tab
            self.setCurrentIndex(self.count()-1)

        # If the conversation is already opened go to that tab
        elif chat_list_item.is_open:
            # Traverse all the tabs in the tab widget
            for index in range(self.count()):
                temp_chat = self.widget(index)
                temp_chat_list_widget_item = temp_chat.list_widget_item

                # If the list_widget_item that produced the signal matches the
                # conversation's list_widget_item set the current index to that tab
                if temp_chat_list_widget_item == list_widget_item:
                    self.setCurrentIndex(index)