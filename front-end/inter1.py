import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Mockup")
        self.setFixedSize(QSize(1009, 684))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282A36;
            }
            QLabel, QPushButton, QTextEdit, QLineEdit {
                font-family: Arial;
                color: #F8F8F2;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        #drop image box is header_frame
        self.header_frame = QFrame()
        self.header_frame.setFixedSize(QSize(460, 245)) 
        self.header_frame.setStyleSheet("""
            QFrame {
                background-color: #44475A;
                border-radius: 10px;
            }
        """)
        #need to make upload label centered vertically in the header_frame
        self.header_layout = QVBoxLayout(self.header_frame)
        self.upload_label = QLabel("Drop Image Here<br><br>-or-<br><br>Click to Upload")
        self.upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_label.setStyleSheet("color: white; font-size: 20px;")
        self.image_label = QLabel()  # This label will hold the image
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self.upload_label)
        self.header_layout.addWidget(self.image_label)
        self.header_frame.setAcceptDrops(True)

        #chat_frame is message send box
        #need to remove the background box and make send message button different color
        chat_frame = QFrame()
        #removed to try to fix it to look like what we have
        #chat_frame.setStyleSheet("background-color: #6272A4; border-radius: 10px;")
        chat_frame.setStyleSheet("background-color: #6272A4; border-radius: 20px;")
        chat_layout = QHBoxLayout(chat_frame)
        # chat_display = QTextEdit()
        # chat_display.setStyleSheet("background-color: #44475A; border-radius: 20px; color: white;")
        chat_input = QLineEdit()
        chat_input.setPlaceholderText("Enter text and press ENTER")
        chat_input.setStyleSheet("background-color: #44475A; color: white;")
        chat_input.setFixedSize(QSize(960, 60))
        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: #50FA7B; color: #282A36;  border-radius: 50px;")
        # chat_layout.addWidget(chat_display, 75)
        chat_layout.addWidget(chat_input, 20)
        chat_layout.addWidget(send_button, 5)
        chat_frame.setFixedSize(QSize(960, 60))

        examples_frame = QFrame()
        examples_frame.setStyleSheet("background-color: #44475A; border-radius: 10px;")
        examples_layout = QHBoxLayout(examples_frame)
        examples_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        example_images = ['example1.png', 'example2.png', 'example3.png']
        for img_path in example_images:
            pixmap = QPixmap(img_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio))
            examples_layout.addWidget(label)
        examples_frame.setFixedSize(QSize(960, 120))


        footer_label = QLabel("By using this service, users are required to agree to the following terms: ...")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("""
            QLabel {
                background-color: #6272A4;
                color: white;
                font-size: 12px;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        footer_label.setFixedSize(QSize(960, 40))

        main_layout.addWidget(self.header_frame, alignment=Qt.AlignmentFlag.AlignLeft) 
        main_layout.addWidget(chat_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(examples_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        self.header_frame.mousePressEvent = self.upload_image

    def upload_image(self, event):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(960, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
            self.upload_label.setText('')

def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
        event.acceptProposedAction()

def dropEvent(self, event):
    if event.mimeData().hasUrls():
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.set_image(file_path)
        event.acceptProposedAction()

    def set_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(960, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.upload_label.setText('')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
