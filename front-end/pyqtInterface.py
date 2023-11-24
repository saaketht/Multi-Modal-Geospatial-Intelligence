import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon


class ParametersWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.main_layout = QVBoxLayout(self)
        self.setFixedSize(QSize(250, 220))

        # Create a button to toggle the collapsible content
        self.toggle_button = QPushButton("Toggle", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.main_layout.addWidget(self.toggle_button)

        # Create a frame for the collapsible content
        self.collapsible_frame = QFrame(self)
        self.collapsible_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.collapsible_layout = QVBoxLayout(self.collapsible_frame)

        # Add widgets for temperature, top P, and max output tokens
        self.temperature_label = QLabel("Temperature:", self.collapsible_frame)
        self.temperature_input = QLineEdit(self.collapsible_frame)
        self.temperature_input.setFixedSize(QSize(200,20))
        self.temperature_input.setStyleSheet("background-color:#44475A; color: white; font-size: 10px;")
        self.collapsible_layout.addWidget(self.temperature_label)
        self.collapsible_layout.addWidget(self.temperature_input)

        self.top_p_label = QLabel("Top P:", self.collapsible_frame)
        self.top_p_input = QLineEdit(self.collapsible_frame)
        self.top_p_input.setFixedSize(QSize(200,20))
        self.top_p_input.setStyleSheet("background-color:#44475A; color: white; font-size: 10px;")
        self.collapsible_layout.addWidget(self.top_p_label)
        self.collapsible_layout.addWidget(self.top_p_input)

        self.max_tokens_label = QLabel("Max Output Tokens:", self.collapsible_frame)
        self.max_tokens_input = QLineEdit(self.collapsible_frame)
        self.max_tokens_input.setFixedSize(QSize(200,20))
        self.max_tokens_input.setStyleSheet("background-color:#44475A; color: white; font-size: 10px;")
        self.collapsible_layout.addWidget(self.max_tokens_label)
        self.collapsible_layout.addWidget(self.max_tokens_input)

        # Initially hide the collapsible content
        self.collapsible_frame.setVisible(False)
        self.main_layout.addWidget(self.collapsible_frame)

    def toggle_content(self):
        # Toggle the visibility of the collapsible content
        self.collapsible_frame.setVisible(self.toggle_button.isChecked())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Mockup")
        self.setFixedSize(QSize(1400, 750))
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
        #chat_frame.setStyleSheet("border-radius: 20px;")
        chat_layout = QHBoxLayout(chat_frame)
        chat_layout.setContentsMargins(5,5,5,5)
        # chat_display = QTextEdit()
        # chat_display.setStyleSheet("background-color: #44475A; border-radius: 20px; color: white;")
        #need to make the placeholder text have left padding
        chat_input = QLineEdit()
        chat_input.setPlaceholderText("Enter text and press ENTER")
        chat_input.setStyleSheet("border-radius: 10px; background-color: #44475A; color: white;")
        chat_input.setFixedSize(QSize(600, 40))
        send_button = QPushButton("Send")
        send_button.setFixedSize(QSize(90,40 ))
        send_button.setStyleSheet("background-color: #44475A; color: white;  border-radius: 10px")
        # chat_layout.addWidget(chat_display, 75)
        chat_layout.addWidget(chat_input, 20)
        chat_layout.addWidget(send_button, 5)
        chat_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        chat_frame.setFixedSize(QSize(960, 80))

        examples_frame = QFrame()
        examples_frame.setStyleSheet("background-color: #44475A; border-radius: 10px;")
        examples_layout = QHBoxLayout(examples_frame)
        examples_label = QLabel("Examples!")
        examples_label.setStyleSheet("color: white; font-size: 16px; padding: 5px;")
        examples_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        examples_layout.addWidget(examples_label)

        
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
        main_layout.addWidget(chat_frame, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(examples_frame, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(footer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        #DO NOT DELETE IN CASE WE NEED IT LATER
        # parameters_widget = ParametersWidget()
        # main_layout.addWidget(parameters_widget)

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
