
# This file hosts the api in a QRunnable object for receiving the model's response

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject,Qt
from replicate.client import Client
import os
from dotenv import load_dotenv

# Get the api key from the .env file
load_dotenv()
api_token = os.getenv('REPLICATE_API_KEY')

# This QObject hosts the signals for the QRunnable class
class ModelSignals(QObject):
    response_received = pyqtSignal(str)
    isStream = pyqtSignal(bool)

# This class will use the Replicate API module to fetch a response from the model
class ModelRunnable(QRunnable):
    # Constructor, parameters include:
    # prompt :  the user's prompt
    # image_path :  the path to the image that the user is currently querying
    # history_dic :  the array of strings alternating between the user's and model's previous messages
    # chat_scroll_layout : layout for the list of messages
    # chat_model_message_widget :  the model's widget to add to the layout
    def __init__(self, prompt, image_path, history_dict,chat_scroll_layout, chat_model_message_widget):
        # Call Parent Constructor
        super().__init__()
        # Set parameters passed to constructor to local variables
        self.prompt = prompt
        self.image_path = image_path
        self.history_dict = history_dict
        self.chat_scroll_layout = chat_scroll_layout
        self.chat_model_message_widget=chat_model_message_widget

        # Create an instance of the ModelSignals QObject to emit signals
        # when necessary
        self.signals = ModelSignals()

        # Model parameters
        self.top_p = 1
        self.max_tokens = 256
        self.temperature = 0.2

    # Run method for threading
    def run(self):
        # Get connection using api key
        replicate = Client(api_token=api_token)

        # Read image path
        image = open(self.image_path, "rb")

        # Initialize empty message text from model, this will be updated when the model responds
        model_message_text= ""

        # Prepare input schema for model
        input = {
                    "image": image,
                    "top_p": self.top_p,
                    "prompt": self.prompt,
                    "history": self.history_dict,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }

        # Try and catch for errors when streaming
        try:
            # Variable i keeps track of message location during streaming
            i = 0

            # Get the streamed input from model, this will get every word or a few words generated at a time during
            # the prediction
            for event in replicate.stream(
                # "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
                "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
                input=input,
            ):
                # Append the word/words to the model_message_text string
                model_message_text += str(event)
                print(str(event), end="")

                # If the first responded text is  the model's name, post the widget to the layout to show that a
                # connection is made
                if str(event).strip() == "GEOINT:":
                    # Post widget to layout
                    self.chat_scroll_layout.addWidget(self.chat_model_message_widget,
                                                      alignment=Qt.AlignmentFlag.AlignTop)

                    # Update the message location variable
                    i += 1

                    # Emit isStream signal of val True, this will change the loading animation to blue notifying
                    # that the streaming feature has been enabled
                    self.signals.isStream.emit(True)

                    # Go to next word/words
                    continue

                # If the first responded text is NOT the model's name, but it is the first set of
                # text, post the widget to the layout to show that a connection is made
                elif i == 0 and not model_message_text.startswith("GEOINT:"):
                    # Post widget to layout
                    self.chat_scroll_layout.addWidget(self.chat_model_message_widget,
                                                      alignment=Qt.AlignmentFlag.AlignTop)

                    # Update the message location variable
                    i += 1

                    # Emit isStream signal of val True, this will change the loading animation to blue notifying
                    # that the streaming feature has been enabled
                    self.signals.isStream.emit(True)

                    # Go to next word/words
                    continue

                # If the model repeats its name during message, for some reason, strip its name and keep text
                elif i > 0 and model_message_text.startswith("GEOINT:"):
                    # Update the message location variable
                    i += 1

                    # Strip the model's name
                    stream = str(model_message_text)[len("GEOINT:"):].strip()

                    # Update text of the posted widget
                    self.chat_model_message_widget.message_content.setText(stream)

                # If the model does NOT repeat its name during message, update the widget's text
                elif i>0 and not model_message_text.startswith("GEOINT:"):
                    # Update text of the posted widget
                    self.chat_model_message_widget.message_content.setText(str(model_message_text))

                    # Update the message location variable
                    i += 1

            # Ensure the model's name is not in the model_message_text string
            if model_message_text.startswith("GEOINT:"):
                model_message_text = model_message_text[len("GEOINT:"):].strip()

        # Caught an exception during streaming, meaning the streaming feature failed
        except:
            # Emit isStream signal of val False, this will change the loading animation to Red notifying
            # that the streaming feature has Failed, and thus model response will be slower than usual
            self.signals.isStream.emit(False)

            # Run the model normally with input
            model_output= replicate.run(
                # "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
                "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
                input=input
            )

            # For every word append it to the string, Usually, the model responds with an array of words so we j
            # sut append it  the model_message_text string
            for item in model_output:
                model_message_text += item

            # Ensure the model's name is not in the model_message_text string
            if model_message_text.startswith("GEOINT:"):
                model_message_text = model_message_text[len("GEOINT:"):].strip()

            print(model_message_text)

            # Set text of empty ModelMessage widget
            self.chat_model_message_widget.message_content.setText(model_message_text)

            # Post widget to layout
            self.chat_scroll_layout.addWidget(self.chat_model_message_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # No matter what way the response is received, emit the response
        self.signals.response_received.emit(model_message_text)
