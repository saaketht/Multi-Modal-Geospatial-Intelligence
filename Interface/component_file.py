
# This file contains all the styled components/widgets that fit the application's theme.

from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QStyleOptionTabWidgetFrame
from PyQt6.QtWidgets import (
    QTabBar,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QSpacerItem,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QDockWidget,
    QSizePolicy,
    QFrame,
    QTabWidget,
    QPlainTextEdit,
    QInputDialog,
    QSplitter
)

# Styled QScrollArea
class ScrollArea(QScrollArea):
    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Set the stylesheet of QScrollArea
        self.setStyleSheet('''
        QScrollArea
        {
            padding:0;
            background: #202020;
            border-top: 2px solid #494949;
            border-bottom: 2px solid #494949;
            border-radius:0;
            margin:0;
        }

        QScrollBar:vertical 
        {
             border: 2px solid transparent;
             background: transparent;
             width: 15px;
             margin: 22px 0 22px 0;
             border-radius:6px;
        }
         
        QScrollBar::handle:vertical {
            background: #494949;
            border:2px solid transparent;
            min-height: 20px;
            border-radius:5px;
        }

        QScrollBar::add-line:vertical {
            border: 2px solid transparent;
            background: transparent;
            height: 20px;
            border-radius:5px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            border: 2px solid transparent;
            background: transparent;
            height: 20px;
            border-radius:5px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
         
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: 2px solid transparent;
            width: 3px;
            height: 3px;
            border-radius:3px;
            background: transparent;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        ''')

# Styled QSplitter
class Splitter (QSplitter):
    # Constructor
    def __init__(self, parent=None):
        #Call Parent Constructor
        super().__init__(parent=parent)

        # Set the stylesheet of QSplitter
        self.setStyleSheet('''
        QSplitter::handle {
            background-color: #2d2d2d;
        }
        
        QSplitter::handle:horizontal {
            width: 4px;
        }
        
        QSplitter::handle:vertical {
            height: 4px;
        }
        
        QSplitter::handle:hover {
            background-color: #494949;
        }
        QSplitter::handle:pressed {
            background-color: #03B5A9;
        }
        
        ''')

# Styled QPlainTextEdit
class PlainTextEdit(QPlainTextEdit):
    # Constructor
    def __init__(self, parent=None):
        #Call Parent Constructor
        super().__init__(parent=parent)

        #Set stylesheet of QPlainTextEdit
        self.setStyleSheet('''
        PlainTextEdit
        {
            border-radius: 0;
            border-top:2px solid #494949;
            border-bottom: 2px solid #494949;
            border-right:0;
            border-left:0;
            color:#FFFFFF;
        }
        
        ''')

# Styled QSlider
class Slider(QSlider):
    # Constructor
    def __init__(self, Orientation, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent, orientation=Orientation)

        # Set stylsheet of QSlider
        self.setStyleSheet('''
        QSlider::groove:horizontal {
            border: 0px solid;
            height:10px;
            margin: -3px 2px;
            min-width:200px;
        }
        QSlider::handle:horizontal
        {
            background-color: #FFFFFF;
            border: 0px solid #FFFFFF;
            
            width: 10px;
            border-radius: 5px;
            margin: 0px 0px;
        }
        
        QSlider::add-page:horizontal 
        {
            background: #2D2D2D;
        }
        
        QSlider::sub-page:horizontal
        {
            background: #03B5A9;
        }
        ''')

