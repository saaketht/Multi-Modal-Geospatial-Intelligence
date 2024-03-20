import sys
import json
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtWebEngineWidgets


from ipyleaflet import Map, Marker, LayersControl, basemaps
from ipywidgets import HTML, IntSlider
from ipywidgets.embed import embed_data
import folium
import io
class interactive_map_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.m = folium.Map(
            location=[28.598, -81.1974],tiles="openstreetmap",
            zoom_start=17,max_zoom=18
        )
        folium.TileLayer(attr="<a href=''></a>",
            tiles="https://geoint-bucket.s3.amazonaws.com/tileserv/{z}/{x}/{y}.png").add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)

        self.w = QtWebEngineWidgets.QWebEngineView(self)
        self.w.setHtml(self.data.getvalue().decode())

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.w)
        self.setLayout(self.layout)

# class MapWindow(QWidget):
#     def __init__(self, base_coords):
#         self.base_coords = base_coords
#         # Setting up the widgets and layout
#         super().__init__()
#         self.layout = QVBoxLayout()
#         self.title = QLabel("<b>This is my title</b>")
#         self.layout.addWidget(self.title)
#
#         # Create QtWebEngineView widget
#         self.web = QtWebEngineWidgets.QWebEngineView(self)
#
#         # Sliders
#         s1 = IntSlider(max=200, value=100)
#         s2 = IntSlider(value=40)
#
#         # Working with the maps with ipyleaflet
#         self.map = Map(center=self.base_coords, basemaps=basemaps.OpenStreetMap.Mapnik, zoom=10)
#         self.marker = Marker(location=self.base_coords)
#         self.marker.popup = HTML(value='This is my marker')
#         self.map.add(self.marker)
#
#         data = embed_data(views=[s1, s2, self.map])
#
#         html_template = """
#         <html>
#           <head>
#
#             <title>Widget export</title>
#
#             <!-- Load RequireJS, used by the IPywidgets for dependency management -->
#             <script
#               src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"
#               integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA="
#               crossorigin="anonymous">
#             </script>
#
#             <!-- Load IPywidgets bundle for embedding. -->
#             <script
#               data-jupyter-widgets-cdn="https://unpkg.com/"
#               data-jupyter-widgets-cdn-only
#               src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@*/dist/embed-amd.js"
#               crossorigin="anonymous">
#             </script>
#
#             <!-- The state of all the widget models on the page -->
#             <script type="application/vnd.jupyter.widget-state+json">
#               {manager_state}
#             </script>
#           </head>
#
#           <body>
#
#             <h1>Widget export</h1>
#
#             <div id="first-slider-widget">
#               <!-- This script tag will be replaced by the view's DOM tree -->
#               <script type="application/vnd.jupyter.widget-view+json">
#                 {widget_views[0]}
#               </script>
#             </div>
#
#             <hrule />
#
#             <div id="second-slider-widget">
#               <!-- This script tag will be replaced by the view's DOM tree -->
#               <script type="application/vnd.jupyter.widget-view+json">
#                 {widget_views[1]}
#               </script>
#             </div>
#
#           </body>
#         </html>
#         """
#
#         manager_state = json.dumps(data['manager_state'])
#         widget_views = [json.dumps(view) for view in data['view_specs']]
#         rendered_template = html_template.format(manager_state=manager_state, widget_views=widget_views)
#
#         # Set HTML
#         self.web.setHtml(rendered_template)
#
#         # Add webengine to layout and add layout to widget
#         self.layout.addWidget(self.web)
#         self.setLayout(self.layout)
#
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     base_coords = [45.783119, 3.123364]
#     widget = MapWindow(base_coords)
#     widget.resize(900, 800)
#     sys.exit(app.exec())