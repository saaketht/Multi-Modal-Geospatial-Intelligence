
# This file contains widgets related to both the Current Image Window and the
# Image Preview Widget within the File Explorer Window

from component_file import *
from PyQt6.QtWidgets import (
    QLabel,QListWidgetItem
)
from PyQt6.QtCore import Qt

# This widget is a custom widget that allows users to display an image that keeps
# the aspect ratio of the original image without rescaling the original image every time
# a resize event is called, this way we avoid interpolation algorithms that diminish the quality of
# the original image.
class image_preview_widget(QWidget):
    # Signal returns path name, index of widget to toggle off
    toggleOffFileExplorerButton = pyqtSignal(QListWidgetItem)
    # Constructor
    def __init__(self, text=None):
        # Call Parent Constructor
        super().__init__()

        # This QLabel, purposely spelled incorrectly, is used to display the image
        self.lable = QLabel()
        self.lable.placeholder = text  # The label's placeholder while an image is not being viewed
        self.lable.setText(self.lable.placeholder)  # Set Placeholder
        self.lable.setScaledContents(True)  # Make contents scaled
        self.lable.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Make the contents align center

        # Attributes
        self.list_widget_item_index = -1  # Holds the List widget item, NOT the index, its functionality changed
        self.currentImagePath = ""  # Holds the current image path
        self.currentImage = None  # Holds the QPixmap of the image
        self.currentImageHeight = 0  # Holds the image's original height
        self.currentImageWidth = 0  # Holds the image's original width
        self.is_an_image = False  # Bool val of whether the label is an image

        # Set the minimum size of the Label and widget to 0, 0
        self.setMinimumSize(0, 0)
        self.lable.setMinimumSize(0, 0)

        # Set size policy of label and widget
        # THIS PART IS IMPORTANT
        # We se the size policy of the widget to ignored to take all the space of the window this widget
        # is called into, we then set the size policy of the label to fixed to avoid rescaling via interpolation
        self.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
        self.lable.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        # Set stylesheet for label
        self.lable.setStyleSheet("color: #FFFFFF;")

        # Set stylesheet for widget
        self.setStyleSheet('''
        QWidget
        {
            background: transparent;
            border: transparent;
        }
        ''')

        # The widget consists of two layouts, a vertical and horizontal layout
        # these layouts will be nested to host the label in the middle.
        self.Layout = QVBoxLayout()
        self.Layout.setSpacing(0)
        self.Layout.setContentsMargins(0,0,0,0)

        # Add the label to the vertical layout
        self.Layout.addWidget(self.lable, Qt.AlignmentFlag.AlignCenter)

        # The super layout is the outer layout and that is the Horizontal layout
        self.superLayout = QHBoxLayout()
        self.superLayout.setSpacing(0)
        self.superLayout.setContentsMargins(0,0,0,0)

        # add the vertical layout to the horizontal layout
        self.superLayout.addLayout(self.Layout)

        # Set the horizontal layout to the widget
        self.setLayout(self.superLayout)

    # Instead of overriding the setPixmap functions, we create a new variant of the
    # setPixmap called setPixmap2 that will populate the attributes with the image's
    # values
    def setPixmap2(self, pixmap):
        # Update attributes
        self.currentImage = pixmap  # Set pixmap to self.currentImage
        self.currentImageHeight = pixmap.height()  # Set the original height of pixmap
        self.currentImageWidth = pixmap.width()  # Set the original width of pixmap

        # Set label's pixmap
        self.lable.setPixmap(pixmap)

        # Get current width and height of the widget
        current_width = self.size().width()
        current_height = self.size().height()

        # Calculate the h to w ratio of widget, initialized to 0
        current_h_w_ratio = 0
        # If the width does not equal 0 to avoid divide by 0 error
        if current_width != 0:
            # Update h to w ratio
            current_h_w_ratio = current_height / current_width

        # Store height and width of the image's original size
        # as local variables
        height = self.currentImageHeight
        width = self.currentImageWidth

        # Calculate the h to w ratio of original image, initialized to 0
        image_h_w_ratio = 0
        # If the width does not equal 0 to avoid divide by 0 error
        if width != 0:
            # Update h to w ratio
            image_h_w_ratio = height / width

        # The following statements sets the image to the size of the widget while keeping the
        # image's original aspect ratio

        # if the widget's height is smaller than 100px or
        # if the widget's width is smaller than the width of the image if scaled to a height of 100px
        # then set the max height of the image to 100px
        if current_height <= 100 or current_width <= self.heightForWidth2(height, width, 100):
            # Get the new width of the image based off its aspect ratio while using the height of widget
            new_width = self.heightForWidth2(height, width, 100)

            # Resize the label to the recalculated dimensions
            self.lable.setFixedSize(new_width, 100)

        # if the ratio of the image is bigger than the ratio of the widget, in other words if the
        # height of the image is bigger than the height of the widget if they were scaled to the same width,
        # then resize the image's height to the widget's height and get a smaller width to fit within the widget's
        # width.
        elif image_h_w_ratio > current_h_w_ratio:
            # Get the new width of the image based off its aspect ratio while using the height of widget
            new_width = self.heightForWidth2(height, width, current_height)

            # Resize the label to the recalculated dimensions
            self.lable.setFixedSize(new_width, current_height)

        # if the ratio of the image is smaller than the ratio of the widget, in other words if the
        # height of the image is smaller than the height of the widget if they were scaled to the same width,
        # then resize the image's width to the widget's width and get a smaller height to fit within the widget's
        # height.
        elif image_h_w_ratio <= current_h_w_ratio:
            # Get the new height of the image based off its aspect ratio while using the width of widget
            new_height = self.widthForHeight2(height, width, current_width)

            # Resize the label to the recalculated dimensions
            self.lable.setFixedSize(current_width, new_height)

    # This function takes the image's original height and width to get the w/h ratio to calculate the
    # new width of the image given a new height.
    def heightForWidth2(self, initial_height, initial_width, height):
        # if the initial height is zero return 0 because we cannot divide by 0
        if initial_height == 0:
            return 0

        # Calculate the w/h aspect ratio
        ratio = initial_width/initial_height

        # return the rounded integer of the ratio multiplied by the desired height
        return int(ratio*height)

    # This function takes the image's original height and width to get the h/w ratio to calculate the
    # new height of the image given a new width.
    def widthForHeight2(self, initial_height, initial_width, width):
        # if the initial width is zero return 0 because we cannot divide by 0
        if initial_width == 0:
            return 0
        # Calculate the h/w aspect ratio
        ratio = initial_height/initial_width

        # return the rounded integer of the ratio multiplied by the desired width
        return int(ratio*width)

    # Here we override the resize event to resize the label within the widget to maintain the aspect ratio
    # of the original image
    def resizeEvent(self, e):
        # Only resize the label if the widget is hosting an image
        if self.is_an_image:
            # Get event's width and height of the widget
            event_width = e.size().width()
            event_height = e.size().height()

            # Calculate the h to w ratio of widget, initialized to 0
            event_h_w_ratio = 0

            # If the width does not equal 0 to avoid divide by 0 error
            if event_width != 0:
                # Update h to w ratio
                event_h_w_ratio = event_height / event_width

            # Store height and width of the image's original size
            # as local variables
            height = self.currentImageHeight
            width = self.currentImageWidth

            # Calculate the h to w ratio of image, initialized to 0
            image_h_w_ratio = 0

            # If the width does not equal 0 to avoid divide by 0 error
            if width != 0:
                image_h_w_ratio = height / width

            # if the widget's height is smaller than 100px or
            # if the widget's width is smaller than the width of the image if scaled to a height of 100px
            # then set the max height of the image to 100px
            if event_height<=100 or event_width<=self.heightForWidth2(height, width, 100):
                # Get the new width of the image based off its aspect ratio while using the height of widget
                new_width = self.heightForWidth2(height, width, 100)

                # Resize the label to the recalculated dimensions
                self.lable.setFixedSize(new_width, 100)

            # if the ratio of the image is bigger than the ratio of the widget, in other words if the
            # height of the image is bigger than the height of the widget if they were scaled to the same width,
            # then resize the image's height to the widget's height and get a smaller width to fit within the widget's
            # width.
            elif image_h_w_ratio > event_h_w_ratio:
                # Get the new width of the image based off its aspect ratio while using the height of widget
                new_width = self.heightForWidth2(height, width, event_height)

                # Resize the label to the recalculated dimensions
                self.lable.setFixedSize(new_width, event_height)

            # if the ratio of the image is smaller than the ratio of the widget, in other words if the
            # height of the image is smaller than the height of the widget if they were scaled to the same width,
            # then resize the image's width to the widget's width and get a smaller height to fit within the widget's
            # height.
            elif image_h_w_ratio <= event_h_w_ratio:
                # Get the new height of the image based off its aspect ratio while using the width of widget
                new_height = self.widthForHeight2(height, width, event_width)

                # Resize the label to the recalculated dimensions
                self.lable.setFixedSize(event_width, new_height)

        # Call the Parent resize event
        super().resizeEvent(e)