# Custom title bar, inherits from QFrame to host other widgets,like push buttons and labels
class TitleBar(QFrame):
    # Constructor
    def __init__(self, title='', parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Set stylsheet of QFrame
        self.setStyleSheet('''
                background-color: #2D2D2D;
                border: 2px solid #494949;
                border-radius: 10px;
                padding-right: 4px;
                padding-left:4px;
                ''')

        # Create QFont
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)

        self.setFont(self.font1)

        # Title Bar will be 38px in height
        self.setFixedHeight(38)

        # Layout for Frame
        self.layoutSub = QHBoxLayout(self)
        self.layoutSub.setContentsMargins(0, 0, 0, 0)
        self.layoutSub.setSpacing(4)
        self.layoutSub.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layoutSub.addStretch()

        # The following three are buttons for the title bar
        self.titlebar_button1 = icon_button(icon_square_len=16, initial_icon='feather(3px)/help-circle.svg',
                                            button_square_len=28, type='type2')
        self.titlebar_button1.setToolTip("Help")
        self.titlebar_button2 = icon_button(icon_square_len=16, initial_icon='feather(3px)/sliders.svg',
                                            button_square_len=28, type='type2')
        self.titlebar_button2.setToolTip("Model Parameters")
        self.titlebar_button3 = icon_button(icon_square_len=16, initial_icon='feather(3px)/settings.svg',
                                            button_square_len=28, type='type2')
        self.titlebar_button3.setToolTip("Settings")


        # Label for the Title bar
        self.titlebar_title = QLabel(title)
        self.titlebar_title.setStyleSheet('''
                    color: #FFFFFF;
                    margin: 0px;
                    border: 0px;
                    ''')

        # Set font for label
        self.titlebar_title.setFont(self.font1)

        # QSpacerItems are used to make the buttons off center, but keep Label centered
        # note 3 spacers are added becasue there are 3 buttons on the right that are 28px by 28px, but the spacing between them
        # is 4px, so the spacer item size must be 32 px bc there isn't any space between the spacers.
        self.spacer1 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer2 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer3 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Add spacers
        self.layoutSub.addItem(self.spacer1)
        self.layoutSub.addItem(self.spacer2)
        self.layoutSub.addItem(self.spacer3)

        # Add buttons and title
        self.layoutSub.addWidget(self.titlebar_title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutSub.addStretch()
        self.layoutSub.addWidget(self.titlebar_button1)
        self.layoutSub.addWidget(self.titlebar_button2)
        self.layoutSub.addWidget(self.titlebar_button3)


# Custom title bar for Dock Widgets, inherits from QFrame to host other widgets,like push buttons and labels
class DockTitleBar(QFrame):
    # Constructor
    def __init__(self, title='', parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Set stylsheet of QFrame
        self.setStyleSheet('''
                background-color: #2D2D2D;
                border: 2px solid #494949;
                border-radius: 10px;
                padding-right: 4px;
                padding-left:4px;
                ''')

        # Create QFont
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)

        self.setFont(self.font1)

        # Title Bar will be 38px in height
        self.setFixedHeight(38)
        self.layoutSub = QHBoxLayout(self)
        self.layoutSub.setContentsMargins(0, 0, 0, 0)
        self.layoutSub.setSpacing(4)

        # The following 2 are buttons for the dock title bar, they include the close and float buttons
        self.titlebar_exit = icon_button(icon_square_len=16, initial_icon='feather(3px)/x.svg',
                                         button_square_len=28, type='type2', exit=True)
        self.titlebar_exit.setToolTip("Close")
        self.titlebar_float = icon_button(icon_square_len=16, initial_icon='feather(3px)/arrow-up-right.svg',
                                          button_square_len=28, type='type2')
        self.titlebar_float.setToolTip("Pop-Out")

        # Label for the Title bar
        self.titlebar_title = QLabel(title)
        self.titlebar_title.setStyleSheet('''
                    color: #FFFFFF;
                    margin: 0 2px 0 0 ;
                    border: 0px;
                    ''')
        self.titlebar_title.setFont(self.font1)

        # QSpacerItems are used to make the buttons off center, but keep Label centered
        # note 2 spacers are added becasue there are 2 buttons on the right that are 28px by 28px, but the spacing between them
        # is 4px, so the spacer item size must be 32 px bc there isn't any space between the spacers.
        self.spacer1 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer2 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Add buttons and title
        self.layoutSub.addWidget(self.titlebar_exit)
        self.layoutSub.addWidget(self.titlebar_float, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutSub.addStretch()
        self.layoutSub.addWidget(self.titlebar_title)

        # Add spacers and Stretch
        self.layoutSub.addItem(self.spacer1)
        self.layoutSub.addItem(self.spacer2)
        self.layoutSub.addStretch()

# Custom TabWidget, inherits from QTabWidget
class TabWidget(QTabWidget):
    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent=parent)

        # Create QFont
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(14)
        self.font1.setWeight(1000)

        # Let Tabs be movable
        self.setMovable(True)

        # Let tab widget use scroll buttons
        self.setUsesScrollButtons(True)

        # Let tabs be closable
        self.setTabsClosable(True)

        # Set Font for Tab Widget
        self.setFont(self.font1)

        # Set Content margins to 0
        self.setContentsMargins(0, 0, 0, 0)

        # Set stylesheet for QTabWidget
        self.setStyleSheet('''
        QToolTip
        {
            background-color: #494949;
            color:#FFFFFF;
            border:none
        }
        QTabWidget QWidget
        {
            border: none;
        }
        
        QTabWidget QFrame
        {
            border: none;
        }
        
        QTabWidget::pane 
        {
            margin-top:-2px;
            border: none;
            background: #202020;
            border-top:2px solid #494949;
            border-bottom-left-radius:10px;
            border-bottom-right-radius:10px;
        }
        
        QTabWidget::tab-bar
        {
            top:0px;
            bottom:0px;
            border:none;
            padding:0px;
            margin:1.5px;
            alignment:left;
        }
        
        QTabBar::tab:top 
        {
            top:0px;
            color:#FFFFFF;
            background:#202020;
            border: 2px solid #494949;
            border-top-right-radius:10px;
            border-top-left-radius:10px;
            margin-top:0px;
            margin-left:6px;
            margin-right:0px;
            margin-bottom:0px;
            /*total height of the tab must be 38px, but the borders of the tab belong to a frame so */
            padding-left:7px;
            padding-bottom:0;
            padding-top:0;
            padding-right:7px;
            height:34px;
            width:125px;
        }
        
        /*commented because it does not render fast enough when moving tabs around*/
        /*
        QTabBar::tab::last
        {
            margin-right: 6px;
        }
        QTabBar::tab::only-one
        {
            margin-left: 8px;
            margin-right:1.5px;
        }*/
        
        QTabBar
        {
            
        }
        QTabBar::tab:selected {
            /*background:#202020;*/
            font-family: Arial;
            font-size: 14px; 
            font-weight: 1000;
            border-bottom: 2px solid #202020;
        }
        
        QTabBar::tab:!selected
        {
            background: #494949;
            border-bottom: 2px solid #494949;
            
        }
        QTabBar::tab:!selected:hover
        {
            background: #03B5A9;
            border: 2px solid #03B5A9;
            border-bottom: 2px solid #494949;
        
        }
        QTabBar::close-button
        {
            background: transparent;
            subcontrol-position: right;
            image: url(feather(3px)/x.svg);v
        }

        QTabBar::close-button:hover
        {
            border-radius:10px;
            background:#494949;
        }
        
        QTabBar::close-button:pressed
        {
            border-radius:10px;
            background:#FF0000;
        }
        
        QTabBar QToolButton
        {
            background-color: #202020;
            border-image: none;
            border: 2px solid #202020;
            border-radius:10px;
            padding:8px;
            margin-bottom:4px;
            margin-right:1px;
            margin-top:0;
            margin-left:1px;
        }
        
        QTabBar QToolButton:hover 
        {
            background-color: #2d2d2d;
            border: 2px solid #2d2d2d;
        }
        
        QTabBar QToolButton:pressed 
        {
            
            background-color: #03B5A9;
            border: 2px solid #03B5A9;
        }
        
        QTabBar::scroller 
        { /* the width of the scroll buttons */
            width:74px;
        }
        
        QTabBar::tear
        {
            background:none;
            border:none;
        } 
        
        QTabBar QToolButton::right-arrow 
        {
            image: url(feather(3px)/arrow-right.svg);
        }
        
        QTabBar QToolButton::left-arrow 
        {
            image: url(feather(3px)/arrow-left.svg);
        }
        
        QTabBar QToolButton::left-arrow:disabled 
        {
            image: url(feather(3px)/arrow-left-disabled.svg)
        }
        
        QTabBar QToolButton::right-arrow:disabled 
        {
            image: url(feather(3px)/arrow-right-disabled.svg)
        }
        ''')

        self.index = 0

        # Add new tab button
        self.addButton = icon_button(initial_icon='feather(3px)/plus.svg', icon_square_len=16, button_square_len=34)
        self.addButton.setToolTip("Add New Chat")

        # Create an empty corner widget to set position of add button
        corner_widget = QWidget()
        corner_widget.setContentsMargins(0, 0, 0, 0)
        corner_widget_layout = QHBoxLayout()
        corner_widget_layout.setContentsMargins(0, 0, 4, 4)
        corner_widget_layout.setSpacing(0)
        corner_widget_layout.addWidget(self.addButton, alignment=Qt.AlignmentFlag.AlignBottom)
        corner_widget.setLayout(corner_widget_layout)

        # set the corner widget
        self.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)

    # remove tab method, functions the same as the remove tab, but updates index when deleted
    def removeTab2(self, index):
        self.removeTab(index)
        self.index = self.index - 1

    # default value of "Tab" with an optional title parameter
    def addTab2(self, widget=None, title='Tab'):
        # if title=='Tab':
        # title = title + " " + str(self.index +1)
        if widget is None:
            widget = QWidget(parent=None)
        temp = self.index

        icon = QIcon('feather(2.5px)/globe.svg')
        self.insertTab(temp, widget, icon, title)

        #TODO: SINCE THIS IS AS CUSTOM FEATURE MOVE TO CHATWIDGETTAB IN CHATBOX.py UNDER CREATE NEW TAB METHOD
        if title == "Help":
            tab_index = self.indexOf(widget)
            self.tabBar().setTabButton(tab_index, QTabBar.ButtonPosition.RightSide, None)
        self.index += 1

