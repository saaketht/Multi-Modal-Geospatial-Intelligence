
# This file contains custom components related to the Chat History Dockable Window.

import os, shutil
from datetime import datetime
from chatbox_file import *
from PyQt6.QtWidgets import (
    QHBoxLayout, QWidget,
    QListWidget, QMessageBox,
    QListWidgetItem, QSizePolicy,
    QAbstractItemView
)

# This is a custom QListWidget used for managing all of the user's previous conversation
class ChatHistoryListWidget(QListWidget):
    # This signal will be emmited from the open button click signal in the custom list widget, and will be connected to
    # the add_existing_chat function in the ChatTabWidget class,
    loadExistingChat = pyqtSignal(str, str, QListWidgetItem)

    # Constructor, the app_data_path is the path to the user's application folder,
    # where we will store all the user's previous conversation
    def __init__(self, app_data_path, parent=None):
        # Call the Parent Constuctor for QListWidget
        super().__init__(parent=parent)

        # Deactivate selection mode
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Create a chat_history folder in the application folder, if it does not exist already
        self.chat_data_path = os.path.join(app_data_path, "chat_history")
        if not os.path.exists(self.chat_data_path):
            os.makedirs(self.chat_data_path)

        # Set stylesheet for QListWidget
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

        # Call the load_items method, to load all the user's conversations when the application is opened.
        self.load_items()


    # Method creates a new list item in list widget when user creates a NEW conversation.
    # When a user creates a new list a new folder is added within the chat_history folder in the application's folder
    # to store the data related to that conversation
    def create_item_from_new_chat(self, title_prompt):
        # Create an instance of the custom chat list item, with title_prompt
        custom_list_item_widget = ChatListItem(title_prompt)

        # When a new conversation is created, it is automatically opened, so set is_open attribute to True
        custom_list_item_widget.is_open = True

        # Create a new instance of the QListWidgetItem to add to the QListWidget
        list_widget_item = QListWidgetItem(self, type=QListWidgetItem.ItemType.UserType)

        # We set the QListWidgetItem to the size of the custom chat list item size hint
        list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

        # Add the item and set the item to the custom chat list item
        self.addItem(list_widget_item)
        self.setItemWidget(list_widget_item, custom_list_item_widget)

        # We name the folder after the date it was created
        now = datetime.now()
        chat_folder_name = now.strftime("%m-%d-%Y_%H-%M-%f")

        # Join the folder to the chat_history folder in the application's folder
        chat_folder_path = os.path.join(self.chat_data_path, chat_folder_name)

        # Connect the remove button of the custom-list widget item to the remove method
        custom_list_item_widget.remove_button.clicked.connect(
            lambda: self.remove_item(list_widget_item, chat_folder_path))

        # Connect the open button of the custom-list widget item to the open method
        custom_list_item_widget.open_button.clicked.connect(
            lambda: self.loadExistingChat.emit(title_prompt,chat_folder_path,list_widget_item))

        # Set the list_widget_item attribute of the custom list widget item to the QListWidget item
        custom_list_item_widget.list_widget_item = list_widget_item

        # Make the new chat folder within the chat_history folder in the application folder
        # if the folder already exists, append a 1 to make it unique.
        if not os.path.exists(chat_folder_path):
            os.makedirs(chat_folder_path)
        else:
            chat_folder_path = chat_folder_path + "1"
            os.makedirs(chat_folder_path)

        # Return the newly created chat folder path and the list widget item.
        return chat_folder_path, list_widget_item

    # This method will re-create the list widget items for each conversation folder that is in the chat_history folder
    def create_item_from_existing_chat(self, title_prompt, chat_folder_path):

        # Create a new chat widget item
        custom_list_item_widget = ChatListItem(title_prompt)

        # Set is_open attribute False, because when the list of conversations are loaded, none of the conversations are loaded.
        custom_list_item_widget.is_open = False

        # Create a new instance of the QListWidgetItem to add to the QListWidget
        list_widget_item = QListWidgetItem(self, type=QListWidgetItem.ItemType.UserType)

        # We set the QListWidgetItem to the size of the custom chat list item size hint
        list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

        # Add the item and set the item to the custom chat list item
        self.addItem(list_widget_item)
        self.setItemWidget(list_widget_item, custom_list_item_widget)

        # Connect the remove button of the custom-list widget item to the remove method
        custom_list_item_widget.remove_button.clicked.connect(
            lambda: self.remove_item(list_widget_item, chat_folder_path))

        # Connect the open button of the custom-list widget item to the open method
        custom_list_item_widget.open_button.clicked.connect(
            lambda: self.loadExistingChat.emit(title_prompt, chat_folder_path, list_widget_item))

        custom_list_item_widget.list_widget_item = list_widget_item

    #  This method removes previous conversations, its connected to the remove button
    def remove_item(self, list_widget_item, path):

        # get the custom widget from the QListWidget
        chat_list_item = self.itemWidget(list_widget_item)

        # If the custom widget's is_open attribute is True, reject deletion
        if(chat_list_item.is_open):
            QMessageBox.critical(self, "Error", "This chat is open, please close tab before deleting!")

        # Else delete the conversation folder in the chat_history folder.
        else:
            try:
                # Remove the list item from the list
                row = self.row(list_widget_item)
                self.takeItem(row)
            except Exception as e:
                print(f"Error removing item: {e}")

            # remove the conversation folder
            shutil.rmtree(path)

    # This method will load all the conversations in the list widget from the chat_history folder.
    def load_items(self):
        # Traverserse each folder and read the json file to read the name the user gave that conversation.
        # This name will be displayed in the QListWidget.
        for root, dir, file in os.walk(self.chat_data_path):
            print(root)
            print(dir)
            print(file)

            # Every json file in the conversation folder is named data.json
            filename = "data.json"

            # If the file in the conversation folder is the data.json file
            if filename in file:
                # Read the file for the name.
                root_dir = os.path.join(root, filename)
                try:
                    with open(root_dir,"r") as json_file:
                        test_dic = json.load(json_file)
                        title_prompt = test_dic["chat_id"]
                        self.create_item_from_existing_chat(title_prompt, root)

                except FileNotFoundError:
                    pass

# This is the custom widget for the QListWidgetItem
class ChatListItem(QWidget):
    # Constructor, the var text is used as the item's title
    def __init__(self, text, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Layout for the widget
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(5)

        # Set is_open attribute, True by default
        self.is_open = True

        # QWidget's size policy
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Open button
        self.open_button = icon_button(initial_icon="feather/message-circle.svg", icon_square_len=22, button_square_len=34)
        self.open_button.setToolTip("Open")

        # Remove button
        self.remove_button = icon_button(exit=True, icon_square_len=22, button_square_len=34)
        self.remove_button.setIcon(QIcon("feather/trash-2.svg"))
        self.remove_button.setToolTip("Remove")

        # Set the label to the text var from constructor
        self.label = Label(text)
        self.label.setToolTip(text)

        # Make Label content align center, and set its size policy
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        # Add widgets to layout
        layout.addWidget(self.open_button)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.remove_button)
