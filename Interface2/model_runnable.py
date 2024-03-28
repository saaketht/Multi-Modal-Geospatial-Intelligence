from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from send import send_and_receive


class ModelSignals(QObject):
    response_received = pyqtSignal(str)


class ModelRunnable(QRunnable):
    def __init__(self, prompt, image_path, history_dict):
        super().__init__()
        self.prompt = prompt
        self.image_path = image_path
        self.history_dict = history_dict
        self.signals = ModelSignals()

    def run(self):
        model_output = send_and_receive(self.prompt, self.image_path, self.history_dict)
        model_message_text = ""
        for item in model_output:
            model_message_text += item
        self.signals.response_received.emit(model_message_text)
