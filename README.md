# Multi-Modal Geospatial Intelligence

## Objective

Develop a geospatial intelligence application using multi-modal models (Segment Anything Model, OpenAl's CLIP, QA) for zero-shot classification in computer vision tasks, leveraging geospatial datasets like RSICD.

## Key Requirements

1. Integration of Multi-Modal Models
    - Combine vision and language models for accurate classifications and responses.
2. Zero-Shot Classification
    - Leverage the zero-shot classification capabilities of multi-modal models for real-time insights.
3. Geospatial Data Utilization
    - Efficiently process and analyze geospatial datasets to extract valuable insights.
4. User-Friendly Interface
    - Create an intuitive interface for easy navigation and understanding of results.

## Impact

 This project has the potential to revolutionize geospatial data processing and analysis in various sectors like environmental monitoring, urban planning, and disaster management. It can also inspire the development of similar applications in other domains.

## Setting Up the Application: 
Create a python virtual environment, python 3.11 or greater 
The virtual environment must be created in the same directory as  the “interface”  folder. 
Activate that python virtual environment
Using the terminal enter the interface file cd Interface
Install all the packages required for the application by running this command: pip install -r requirements.txt 
Install python-dotenv module by running this command: pip install python-dotenv
Create a .env file inside the interface folder
Add your api key from Replicate (Might have to create an account) to that .env file as shown below. 
REPLICATE_API_KEY = ”######################################”

## To run the application
Run Interface.py
python Interface.py: 
## Python Description files/folders:
The ‘feather’, ‘feather(2.5px)’, and’ feather(3px)’ folders holds the application’s icons, and are sourced from https://feathericons.com/. 
The ‘loadingSvg’ folder holds all the loading animations for the application and are sourced from https://loading.io/ 
The ‘splashScreen’ folder holds the splash screen image that is displayed when the application is booting. 
chat_history_dock.py: Manages the chat sessions within GUI. Allows users to start new chats, open existing ones and remove chats from their history. Contains customized widgets related to the Chat History Window.
chatbox_file.py:  Allows users to interact with Llava. Contains customized widgets related to the chat interface. 
component_file.py: Contains all the styled components/widgets that fit the application's theme.
file_explorer_dock.py: The file explorer dock allows users to upload an image, remove and image, and keep track of what image is currently being viewed in the current conversation. Contains customized widgets related to the File Explorer Window
interface.py: This file calls the main window of the application, it instantiates all of the custom widgets and places all widgets in its rightful location. 
interactive_map_dock.py: Allows users to screenshot, and capture satellite images, and view GeoTiff Images in their rightful location. Contains the widgets related to the Interactive Map Window. Contains localtileserver package built by Bane Sullivan.
image_preview_dock.py: Contains a custom widget for displaying images. Handles image scaling and interactive functionalities. Contains the widgets related to the Current Image Window and the File Explorer Window
model_runnable.py: Integrates multimodal model using a replicate API.
current model application is using: llava-v1.6-vicuna-13b

## Limitations:

If a user tries to pass a file larger than 20 MB through Replicate’s API it will return an error: Prediction interrupted; please retry (code: PA). We believe this is due us setting the file as input in the request body leading to Replicate’s API enforcing limits on the size of the request.