# The following code is a sample image viewer from Qt,

# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QImage, QPixmap, QPalette, QPainter, QAction
# from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
# from PyQt6.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QFileDialog, QApplication
#
#
# class QImageViewer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.printer = QPrinter()
#         self.scaleFactor = 0.0
#
#         self.imageLabel = QLabel()
#         self.imageLabel.setBackgroundRole(QPalette.ColorRole.Base)
#         self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
#         self.imageLabel.setScaledContents(True)
#
#         self.scrollArea = QScrollArea()
#         self.scrollArea.setBackgroundRole(QPalette.ColorRole.Dark)
#         self.scrollArea.setWidget(self.imageLabel)
#         self.scrollArea.setVisible(False)
#
#         self.testSuper = QWidget()
#         self.testLayout =  QHBoxLayout()
#         self.testLayout.setSpacing(0)
#         self.testLayout.setContentsMargins(0,0,0,0)
#         self.testSuper.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
#
#         # self.test = QLabel()
#         # tet = QPixmap("/Users/basmattiejamaludin/Desktop/Images/test.jpg")
#         # tet2= tet.scaled(500,500)
#         # self.test.setPixmap(tet2)
#         # self.test.setBaseSize(100,100)
#         # # self.test.resize(100,100)
#         #/Users/basmattiejamaludin/Desktop/Images/test.jpg
#         #/Users/basmattiejamaludin/Desktop/demo1.jpg
#         self.test = image_preview_widget()
#
#         #/Users/basmattiejamaludin/Documents/Notes/COP4020_Functional_Programming/JQuery_Assignment/newyork1.jpg
#         #/Users/basmattiejamaludin/Desktop/demo1.jpg
#         self.test.setPixmap2(QPixmap("/Users/basmattiejamaludin/Desktop/demo1.jpg"))
#         self.test.is_an_image =True
#         self.test.currentImagePath = "/Users/basmattiejamaludin/Desktop/demo1.jpg"
#
#
#         self.testLayout.addWidget(self.test,Qt.AlignmentFlag.AlignHCenter)
#         self.testSuper.setLayout(self.testLayout)
#
#         self.setCentralWidget(self.test)
#
#         # self.setCentralWidget(self.scrollArea)
#
#         self.createActions()
#         self.createMenus()
#
#         self.setWindowTitle("Image Viewer")
#         self.resize(800, 600)
#
#     def open(self):
#         options = QFileDialog.Option
#         # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
#         fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
#                                                   'Images (*.png *.jpeg *.jpg *.bmp *.gif)')
#         if fileName:
#             image = QImage(fileName)
#             if image.isNull():
#                 QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
#                 return
#
#             self.imageLabel.setPixmap(QPixmap.fromImage(image))
#             self.scaleFactor = 1.0
#
#             self.scrollArea.setVisible(True)
#             self.printAct.setEnabled(True)
#             self.fitToWindowAct.setEnabled(True)
#             self.updateActions()
#
#             if not self.fitToWindowAct.isChecked():
#                 self.imageLabel.adjustSize()
#
#     def print_(self):
#         dialog = QPrintDialog(self.printer, self)
#         if dialog.exec():
#             painter = QPainter(self.printer)
#             rect = painter.viewport()
#             size = self.imageLabel.pixmap().size()
#             size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
#             painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
#             painter.setWindow(self.imageLabel.pixmap().rect())
#             painter.drawPixmap(0, 0, self.imageLabel.pixmap())
#
#     def zoomIn(self):
#         self.scaleImage(1.25)
#
#     def zoomOut(self):
#         self.scaleImage(0.8)
#
#     def normalSize(self):
#         self.imageLabel.adjustSize()
#         self.scaleFactor = 1.0
#
#     def fitToWindow(self):
#         fitToWindow = self.fitToWindowAct.isChecked()
#         self.scrollArea.setWidgetResizable(fitToWindow)
#         if not fitToWindow:
#             self.normalSize()
#
#         self.updateActions()
#
#     def about(self):
#         QMessageBox.about(self, "About Image Viewer",
#                           "<p>The <b>Image Viewer</b> example shows how to combine "
#                           "QLabel and QScrollArea to display an image. QLabel is "
#                           "typically used for displaying text, but it can also display "
#                           "an image. QScrollArea provides a scrolling view around "
#                           "another widget. If the child widget exceeds the size of the "
#                           "frame, QScrollArea automatically provides scroll bars.</p>"
#                           "<p>The example demonstrates how QLabel's ability to scale "
#                           "its contents (QLabel.scaledContents), and QScrollArea's "
#                           "ability to automatically resize its contents "
#                           "(QScrollArea.widgetResizable), can be used to implement "
#                           "zooming and scaling features.</p>"
#                           "<p>In addition the example shows how to use QPainter to "
#                           "print an image.</p>")
#
#     def createActions(self):
#         self.openAct = QAction("&Open...")
#         self.openAct.setShortcut("Ctrl+O")
#         self.openAct.triggered.connect(self.open)
#
#         self.printAct = QAction("&Print...")
#         self.printAct.setShortcut("Ctrl+P")
#         self.printAct.setEnabled(False)
#         self.printAct.triggered.connect(self.print_)
#
#
#         self.exitAct = QAction("E&xit")
#         self.exitAct.setShortcut("Ctrl+Q")
#         self.exitAct.triggered.connect(self.close)
#
#         self.zoomInAct = QAction("Zoom &In (25%)")
#         self.zoomInAct.setShortcut("Ctrl++")
#         self.zoomInAct.setEnabled(False)
#         self.zoomInAct.triggered.connect(self.zoomIn)
#
#         self.zoomOutAct = QAction("Zoom &Out (25%)")
#         self.zoomOutAct.setShortcut("Ctrl+-")
#         self.zoomOutAct.setEnabled(False)
#         self.zoomOutAct.triggered.connect(self.zoomOut)
#
#         self.normalSizeAct = QAction("&Normal Size")
#         self.normalSizeAct.setShortcut("Ctrl+S")
#         self.normalSizeAct.setEnabled(False)
#         self.normalSizeAct.triggered.connect(self.normalSize)
#
#         self.fitToWindowAct = QAction("&Fit to Window")
#         self.fitToWindowAct.setEnabled(False)
#         self.fitToWindowAct.setCheckable(True)
#         self.fitToWindowAct.setShortcut("Ctrl+F")
#         self.fitToWindowAct.triggered.connect(self.fitToWindow)
#
#         self.aboutAct = QAction("&About")
#         self.aboutAct.triggered.connect(self.about)
#
#         self.aboutQtAct = QAction("About &Qt")
#         self.aboutQtAct.triggered.connect(QApplication.aboutQt)
#
#     def createMenus(self):
#         self.fileMenu = QMenu("&File", self)
#         self.fileMenu.addAction(self.openAct)
#         self.fileMenu.addAction(self.printAct)
#         self.fileMenu.addSeparator()
#         self.fileMenu.addAction(self.exitAct)
#
#         self.viewMenu = QMenu("&View", self)
#         self.viewMenu.addAction(self.zoomInAct)
#         self.viewMenu.addAction(self.zoomOutAct)
#         self.viewMenu.addAction(self.normalSizeAct)
#         self.viewMenu.addSeparator()
#         self.viewMenu.addAction(self.fitToWindowAct)
#
#         self.helpMenu = QMenu("&Help", self)
#         self.helpMenu.addAction(self.aboutAct)
#         self.helpMenu.addAction(self.aboutQtAct)
#
#         self.menuBar().addMenu(self.fileMenu)
#         self.menuBar().addMenu(self.viewMenu)
#         self.menuBar().addMenu(self.helpMenu)
#
#     def updateActions(self):
#         self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
#         self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
#         self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
#
#     def scaleImage(self, factor):
#         self.scaleFactor *= factor
#         self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
#
#         self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
#         self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
#
#         self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
#         self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
#
#     def adjustScrollBar(self, scrollBar, factor):
#         scrollBar.setValue(int(factor * scrollBar.value()
#                                + ((factor - 1) * scrollBar.pageStep() / 2)))
#
#
# if __name__ == '__main__':
#     import sys
#     from PyQt6.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#     app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     imageViewer = QImageViewer()
#     imageViewer.show()
#     sys.exit(app.exec())
#     # TODO QScrollArea support mouse
#     # base on https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
#     #
#     # if you need Two Image Synchronous Scrolling in the window by PyQt5 and Python 3
#     # please visit https://gist.github.com/acbetter/e7d0c600fdc0865f4b0ee05a17b858f2