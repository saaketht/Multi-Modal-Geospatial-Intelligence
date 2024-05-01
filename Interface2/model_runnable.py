from PyQt6.QtCore import QRunnable, pyqtSignal, QObject,Qt
from send import send_and_receive
from replicate.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv('REPLICATE_API_KEY')

class ModelSignals(QObject):
    response_received = pyqtSignal(str)
    isStream = pyqtSignal(bool)


class ModelRunnable(QRunnable):
    def __init__(self, prompt, image_path, history_dict,chat_scroll_layout, chat_model_message_widget):
        super().__init__()
        self.prompt = prompt
        self.image_path = image_path
        self.history_dict = history_dict
        self.signals = ModelSignals()
        self.top_p = 1
        self.max_tokens = 256
        self.temperature = 0.2
        self.chat_scroll_layout = chat_scroll_layout
        self.chat_model_message_widget=chat_model_message_widget

    def run(self):
        replicate = Client(api_token=api_token)
        image = open(self.image_path, "rb")
        model_message_text= ""

        input = {
                    "image": image,
                    "top_p": self.top_p,
                    "prompt": self.prompt,
                    "history": self.history_dict,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }

        try:
            i = 0
            for event in replicate.stream(
                "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
                # "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
                input=input,
            ):
                model_message_text+= str(event)
                print(str(event), end="")
                if str(event).strip() == "GEOINT:":
                    print("Post the empty model message")
                    self.chat_scroll_layout.addWidget(self.chat_model_message_widget,
                                                      alignment=Qt.AlignmentFlag.AlignTop)
                    i+=1
                    self.signals.isStream.emit(True)
                    continue
                elif(i==0 and not model_message_text.startswith("GEOINT:")):
                    print("Post the empty model message2")
                    self.chat_scroll_layout.addWidget(self.chat_model_message_widget,
                                                      alignment=Qt.AlignmentFlag.AlignTop)
                    i+= 1
                    self.signals.isStream.emit(True)
                    continue #possible redundancy
                elif i>0 and model_message_text.startswith("GEOINT:"):
                    i+=1
                    stream = str(model_message_text)[len("GEOINT:"):].strip()
                    self.chat_model_message_widget.message_content.setText(stream)
                elif i>0 and not model_message_text.startswith("GEOINT:"):
                    self.chat_model_message_widget.message_content.setText(str(model_message_text))
                    i+=1


            if model_message_text.startswith("GEOINT:"):
                model_message_text = model_message_text[len("GEOINT:"):].strip()
        except:
            self.signals.isStream.emit(False)
            print("except")
            model_output= replicate.run(
                "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
                # "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
                input=input
            )
            for item in model_output:
                model_message_text += item

            if model_message_text.startswith("GEOINT:"):
                model_message_text = model_message_text[len("GEOINT:"):].strip()

            print(model_message_text)
            self.chat_model_message_widget.message_content.setText(model_message_text)
            self.chat_scroll_layout.addWidget(self.chat_model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

            # self.chat_model_message_widget.content_message.setText(model_message_text)

            # model_output = send_and_receive(self.prompt, self.image_path, self.history_dict)
            # for item in model_output:
            #     model_message_text += item


        self.signals.response_received.emit(model_message_text)
