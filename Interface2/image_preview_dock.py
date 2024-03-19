from component_file import *
from PyQt6.QtWidgets import (
    QLabel, QGridLayout
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QPoint,Qt
# class image_preview_widget(QWidget):
#     def __init__(self, text=None):
#         super().__init__()
#         # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # self.setScaledContents(True)
#         # #self.setMaximumSize(315, 317)
#         self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
#         self.currentImage = None
#         self.currentImagePath = None
#         self.p = QPixmap()
#     def setPixmap(self, p):
#         self.p = p
#         self.update()
#     def clear(self):
#         self.p = QPixmap()
#         self.update()
#
#     def paintEvent(self, event):
#         if not self.p.isNull():
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
#             painter.drawPixmap(self.rect(), self.p)
# class image_preview_widget(QWidget):
#     def __init__(self, text=None):
#         super().__init__()
#
#         self.currentImage = None
#         self.currentImagePath = None
#         self.h = self.height()
#         self.w = self.width()
#
#         self.layout = QGridLayout()
#         self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.layout.setContentsMargins(0,0,0,0)
#         self.layout.setHorizontalSpacing(0)
#         self.layout.setVerticalSpacing(0)
#
#         self.label = QLabel(text)
#         self.label.setScaledContents(True)
#         #self.label.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
#
#         self.layout.addWidget(self.label, 1, 1)
#         # self.layout.setRowStretch(0,0)
#         # self.layout.setRowStretch(2,0)
#         # self.layout.setColumnStretch(0,0)
#         # self.layout.setColumnStretch(2,0)
#
#         self.setLayout(self.layout)
#         #self.setMaximumSize(315, 317)
#
#     def setPixmap (self, p):
#         self.label.setPixmap(p)
#         h = p.height()
#         w = p.width()
#         self.label.resize(0.001*self.label.pixmap().size())
#         self.label.update()
#
#
#
#     def clear (self):
#         self.label.clear()

    # def resizeEvent(self, e):
    #     #.label.resize()


class image_preview_widget(QLabel):
    def __init__(self, text=None):
        super().__init__(text=text)

        self.currentImage = None
        self.currentImagePath = None
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.setMaximumSize(315, 317)

    def setPixmap2(self, p):
        h = p.height()
        w = p.width()
        ratio = h/w
        self.setPixmap(p)
        self.resize(0.1 * QSize(w, h))
        self.update()


        # labelRatio = self.height()/self.width()
        # if labelRatio>ratio:
        #     self.resize(int(self.width()), int(self.width()*ratio))
        # elif labelRatio <= ratio:
        #     self.resize(int(self.height()/ratio), int(self.height()))

    # def resizeEvent(self, e):
    #     h = self.pixmap()height()
    #     w = p.width()
    #     ratio = h/w
    #     labelRatio = self.height()/self.width()
    #     if labelRatio>ratio:
    #         self.resize(int(self.width()), int(self.width()*ratio))
    #     elif labelRatio <= ratio:
    #         self.resize(int(self.height()/ratio), int(self.height()))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QPalette, QPainter, QAction
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QFileDialog, QApplication


class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.ColorRole.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    def open(self):
        options = QFileDialog.Option
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...")
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.open)

        self.printAct = QAction("&Print...")
        self.printAct.setShortcut("Ctrl+P")
        self.printAct.setEnabled(False)
        self.printAct.triggered.connect(self.print_)


        self.exitAct = QAction("E&xit")
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.close)

        self.zoomInAct = QAction("Zoom &In (25%)")
        self.zoomInAct.setShortcut("Ctrl++")
        self.zoomInAct.setEnabled(False)
        self.zoomInAct.triggered.connect(self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (25%)")
        self.zoomOutAct.setShortcut("Ctrl+-")
        self.zoomOutAct.setEnabled(False)
        self.zoomOutAct.triggered.connect(self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size")
        self.normalSizeAct.setShortcut("Ctrl+S")
        self.normalSizeAct.setEnabled(False)
        self.normalSizeAct.triggered.connect(self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window")
        self.fitToWindowAct.setEnabled(False)
        self.fitToWindowAct.setCheckable(True)
        self.fitToWindowAct.setShortcut("Ctrl+F")
        self.fitToWindowAct.triggered.connect(self.fitToWindow)

        self.aboutAct = QAction("&About")
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QAction("About &Qt")
        self.aboutQtAct.triggered.connect(QApplication.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec())
    # TODO QScrollArea support mouse
    # base on https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
    #
    # if you need Two Image Synchronous Scrolling in the window by PyQt5 and Python 3
    # please visit https://gist.github.com/acbetter/e7d0c600fdc0865f4b0ee05a17b858f2