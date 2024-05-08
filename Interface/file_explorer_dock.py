
# This file contains widgets related to the File Explorer Window

import os, shutil
import rasterio
from PyQt6.QtWidgets import (
    QListWidget, QFileDialog
)
from PyQt6.QtCore import  QEvent
from rasterio.errors import CRSError
from image_preview_dock import *
from component_file import *
from chatbox_file import *

# This is a custom splitter that will hold two widgets
# The first widget is the image preview widget
# The second is the file explorer widget
# Its purpose is to make the splitter change from horizontal
# to vertical based on the size of the splitter
class FileExplorerSplitter (Splitter):
    # Constructor, takes two widgets
    def __init__(self, firstWidget: QWidget, secondWidget: QWidget, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Add the two widgets
        self.addWidget(firstWidget)
        self.addWidget(secondWidget)

        # Set the orientation, initially vertical
        self.setOrientation(Qt.Orientation.Vertical)

    # Override the resizeEvent
    # to change from vertical to horizontal when necessary
    def resizeEvent(self, e):
        # Get the size of the splitter
        height = self.height()
        width = self.width()

        # If the width is bigger than 1.5 times the height make the orientation horizontal
        if height*1.5 < width:
            self.setOrientation(Qt.Orientation.Horizontal)

        # Otherwise make the orientation vertical
        else:
            self.setOrientation(Qt.Orientation.Vertical)

        # Call parent resize event
        super().resizeEvent(e)


# This is the file explorer widget that will be hosted within a qdockwidget,specifically the "docks" variant
class file_explorer(QWidget):
    #signals returns path name, index of widget, if image is already displayed, and if image that
    # is being displayed exists in file explorer (always true for files in file explorer).
    # These signals will toggle the chosen image to either the Current Image Window, the Interactive Map, and/or the
    # Image preview widget within the file explorer
    toggleImagePreviewWidget = pyqtSignal(str, QListWidgetItem, bool,bool)
    toggleImagePreviewWidget2 = pyqtSignal(str, QListWidgetItem, bool,bool)
    toggleInteractiveMap = pyqtSignal(str, QListWidgetItem, bool)

    # Constructor, takes the application's folder path
    def __init__(self, app_data_path, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Get the uploads folder path from the application's folder, if the folder does not
        # exist create one
        self.uploads_folder = os.path.join(app_data_path, "uploads")
        if not os.path.exists(self.uploads_folder):
            os.makedirs(self.uploads_folder)

        # Make A QListWidget to store the list of images the user uploads to the file explorer
        self.file_list = QListWidget()

        # file_path_line_edit will allow users to enter the path to the image to upload images/files
        self.file_path_line_edit = LineEdit()
        self.file_path_line_edit.setPlaceholderText("Enter Path to Image Here!")

        # Disable selection mode for QListWidget
        self.file_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)

        # This widget consists of two layouts, the horizontal layout and the vertical layout
        # the horizontal layout will hold the buttons and textbox for entering a file, and the vertical layout
        # will be the overall layout, it will have the horizontal layout and then the List widget

        # This is the horizontal layout for holding the buttons and textbox for uploading a file
        self.file_explorer_horizontal_layout = QHBoxLayout()
        self.file_explorer_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.file_explorer_horizontal_layout.setSpacing(5)

        # Set the stylesheet of the ListWidget
        self.file_list.setStyleSheet('''
        QListWidget 
        {
            border-top: 2px solid #494949;
            border-bottom: 2px solid #494949;
            border-right: 0;
            border-left: 0;
            border-radius:0;
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

        # This is the open folder button will open the file explorer on the user's system
        # to navigate what file the user would like to upload
        self.open_folder_button = icon_button(initial_icon='feather/folder.svg', icon_square_len=22,
                                              button_square_len=34)
        self.open_folder_button.setToolTip("Open System's Files")
        # The open folder button is connected to the open_file_dialog method
        self.open_folder_button.clicked.connect(self.open_file_dialog)

        # After navigating a file/image a user can use the add button to
        # add that file/image to the listwidget
        self.add_file_button = icon_button(initial_icon='feather/plus.svg', icon_square_len=22, button_square_len=34)
        self.add_file_button.setToolTip("Add File")
        # The add_file_button folder button is connected to the add_file_to_list method
        self.add_file_button.clicked.connect(lambda: self.add_file_to_list(self.file_path_line_edit.text()))

        # We add the buttons and line edit to the horizontal layout
        self.file_explorer_horizontal_layout.addWidget(self.open_folder_button)
        self.file_explorer_horizontal_layout.addWidget(self.file_path_line_edit)
        self.file_explorer_horizontal_layout.addWidget(self.add_file_button)

        # The vertical layout will hold the horizontal layout and the list widget
        self.file_explorer_vertical_layout = QVBoxLayout()
        self.file_explorer_vertical_layout.setSpacing(8)
        self.file_explorer_vertical_layout.setContentsMargins(0,10,0,0)

        # add the horizontal layout and list widget, self.file_list
        self.file_explorer_vertical_layout.addLayout(self.file_explorer_horizontal_layout)
        self.file_explorer_vertical_layout.addWidget(self.file_list)

        # set this vertical layout as the layout of the file explorer
        self.setLayout(self.file_explorer_vertical_layout)

        # Load all of the files already uploaded to the applicaiton
        self.load_existing_data()

    # Wrapper method for add_file_to_list
    def add_new_file(self, file_path):
        self.add_file_to_list(file_path)

    # This method loads the QFileDialog, allows users to upload images
    def open_file_dialog(self):
        # Get the file path of the selected image/file, only allow tiff, geotiff,
        # png, and jpegs.
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image file", "", "Image files (*.png *.jpg *.jpeg "
                                                                                  "*.bmp *.tiff *.tif)")
        # If file/image is entered/selected add the path to the line edit for users to preview before adding
        if file_path:
            self.file_path_line_edit.setText(file_path)

    # This method adds the file to the list widget, this is triggered from the add button
    def add_file_to_list(self, file_path):
        try:
            # If the file path exists
            if file_path and os.path.isfile(file_path):
                # If the image comes from the uploads folder
                # This condition is used for loading files from the file explorer
                if os.path.dirname(file_path) == self.uploads_folder:
                    # Get the basename
                    base_name = os.path.basename(file_path)

                    # Create a custom list widget item with the basename and set the file path to the folder and the
                    custom_list_item_widget = CustomListItem(base_name, file_path)

                    # Create a QListWidgetItem
                    list_widget_item = QListWidgetItem(self.file_list)

                    # Let the size hint of the QListWidgetitem be the same as the custom list widget item
                    list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

                    # Add the QListWidgetItem to the QListWidget
                    self.file_list.addItem(list_widget_item)

                    # Set the custom list widget item to the QListWidgetItem
                    self.file_list.setItemWidget(list_widget_item, custom_list_item_widget)

                    # Connect the buttons from the custom list widget item to their respective functions
                    custom_list_item_widget.remove_button.clicked.connect(lambda: self.remove_item(list_widget_item))

                    custom_list_item_widget.world_button.clicked.connect(
                        lambda: self.world_button_signal(custom_list_item_widget,list_widget_item))

                    custom_list_item_widget.eye_button.clicked.connect(
                        lambda: self.eye_button_signal(custom_list_item_widget, list_widget_item))

                    # If the file is a GeoTiff connect its
                    # map button, the map button only appears for GeoTiffs
                    if custom_list_item_widget.isGeoReferenced:
                        custom_list_item_widget.map_button.clicked.connect(
                            lambda: self.map_button_signal(custom_list_item_widget, list_widget_item))

                    # Set the "list_widget" attribute of the custom list widget item equal to the list_widget_item
                    custom_list_item_widget.list_widget_item = list_widget_item

                # This condition used when we are adding a new image/file to the file explorer
                else:
                    # Get the basename
                    base_name = os.path.basename(file_path)

                    # Get the expected/desired path for the file, which is uploads folder
                    new_file_path = os.path.join(self.uploads_folder, base_name)

                    # If the file is already uploaded to the file explorer add a counter to the basename
                    file_root, file_extension = os.path.splitext(base_name)
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_name = f"{file_root}({counter}){file_extension}"
                        new_file_path = os.path.join(self.uploads_folder, new_file_name)
                        base_name = new_file_name
                        counter += 1

                    # Add the file from the file path to the uploads folder
                    shutil.copy(file_path, new_file_path)

                    # Create a custom list widget item with the basename and set the file path to the folder and the
                    custom_list_item_widget = CustomListItem(base_name, new_file_path)

                    # Create a QListWidgetItem
                    list_widget_item = QListWidgetItem(self.file_list)

                    # Let the size hint of the QListWidgetitem be the same as the custom list widget item
                    list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

                    # Add the QListWidgetItem to the QListWidget
                    self.file_list.addItem(list_widget_item)

                    # Set the custom list widget item to the QListWidgetItem
                    self.file_list.setItemWidget(list_widget_item, custom_list_item_widget)

                    # Connect the buttons from the custom list widget item to their respective functions
                    custom_list_item_widget.remove_button.clicked.connect(lambda: self.remove_item(list_widget_item))

                    custom_list_item_widget.world_button.clicked.connect(
                        lambda: self.world_button_signal(custom_list_item_widget, list_widget_item))

                    custom_list_item_widget.eye_button.clicked.connect(
                        lambda: self.eye_button_signal(custom_list_item_widget, list_widget_item))

                    # If the file is a GeoTiff connect its
                    # map button, the map button only appears for GeoTiffs
                    if custom_list_item_widget.isGeoReferenced:
                        custom_list_item_widget.map_button.clicked.connect(
                            lambda: self.map_button_signal(custom_list_item_widget, list_widget_item))

                    # Set the "list_widget" attribute of the custom list widget item equal to the list_widget_item
                    custom_list_item_widget.list_widget_item = list_widget_item

                    # Clear the line edit, that displays the path to the image, from the
                    # self.open_file_dialog method
                    self.file_path_line_edit.clear()
            # If the file does not exist, report message to user that the path does
            # not exist
            else:
                QMessageBox.information(self, "Error", "Invalid file path.")

        # If there was an error adding a file report error
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    # This method removes a file from the list and from the upload folder
    def remove_item(self, list_widget_item):
        # Try to catch an error is one occurs while deleting a file
        try:
            # Get the row for which the item is at
            row = self.file_list.row(list_widget_item)

            # Get the custom list widget item from the list widget item
            custom_list_item_widget = self.file_list.itemWidget(list_widget_item)

            # Get the filename from the custom list widget
            filename = custom_list_item_widget.label.text()

            # Get the path of the image in the upload folder from the filename and the uploads folder path
            image_path = os.path.join(self.uploads_folder, filename)

            # Remove image from uploads folder
            os.remove(image_path)

            # Remove the item from the row
            self.file_list.takeItem(row)

        # Report error if there was one when removing the image
        except Exception as e:
            print(f"Error removing item: {e}")

    # This method is connected to the map button, when clicked
    # It will prepare the GeoTiff image to be graphed on a map.
    # The map button will behave in a radio fashion, meaning that only one map button will
    # be toggled at a time. Remember every file has a set of map (map buttons only display for GeoTiff Files),
    # globe, and preview buttons.
    def map_button_signal(self,custom_list_item_widget, list_widget_item):
        # Store list widget item as a local var with identifier temp_list_widget_item
        temp_list_widget_item = list_widget_item

        # If the custom_list_item_widget's is_tiff_displayed attribute is true, meaning the tiff
        # image is already displayed, this means the user wants to untoggle the button, so untoggle it.
        if custom_list_item_widget.is_tiff_displayed:
            # Reset the button's map icon
            custom_list_item_widget.map_button.setIcon(QIcon('feather/map.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to ungraph the tiff image in the Interactive Map
            self.toggleInteractiveMap.emit(image_file_path, temp_list_widget_item,
                                                custom_list_item_widget.is_tiff_displayed)

            # Set the is_tiff_displayed attribute for the custom_list_item_widget to False
            custom_list_item_widget.is_tiff_displayed = False

        # If the custom_list_item_widget's is_tiff_displayed attribute is False, meaning the tiff
        # image is NOT already displayed, this means the user wants to toggle the button, so toggle it.
        else:
            # Set the button's map icon to an X to indicate that it is being displayed
            custom_list_item_widget.map_button.setIcon(QIcon('feather/x.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to graph the tiff image in the Interactive Map
            self.toggleInteractiveMap.emit(image_file_path, temp_list_widget_item,
                                           custom_list_item_widget.is_tiff_displayed)

            # Set the is_tiff_displayed attribute for the custom_list_item_widget to True
            custom_list_item_widget.is_tiff_displayed = True

            # When graphed make sure the toggled list widget item can be seen
            self.file_list.scrollToItem(list_widget_item)

    # This method is connected to the eye button, when clicked
    # It will prepare the image to be previewed in the file explorer.
    # The eye button will behave in a radio fashion, meaning that only one eye button will
    # be toggled at a time. Remember every file has a set of map (map buttons only display for GeoTiff Files),
    # globe, and preview buttons.
    def eye_button_signal(self,custom_list_item_widget, list_widget_item):
        # Store list widget item as a local var with identifier temp_list_widget_item
        temp_list_widget_item = list_widget_item

        # If the custom_list_item_widget's is_preview_image_displayed attribute is true, meaning the image
        # is already displayed, this means the user wants to untoggle the button, so untoggle it.
        if custom_list_item_widget.is_preview_image_displayed:
            # Reset the button's eye icon
            custom_list_item_widget.eye_button.setIcon(QIcon('feather/eye.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to unview the image in the File Explorer Image Preview Widget
            self.toggleImagePreviewWidget2.emit(image_file_path, temp_list_widget_item,
                                               custom_list_item_widget.is_preview_image_displayed, True)

            # Set the is_preview_image_displayed attribute for the custom_list_item_widget to False
            custom_list_item_widget.is_preview_image_displayed = False

        # If the custom_list_item_widget's is_preview_image_displayed attribute is False, meaning the
        # image is NOT already displayed, this means the user wants to toggle the button, so toggle it.
        else:
            # Set the button's eye icon to an eye-off icon to indicate that it is being displayed
            custom_list_item_widget.eye_button.setIcon(QIcon('feather/eye-off.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to view the image in the File Explorer Image Preview Widget
            self.toggleImagePreviewWidget2.emit(image_file_path, temp_list_widget_item,
                                               custom_list_item_widget.is_preview_image_displayed, True)

            # Set the is_preview_image_displayed attribute for the custom_list_item_widget to True
            custom_list_item_widget.is_preview_image_displayed = True

            # When graphed make sure the toggled list widget item can be seen
            self.file_list.scrollToItem(list_widget_item)

    # This method is connected to the globe button, when clicked
    # It will prepare the image to be viewed  in the Current Image Window, and
    # appended to the current conversation for querying.
    # The globe button will behave in a radio fashion, meaning that only one globe button will
    # be toggled at a time. Remember every file has a set of map (map buttons only display for GeoTiff Files),
    # globe, and preview buttons.
    def world_button_signal(self, custom_list_item_widget, list_widget_item):
        # Store list widget item as a local var with identifier temp_list_widget_item
        temp_list_widget_item = list_widget_item

        # If the custom_list_item_widget's is_image_displayed attribute is true, meaning the image
        # is already displayed, this means the user wants to untoggle the button, so untoggle it.
        if custom_list_item_widget.is_image_displayed:
            # Reset the button's globe icon
            custom_list_item_widget.world_button.setIcon(QIcon('feather/globe.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to view the image in the Current Image Window
            self.toggleImagePreviewWidget.emit(image_file_path,temp_list_widget_item , custom_list_item_widget.is_image_displayed,True)

            # Set the is_image_displayed attribute for the custom_list_item_widget to False
            custom_list_item_widget.is_image_displayed = False

        # If the custom_list_item_widget's is_image_displayed attribute is False, meaning the
        # image is NOT already displayed, this means the user wants to toggle the button, so toggle it.
        else:
            # Set the button's eye icon to an X to indicate that it is being displayed
            custom_list_item_widget.world_button.setIcon(QIcon('feather/x.svg'))

            # Get the image file path from the image_path attribute from custom_list_item_widget
            image_file_path = custom_list_item_widget.image_path

            # Emit a signal to view the image in the Current Image Window
            self.toggleImagePreviewWidget.emit(image_file_path, temp_list_widget_item, custom_list_item_widget.is_image_displayed, True)

            # Set the is_image_displayed attribute for the custom_list_item_widget to True
            custom_list_item_widget.is_image_displayed = True

            # When graphed make sure the toggled list widget item can be seen
            self.file_list.scrollToItem(list_widget_item)

    # This method is used to reset the globe button under the condition that another
    # image has been signaled to be viewed.
    # This resets the previously toggled button allowing for another one to be toggled.
    # Instead of calling the button signal to untoggle it, we just reset it because if we will call the
    # button signal the Current Image Window will be enabled to reset the image to empty.
    # We dp not want to reset the Image, we just want to change the image, thus we do not use the world_button signal
    def radio_reset_for_custom_list_item(self, list_widget_item):
        # Store list_widget_item as a local var with the identifier item
        item = list_widget_item

        # get the custom widget of the list_widget_item
        widget_at_index = self.file_list.itemWidget(item)

        # Reset the button's globe icon
        widget_at_index.world_button.setIcon(QIcon('feather/globe.svg'))

        # Set the is_image_displayed attribute for the custom_list_item_widget to False
        widget_at_index.is_image_displayed = False

        # Only re-enable the remove button if image isn't being displayed in the other two
        # windows
        if (not widget_at_index.is_preview_image_displayed) and (not widget_at_index.is_tiff_displayed):
            widget_at_index.remove_button.setEnabled(True)

    # This method is used to reset the eye button under the condition that another
    # image has been signaled to be viewed.
    # This resets the previously toggled button allowing for another one to be toggled.
    # Instead of calling the button signal to untoggle it, we just reset it because if we will call the
    # button signal the Image Preview in the File Explorer will be enabled to reset the image to empty.
    # We dp not want to reset the Image, we just want to change the image, thus we do not use the eye_button signal
    def radio_reset_for_custom_list_item2(self, list_widget_item):
        # Store list_widget_item as a local var with the identifier item
        item = list_widget_item

        # get the custom widget of the list_widget_item
        widget_at_index = self.file_list.itemWidget(item)

        # Reset the button's eye icon
        widget_at_index.eye_button.setIcon(QIcon('feather/eye.svg'))

        # Set the is_preview_image_displayed attribute for the custom_list_item_widget to False
        widget_at_index.is_preview_image_displayed = False

        # Only re-enable the remove button if image isn't being displayed in the other two
        # windows
        if (not widget_at_index.is_image_displayed) and (not widget_at_index.is_tiff_displayed):
            widget_at_index.remove_button.setEnabled(True)

    # This method is used to reset the map button under the condition that another
    # tiff image has been signaled to be graphed.
    # This resets the previously toggled button allowing for another one to be toggled.
    # Instead of calling the button signal to untoggle it, we just reset it because if we will call the
    # button signal the Interactive Map Window will be enabled to ungraph the tiff image to empty.
    # We do not want to reset the Image, we just want to change the image, thus we do not use the map_button signal
    def radio_reset_for_custom_list_item3(self, list_widget_item):
        # Store list_widget_item as a local var with the identifier item
        item = list_widget_item

        # get the custom widget of the list_widget_item
        widget_at_index = self.file_list.itemWidget(item)

        # Reset the button's map icon
        widget_at_index.map_button.setIcon(QIcon('feather/map.svg'))

        # Set the is_tiff_displayed attribute for the custom_list_item_widget to False
        widget_at_index.is_tiff_displayed = False

        # Only re-enable the remove button if image isn't being displayed in the other two
        # windows
        if (not widget_at_index.is_image_displayed) and (not widget_at_index.is_preview_image_displayed):
            widget_at_index.remove_button.setEnabled(True)

    # This method will traverse the uploads folder to display all the images that have been
    # uploaded to the applicaiton via the File Explorer
    def load_existing_data(self):
        # Get the directory of the uploads folder
        directory = os.fsencode(self.uploads_folder)

        # Traverse every file in the directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)

            # Get the path for each file
            path = os.path.join(self.uploads_folder, filename)

            # Add that image to the list in the file explorer widget via
            # self.add_file_to_list method
            self.add_file_to_list(path)

    # This method is used to get a list widget item from the image path
    def get_list_widget_item(self, image_path):
        # Traverse all widgets in the list widget via index and return if
        # target image path has been found
        for index in range(self.file_list.count()):
            # Get the list widget from the index in the ListWidget
            list_widget_item = self.file_list.item(index)

            # Get the custom list widget item from the ListWidgetItem
            custom_list_item = self.file_list.itemWidget(list_widget_item)

            # If the custom list widget item's image_path attribute matches the
            # desired image_path return it.
            if image_path == custom_list_item.image_path:
                return list_widget_item
        # If the custom list widget item's image_path attribute does not match the
        # desired image_path return None.
        return None


# This is the custom widget that will be used in place of the QListWidgetItem for
# The QListWidget in the file_explorer widget
class CustomListItem(QWidget):
    # Constructor, parameters include text for the label and the image path
    def __init__(self, text, image_path, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # This widget has a Horizontal layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 11, 0, 11)
        layout.setSpacing(5)

        # Set size policy to ignored to take all the space up in the QListWidget
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # All the possible buttons that can be displayed per image/file
        self.remove_button = icon_button(initial_icon='feather/image.svg', icon_square_len=22, button_square_len=34)
        self.eye_button = icon_button(initial_icon='feather/eye.svg', icon_square_len=22, button_square_len=34)
        self.world_button = icon_button(initial_icon='feather/globe.svg', icon_square_len=22, button_square_len=34)
        self.map_button = icon_button(initial_icon='feather/map.svg', icon_square_len=22, button_square_len=34)

        # Set tooltips for each button
        self.remove_button.setToolTip("Delete")
        self.eye_button.setToolTip("Preview Image")
        self.world_button.setToolTip("Analyze Image")
        self.map_button.setToolTip("Map GeoTiff File")

        # Label for the image
        self.label = Label(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.label.setToolTip(text)

        self.remove_button.installEventFilter(self)

        # Attributes
        self.image_path = image_path  # Stores the image's path that is associated with
        self.is_preview_image_displayed = False  # Bool val represents if image is displayed in Current Image Window
        self.is_image_displayed = False  # Bool val represents if image is displayed in Image Preview Widget
        self.is_tiff_displayed = False  # Bool val represents if image is displayed in Interactive Map Window
        self.isGeoReferenced = False  # Bool val represents if image is a GeoTiff

        # Get base name of file and extension
        self.image_basename = os.path.basename(self.image_path)
        _ , self.image_type = os.path.splitext(self.image_basename)

        # Check if image is tiff image
        if self.image_type == ".tiff" or self.image_type == ".tif":

            # Check if tiff image is geo-referenced
            _, isGeoReferenced =self.check_georeference(self.image_path)

            # If so add the map button and update respective attribute
            if isGeoReferenced:
                self.isGeoReferenced = True
                layout.addWidget(self.map_button)

            # Else add the map button and update respective attribute
            else:

                self.isGeoReferenced = False
                layout.addWidget(self.map_button)

                # Disable map button
                self.map_button.setEnabled(False)

        # Add remove button first
        layout.addWidget(self.remove_button)

        # If the file is tiff and is geo-referenced make label green
        if self.isGeoReferenced:
            self.label.setStyleSheet('''
        Label
        {
            background: transparent;
            padding: 0 16px;
            border-top:0;
            border-bottom:2px solid #494949;
            border-right:0;
            border-left:0;
            border-radius:0;
            color: rgb(109,148,92);
        }
        ''')

        # If the image is tiff but not geo-referenced make label red
        elif self.isGeoReferenced == False and (self.image_type == ".tiff" or self.image_type == ".tif"):
            self.label.setStyleSheet('''
            Label
            {
                background: transparent;
                padding: 0 16px;
                border-top:0;
                border-bottom:2px solid #494949;
                border-right:0;
                border-left:0;
                border-radius:0;
                color: rgb(229,96,104);
            }
        ''')

        # Default label color is white

        # Add label to widget
        layout.addWidget(self.label, 1)

        # If image is tiff and geo-referenced add map button
        if self.isGeoReferenced:
            layout.addWidget(self.map_button)

        # If image is tiff but not geo-referenced add map button but disable it.
        elif self.isGeoReferenced == False and (self.image_type == ".tiff" or self.image_type == ".tif"):
            layout.addWidget(self.map_button)
            self.map_button.setEnabled(False)

        # Add eye button and world button
        layout.addWidget(self.eye_button)
        layout.addWidget(self.world_button)

    # This method checks if a tiff image is geo-referenced
    def check_georeference(self, file_path):
        try:
            with rasterio.open(file_path) as src:
                # Check for a valid coordinate reference system
                if src.crs is None:
                    return "GeoTIFF error: No coordinate reference system found.", False

                # Check the geotransform
                if src.transform is None or src.transform == (0, 1, 0, 0, 0, 1):
                    return "GeoTIFF error: Invalid geotransform.", False

                # Display the CRS and geotransform
                # print("Coordinate Reference System (CRS):", src.crs)
                # print("Geotransform:", src.transform)

                return "GeoTIFF is properly georeferenced.", True

        except CRSError as e:
            return f"CRS error: {str(e)}",False
        except Exception as e:
            return f"Error opening the GeoTIFF: {str(e)}",False

    # This event filter defines how the remove image button should behave
    def eventFilter(self, source, event):
        if source == self.remove_button:
            if event.type() == QEvent.Type.HoverEnter:
                self.remove_button.setIcon(QIcon('feather/trash-2.svg'))
                self.remove_button.setStyleSheet("border:0px; border-radius:10px; background-color: #2d2d2d;")
            elif event.type() == QEvent.Type.HoverLeave:
                self.remove_button.setIcon(QIcon('feather/image.svg'))
                self.remove_button.setStyleSheet("border:0px; border-radius:10px; background-color: #202020;")
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.remove_button.setStyleSheet("border:0px; border-radius:10px; background-color: red;")
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.remove_button.setStyleSheet("border:0px; border-radius:10px;")
        return super().eventFilter(source, event)