# Styled QLineEdit
class LineEdit(QLineEdit):
    # Custom Signal
    enter_pressed = pyqtSignal()

    # Constructor
    def __init__(self):
        #Call Parent Constructor
        super().__init__(parent=None)

        # Height of text box mus tbe 34 px
        self.setFixedHeight(34)

        #Let text be in the middle of the box, vertically
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Create QFont and set it text in the line edit
        font1 = QFont('Arial')
        font1.setPixelSize(13)
        self.setFont(font1)

        # Set stylesheet for QLineEdit
        self.setStyleSheet('''
        LineEdit
        {
            background: #202020;
            padding: none 16px;
            border: 2px solid #494949;
            border-radius:10px;
            color: #FFFFFF;
        }
        ''')

    # When enter is pressed emit signal
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.enter_pressed.emit()
        else:
            super().keyPressEvent(event)

# Styled QLabel
class Label(QLabel):

    # Constructor
    def __init__(self, text=""):
        # Call Parent Constructor
        super().__init__(text=text, parent=None)

        # Set Label height to 34px
        self.setFixedHeight(34)

        # Create QFont and set it text in the line edit
        font1 = QFont('Arial')
        font1.setPixelSize(13)
        self.setFont(font1)

        # Let label words wrap
        self.setWordWrap(False)

        # Set stylesheet for QLabel
        self.setObjectName("Label")
        self.setStyleSheet('''
        Label
        {
            background: transparent;
            padding: 0 16px;
            border-top:0;
            border-bottom:2px solid #494949;
            border-right:0;
            border-left:0;
            border-radius:0;
            color: #FFFFFF;
        }
        ''')

