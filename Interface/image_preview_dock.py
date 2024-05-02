from component_file import *
from PyQt6.QtWidgets import (
    QLabel, QGridLayout,QListWidgetItem
)
from PyQt6.QtGui import QPixmap, QPainter,QImage
from PyQt6.QtCore import QPoint,Qt, QModelIndex


class image_preview_widget(QWidget):
    # signal returns path name, index of widget to toggle off
    toggleOffFileExplorerButton = pyqtSignal(QListWidgetItem)
    def __init__(self, text=None):
        super().__init__()
        self.lable = QLabel()
        self.lable.placeholder = text
        self.lable.setText(self.lable.placeholder)
        self.list_widget_item_index = -1
        self.currentImagePath = ""
        self.currentImage = None
        self.currentImageHeight = 0
        self.currentImageWidth = 0
        self.setMinimumSize(0,0)
        self.lable.setMinimumSize(0,0)
        self.is_an_image = False
        self.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
        self.lable.setScaledContents(True)
        self.lable.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lable.setStyleSheet("color: #FFFFFF;")
        self.setStyleSheet('''
        QWidget
        {
            background: transparent;
            border: transparent;
        }
        ''')
        # self.lable.setFixedSize(100,100)

        self.Layout = QVBoxLayout()
        self.Layout.addWidget(self.lable, Qt.AlignmentFlag.AlignCenter)
        self.Layout.setContentsMargins(0,0,0,0)
        self.Layout.setSpacing(0)
        self.superLayout = QHBoxLayout()
        self.superLayout.setSpacing(0)
        self.superLayout.setContentsMargins(0,0,0,0)
        self.superLayout.addLayout(self.Layout)
        self.setLayout(self.superLayout)

        # self.setMaximumSize(315, 317)

    def setPixmap2(self, pixmap):
        self.currentImage = pixmap
        self.currentImageHeight = pixmap.height()
        self.currentImageWidth = pixmap.width()

        self.lable.setPixmap(pixmap)

        current_width = self.size().width()
        current_height = self.size().height()
        current_h_w_ratio = 0
        if (current_width != 0):
            current_h_w_ratio = current_height / current_width

        height = self.currentImageHeight
        width = self.currentImageWidth
        image_h_w_ratio = 0
        if (width != 0):
            image_h_w_ratio = height / width

        if image_h_w_ratio > current_h_w_ratio:
            new_width = self.heightForWidth2(height, width, current_height)
            self.lable.setFixedSize(new_width, current_height)
        elif image_h_w_ratio <= current_h_w_ratio:
            new_height = self.widthForHeight2(height, width, current_width)
            self.lable.setFixedSize(current_width, new_height)

    def heightForWidth2(self, initial_height, initial_width,height):
        if initial_width == 0:
            return 0
        ratio = initial_width/initial_height
        return int(ratio*height)

    def widthForHeight2(self, initial_height, initial_width,width):
        if initial_width == 0:
            return 0
        ratio = initial_height/initial_width
        return int(ratio*width)

    def resizeEvent(self, e):
        if (self.is_an_image):
            # image_pixmap = QPixmap(self.currentImagePath)
            event_width = e.size().width()
            event_height = e.size().height()
            event_h_w_ratio = 0
            if (event_width != 0):
                event_h_w_ratio = event_height / event_width

            height = self.currentImageHeight
            width = self.currentImageWidth
            image_h_w_ratio = 0
            if (width != 0):
                image_h_w_ratio = height / width


            if(event_height<=100 or event_width<=self.heightForWidth2(height, width, 100)):
                new_width = self.heightForWidth2(height, width, 100)
                self.lable.setFixedSize(new_width, 100)

            elif image_h_w_ratio > event_h_w_ratio:

                new_width = self.heightForWidth2(height, width, event_height)
                self.lable.setFixedSize(new_width, event_height)

            elif image_h_w_ratio <= event_h_w_ratio:

                new_height = self.widthForHeight2(height, width, event_width)
                self.lable.setFixedSize(event_width, new_height)


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