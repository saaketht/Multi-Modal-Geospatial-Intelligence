from component_file import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QDockWidget, QTabWidget, QListWidget,
    QPlainTextEdit, QFileDialog, QMessageBox, QGridLayout, QToolBar, QListWidgetItem, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QEvent, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QAction, QFontDatabase, QFontMetrics
from image_preview_dock import *
import os, sys, shutil

# This is the file explorer widget that will be hosted within a qdockwidget,specifically the "docks" variant
class file_explorer(QWidget):
    def __init__(self, image_preview_widget, parent=None):
        super().__init__(parent=parent)
        self.uploads_folder = os.path.join(os.getcwd(), "uploads")
        if not os.path.exists(self.uploads_folder):
            os.makedirs(self.uploads_folder)
        self.file_list = QListWidget()
        self.file_path_line_edit = LineEdit()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)

        self.image_preview_widget = image_preview_widget

        self.file_explorer_layout = QHBoxLayout()
        self.file_explorer_layout.setContentsMargins(0, 0, 0, 0)
        self.file_explorer_layout.setSpacing(5)
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

        self.open_folder_button = icon_button(initial_icon='feather/folder.svg', icon_square_len=22, button_square_len=34)
        self.open_folder_button.clicked.connect(self.open_file_dialog)

        self.add_file_button = icon_button(initial_icon='feather/plus.svg', icon_square_len=22, button_square_len=34)
        self.add_file_button.clicked.connect(self.add_file_to_list)

        self.file_explorer_layout.addWidget(self.open_folder_button)
        self.file_explorer_layout.addWidget(self.file_path_line_edit)
        self.file_explorer_layout.addWidget(self.add_file_button)

        self.file_explorer_vertical_layout = QVBoxLayout()
        self.file_explorer_vertical_layout.addLayout(self.file_explorer_layout)
        self.file_explorer_vertical_layout.addWidget(self.file_list)

        self.setLayout(self.file_explorer_vertical_layout)

        #return docks("Map File Explorer", file_explorer_widget, self)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PNG file", "", "PNG files (*.png)")
        if file_path:
            self.file_path_line_edit.setText(file_path)

    def add_file_to_list(self):
        file_path = self.file_path_line_edit.text()
        try:
            if file_path and os.path.isfile(file_path):
                base_name = os.path.basename(file_path)
                new_file_path = os.path.join(self.uploads_folder, base_name)

                file_root, file_extension = os.path.splitext(base_name)
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_name = f"{file_root}_{counter}{file_extension}"
                    new_file_path = os.path.join(self.uploads_folder, new_file_name)
                    counter += 1

                shutil.copy(file_path, new_file_path)

                custom_list_item_widget = CustomListItem(new_file_path, self.image_preview_widget, self.file_list)

                list_widget_item = QListWidgetItem(self.file_list)
                list_widget_item.setSizeHint(custom_list_item_widget.sizeHint())

                self.file_list.addItem(list_widget_item)
                self.file_list.setItemWidget(list_widget_item, custom_list_item_widget)
                custom_list_item_widget.remove_button.clicked.connect(lambda: self.remove_item(list_widget_item))

                custom_list_item_widget.list_widget_item = list_widget_item

                self.file_path_line_edit.clear()
            else:
                QMessageBox.information(self, "Error", "Invalid file path.")
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def remove_item(self, list_widget_item):
        try:
            row = self.file_list.row(list_widget_item)
            self.file_list.takeItem(row)
        except Exception as e:
            print(f"Error removing item: {e}")


class CustomListItem(QWidget):
    def __init__(self, text, image_preview_widget, list_widget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 11, 0, 11)
        layout.setSpacing(5)
        self.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)

        self.remove_button = icon_button(initial_icon='feather/image.svg', icon_square_len=22, button_square_len=34)

        self.eye_button = icon_button(initial_icon='feather/eye.svg', icon_square_len=22, button_square_len=34)

        self.world_button = icon_button(initial_icon='feather/globe.svg', icon_square_len=22, button_square_len=34)

        self.label = Label(text)
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)

        self.image_preview_widget = image_preview_widget
        self.list_widget = list_widget

        self.eye_button.clicked.connect(self.toggle_eye_icon)
        self.is_eye_icon = True

        #self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.installEventFilter(self)

        self.world_button.clicked.connect(self.toggle_image_preview)
        self.is_image_displayed = False

        layout.addWidget(self.remove_button)
        layout.addWidget(self.label, 1)
        # layout.addStretch()
        #layout.addWidget(self.eye_button)
        layout.addWidget(self.world_button)

    def preview_image(self):
        file_path = self.label.text()
        if os.path.isfile(file_path):
            self.image_preview_widget.setPixmap(QPixmap(file_path))
            self.image_preview_widget.currentImage = QPixmap(file_path)
            self.image_preview_widget.currentImagePath = file_path

    # def remove_item(self):
    #     try:
    #         row = self.list_widget.row(self.list_widget_item)
    #         self.list_widget.takeItem(row)
    #     except Exception as e:
    #         print(f"Error removing item: {e}")

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
            self.image_preview_widget.clear()
            self.world_button.setIcon(QIcon('feather/globe.svg'))
            self.image_preview_widget.currentImage = None
            self.image_preview_widget.currentImagePath = None
            self.is_image_displayed = False
        elif os.path.isfile(file_path):
            self.test =  QPixmap(file_path)
            self.image_preview_widget.setPixmap(self.test)
            self.image_preview_widget.currentImage = QPixmap(file_path)
            self.image_preview_widget.currentImagePath = file_path
            self.world_button.setIcon(QIcon('feather/x.svg'))
            self.is_image_displayed = True

    def toggle_eye_icon(self):
        if self.is_eye_icon:
            self.eye_button.setIcon(QIcon('feather/eye-off.svg'))
            self.is_eye_icon = False
        else:
            self.eye_button.setIcon(QIcon('feather/eye.svg'))
            self.is_eye_icon = True