# Styled QDockWidget
class DockWidget(QDockWidget):
    # Constructor
    def __init__(self, title, widget_to_dock, parent=None):
        # Call Parent Constructor
        super().__init__(title, parent)

        # Allow dock to be all areas
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # Set Window Title
        self.setWindowTitle(title)

        # Create QFont and set it for dock
        font1 = QFont('Arial')
        font1.setPixelSize(13)
        font1.setWeight(1000)
        self.setFont(font1)

        # Make window minimum size 300px by 200px
        self.setMinimumSize(300, 200)

        # Create a frame for the widget to be displayed on
        self.frame = QFrame()
        self.frame_layout = QVBoxLayout(self.frame)

        self.frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setContentsMargins(10, 10, 10, 10)
        self.frame_layout.setSpacing(0)
        self.frame_layout.addWidget(widget_to_dock)

        # set the widget to the frame
        self.setWidget(self.frame)

        # Let Dock be docked and not floating, initially
        self.setFloating(False)

        # Create an instance of the custom dock tile bar
        self.titlebar = DockTitleBar(title)

        # Set object name for the widget that is placed in the dock, for stylesheet
        self.widget().setObjectName("widget")

        # Set Title bar to custom title bar
        self.setTitleBarWidget(self.titlebar)

        # Connect custom buttons from title bar
        self.titlebar.titlebar_exit.clicked.connect(lambda: self.close())
        self.titlebar.titlebar_float.clicked.connect(lambda: self.setFloating(True))

        # check if dock is floating or not.
        self.topLevelChanged.connect(lambda x: self.floatHandler(x))

        # Set stylesheet for QDockWidget
        self.setStyleSheet('''
        QDockWidget 
        { 
            background: #494949;
            color:#ffffff;
            titlebar-close-icon: url(feather(3px)/x.svg);
            titlebar-normal-icon: url(feather(3px)/arrow-up-right.svg);
        }
        
        QDockWidget #widget
        {
            color:#ffffff;
            background: #202020;
            margin-top:2px;
            border: 2px solid #494949;
            border-radius:10px;
        } 
        
        /*this will change the contents of the qdock widget too bc all widgets are QWidgets 
        I STRONGLY recommend changing/styling those widgets instead of inheriting this stylesheet
        so THIS MUST BE FIXED*/
        QDockWidget QListWidget
        {
            color:#ffffff;
            background: #202020;
            border: 2px solid transparent;
            border-radius:8px;
        }
        
        /*QDockWidget::title 
        {
            background: #2D2D2D; 
            text-align: center;
            border: 2px solid #494949;
            border-radius: 10px;
            padding:2px;
        }
        
        QDockWidget::close-button, QDockWidget::float-button 
        {
            border: 0px solid transparent;
            background: #2D2D2D;
            icon-size: 28px;
            width:16px;
            border-radius:10px;
            padding:6px;
            margin:4px;
        }
        
        QDockWidget::float-button
        {
            subcontrol-position: top left;
            subcontrol-origin: margin;
            position: absolute;
            top: 0px; left: 34px;
            icon: url(feather(3px)/arrow-up-right.svg);
            
        }
        
        QDockWidget::close-button {
            subcontrol-position: top left;
            subcontrol-origin: margin;
            position: absolute;
            top: 0px; left: 2px;
            icon: url(feather(3px)/x.svg);
        }
        
        QDockWidget::float-button:hover {
            icon: url(feather(3px)/arrow-up-right.svg);
            background:#494949;
        }
        
        QDockWidget::close-button:hover {
            icon: url(feather(3px)/x.svg);
            background:#494949;
        }
        QDockWidget::float-button:pressed {
            icon: url(feather(3px)/arrow-up-right.svg);
            background:#03B5A9;
        }
        
        QDockWidget::close-button:pressed {
            icon: url(feather(3px)/x.svg);
            background:#ff0000;
        }*/
        ''')

    # method removes the custom titlebar if window is floating, if not put it back.
    # Reason for this is because the dock no longer becomes
    # resizable when floating with a custom titlebar.
    def floatHandler(self, x):
        # If floating, set titlebar to native titlebar
        if x:
            self.setTitleBarWidget(None)

        # If not floating set titlebar to custom one, must reconnect buttons
        else:
            self.setTitleBarWidget(self.titlebar)
            self.titlebar.titlebar_exit.clicked.connect(lambda: self.close())
            self.titlebar.titlebar_float.clicked.connect(lambda: self.setFloating(True))


# Styled ICON_ONLY QPushButtons
class icon_button(QPushButton):

    # constructor for the icon_button object
    # parameters configure the button's style
    def __init__(self, initial_icon='feather/activity.svg', icon_square_len=20, button_square_len=34, type='type1',
                 exit=False):

        # call parent constructor, QPushButton
        super().__init__()

        self.initial_icon = initial_icon  # set icon path parameter to object attribute
        self.setIcon(QIcon(self.initial_icon))  # set icon for button
        self.setIconSize(QSize(icon_square_len, icon_square_len))  # set icon size
        self.setFixedSize(QSize(button_square_len, button_square_len))  # set button size

        # if the button is an exit button, style it this way
        if (exit == True and type == 'type1'):
            self.setIcon(QIcon('feather(3px)/x.svg'))
            self.setStyleSheet('''
            icon_button
            {
                background-color: transparent;
                border-radius: 10px;
                border:0px;
                margin:0px;
            }
            
            icon_button:hover {
                background-color: #2d2d2d;
            }
            
            icon_button:pressed
            {
                background-color: #FF0000;
            }
            QToolTip
            {
                background-color: #494949;
                color:#FFFFFF;
                border:none
            }
            ''')
        elif (exit == True and type == 'type2'):
            self.setIcon(QIcon('feather(3px)/x.svg'))
            self.setStyleSheet('''
            icon_button
            {
                background-color: transparent;
                border-radius: 10px;
                border:0px;
                margin:0px;
            }

            icon_button:hover {
                background-color: #494949;
            }

            icon_button:pressed
            {
                background-color: #FF0000;
            }
            QToolTip
            {
                background-color: #494949;
                color:#FFFFFF;
                border:none
            }
            ''')

        # all other buttons are styled this way
        elif (exit == False and type == 'type1'):
            self.setStyleSheet('''
            icon_button
            {
                background-color: transparent;
                margin:0px;
                border-radius: 10px;
                border:0px;
            }
            icon_button:hover 
            {
                background-color: #2d2d2d;
            }
            icon_button:pressed
            {
                background-color: #03B5A9;
            }
            QToolTip
            {
                background-color: #494949;
                color:#FFFFFF;
                border:none
            }
            ''')
        elif (exit == False and type == 'type2'):
            self.setStyleSheet('''
            icon_button
            {
                background-color: #2d2d2d;
                margin:0px;
                border-radius: 10px;
                border:0px;
            }
            icon_button:hover 
            {
                background-color: #494949;
            }
            icon_button:pressed
            {
                background-color: #03B5A9;
            }
            QToolTip
            {
                background-color: #494949;
                color:#FFFFFF;
                border:none
            }
            ''')

# Styled QInputDialog
class CustomInputDialog(QInputDialog):
    # Constructor
    def __init__(self, parent=None):
        # Call Parent Constructor
        super().__init__(parent)

        # Set Window Title
        self.setWindowTitle("New Tab")

        # Input label
        self.setLabelText("<b>Enter tab name:</b>")

        # Re-name Ok button as Apply
        self.setOkButtonText("Apply")

        # Set stylesheet for QInputDialog
        self.setStyleSheet("""
            QInputDialog {
                background-color: #202020;
                color: #FFFFFF;
                border: 2px solid #494949;
                border-radius: 10px;
            }
            QFrame 
            {
               background-color: #202020;            
            }

            QLabel {
                color: #FFFFFF;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #202020;
                color: #FFFFFF;
                border: 2px solid #494949;
                border-radius: 10px;
                padding: 6px;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #202020;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-family: Arial;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #494949;
            }
            QPushButton:pressed {
                background-color: #03B5A9;
            }
        """)
