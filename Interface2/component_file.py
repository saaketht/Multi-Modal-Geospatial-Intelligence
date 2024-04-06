import sys
from PyQt6.QtCore import Qt, QSize, QRect, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPainter, QBrush, QColor
from PyQt6.QtWidgets import QStyleOptionTabWidgetFrame
# from send import sendAndReceive
from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QApplication,
    QBoxLayout,
    QTabBar,
    QToolBar,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QSpacerItem,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QDockWidget,
    QSizePolicy,
    QGridLayout,
    QFrame,
    QTabWidget,
    QPlainTextEdit,
    QInputDialog
)


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        test1 = QTreeWidgetItem()


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

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


class Slider(QSlider):
    def __init__(self, Orientation, parent=None):
        super().__init__(parent=parent, orientation=Orientation)
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


class TitleBar(QFrame):
    def __init__(self, title='', parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet('''
                background-color: #2D2D2D;
                border: 2px solid #494949;
                border-radius: 10px;
                padding-right: 4px;
                padding-left:4px;
                ''')
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)
        self.setFont(self.font1)
        self.setFixedHeight(38)
        self.layoutSub = QHBoxLayout(self)
        self.layoutSub.setContentsMargins(0, 0, 0, 0)
        self.layoutSub.setSpacing(4)
        self.layoutSub.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layoutSub.addStretch()

        self.titlebar_button1 = icon_button(icon_square_len=16, initial_icon='feather(3px)/help-circle.svg',
                                            button_square_len=28, type='type2')
        self.titlebar_button2 = icon_button(icon_square_len=16, initial_icon='feather(3px)/sliders.svg',
                                            button_square_len=28, type='type2')
        self.titlebar_button3 = icon_button(icon_square_len=16, initial_icon='feather(3px)/settings.svg',
                                            button_square_len=28, type='type2')

        self.titlebar_title = QLabel(title)
        self.titlebar_title.setStyleSheet('''
                    color: #FFFFFF;
                    margin: 0px;
                    border: 0px;
                    ''')
        self.titlebar_title.setFont(self.font1)
        # note 3 spacers are added becasue there are 3 buttons on the right that are 28px by 28px, but the spacing between them
        # is 4px, so the spacer item size must be 32 px bc there isn't any space between the spacers.
        self.spacer1 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer2 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer3 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layoutSub.addItem(self.spacer1)
        self.layoutSub.addItem(self.spacer2)
        self.layoutSub.addItem(self.spacer3)

        self.layoutSub.addWidget(self.titlebar_title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutSub.addStretch()
        self.layoutSub.addWidget(self.titlebar_button1)
        self.layoutSub.addWidget(self.titlebar_button2)
        self.layoutSub.addWidget(self.titlebar_button3)


class DockTitleBar(QFrame):
    def __init__(self, title='', parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet('''
                background-color: #2D2D2D;
                border: 2px solid #494949;
                border-radius: 10px;
                padding-right: 4px;
                padding-left:4px;
                ''')
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(13)
        self.font1.setWeight(1000)
        self.setFont(self.font1)
        self.setFixedHeight(38)
        self.layoutSub = QHBoxLayout(self)
        self.layoutSub.setContentsMargins(0, 0, 0, 0)
        self.layoutSub.setSpacing(4)
        # self.layoutSub.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.titlebar_exit = icon_button(icon_square_len=16, initial_icon='feather(3px)/x.svg',
                                         button_square_len=28, type='type2', exit=True)
        self.titlebar_float = icon_button(icon_square_len=16, initial_icon='feather(3px)/arrow-up-right.svg',
                                          button_square_len=28, type='type2')

        self.titlebar_title = QLabel(title)
        self.titlebar_title.setStyleSheet('''
                    color: #FFFFFF;
                    margin: 0 2px 0 0 ;
                    border: 0px;
                    ''')
        self.titlebar_title.setFont(self.font1)
        # note 3 spacers are added becasue there are 3 buttons on the right that are 28px by 28px, but the spacing between them
        # is 4px, so the spacer item size must be 32 px bc there isn't any space between the spacers.
        self.spacer1 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.spacer2 = QSpacerItem(32, 32, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layoutSub.addWidget(self.titlebar_exit)
        self.layoutSub.addWidget(self.titlebar_float, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layoutSub.addStretch()
        self.layoutSub.addWidget(self.titlebar_title)
        self.layoutSub.addItem(self.spacer1)
        self.layoutSub.addItem(self.spacer2)
        self.layoutSub.addStretch()


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.font1 = QFont('Arial')
        self.font1.setPixelSize(14)
        self.font1.setWeight(1000)
        self.setMovable(True)
        self.setFont(self.font1)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''
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
        self.setTabsClosable(True)
        # self.tabCloseRequested.connect(self.removeTab2)
        self.index = 0

        # delete from here
        # self.addTab2(widget=chat())
        # self.addTab2(widget=chat())
        # to here

        self.addButton = icon_button(initial_icon='feather(3px)/plus.svg', icon_square_len=16, button_square_len=34)

        corner_widget = QWidget()
        corner_widget.setContentsMargins(0, 0, 0, 0)
        corner_widget_layout = QHBoxLayout()
        corner_widget_layout.setContentsMargins(0, 0, 4, 4)
        corner_widget_layout.setSpacing(0)
        corner_widget_layout.addWidget(self.addButton, alignment=Qt.AlignmentFlag.AlignBottom)
        corner_widget.setLayout(corner_widget_layout)
        self.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)

        # DELETE THIS, CONNEC THSI WHEN YOU CREATE A A CHAT BOX FILE
        # self.addButton.clicked.connect(lambda : self.addTab2(widget=chat()))

        # self.test = QHBoxLayout()
        # spacer = QSpacerItem(8,8,QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.test.addWidget(self.addButton)
        # self.test.addItem(spacer)

        self.setUsesScrollButtons(True)

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
        # self.tabBar().tabButton(temp, QTabBar().ButtonPosition.RightSide).setFixedSize(QSize(24, 24))
        self.index += 1


class LineEdit(QLineEdit):
    enter_pressed = pyqtSignal()

    def __init__(self):
        super().__init__(parent=None)

        self.setFixedHeight(34)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        font1 = QFont('Arial')
        font1.setPixelSize(13)
        self.setFont(font1)
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.enter_pressed.emit()
        else:
            super().keyPressEvent(event)


class Label(QLabel):
    def __init__(self, text=""):
        super().__init__(text=text, parent=None)

        self.setFixedHeight(34)
        font1 = QFont('Arial')
        font1.setPixelSize(13)
        self.setFont(font1)
        self.setWordWrap(False)
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


class DockWidget(QDockWidget):
    def __init__(self, title, widget_to_dock, parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.setWindowTitle(title)

        font1 = QFont('Arial')
        font1.setPixelSize(13)
        font1.setWeight(1000)
        self.setFont(font1)
        self.setMinimumSize(300, 200)

        self.frame = QFrame()
        self.frame_layout = QVBoxLayout(self.frame)

        # self.frame.setLayout(self.frame_layout)
        self.frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setContentsMargins(10, 10, 10, 10)
        self.frame_layout.setSpacing(0)
        self.frame_layout.addWidget(widget_to_dock)
        self.setWidget(self.frame)

        self.setFloating(False)
        self.titlebar = DockTitleBar(title)
        self.widget().setObjectName("widget")
        self.setTitleBarWidget(self.titlebar)
        self.titlebar.titlebar_exit.clicked.connect(lambda: self.close())
        self.titlebar.titlebar_float.clicked.connect(lambda: self.setFloating(True))

        self.topLevelChanged.connect(lambda x: self.floatHandler(x))

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

    def floatHandler(self, x):
        if x:
            self.setTitleBarWidget(None)
        else:
            self.setTitleBarWidget(self.titlebar)
            self.titlebar.titlebar_exit.clicked.connect(lambda: self.close())
            self.titlebar.titlebar_float.clicked.connect(lambda: self.setFloating(True))


class icon_button(QPushButton):

    # constructor for the icon_button object
    # parameters configure the button's style
    def __init__(self, initial_icon='feather/activity.svg', icon_square_len=20, button_square_len=34, type='type1',
                 exit=False, toggle=False):

        # call parent constructor, QPushButton
        super().__init__()

        # FONTS
        # id = QFontDatabase.addApplicationFont(
        #     '/Users/basmattiejamaludin/Documents/Notes/Python/PyQt6/SFProTTF/SFProText-HeavyItalic.ttf')
        # if id < 0: print('error')
        # families = QFontDatabase.applicationFontFamilies(id)
        # self.setFont(QFont(families[0], 12))

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
            ''')


class CustomInputDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New Tab")
        self.setLabelText("<b>Enter tab name:</b>")
        self.setOkButtonText("Apply")

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
                background-color: #494949;
                color: #FFFFFF;
                border: 2px solid #202020;
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
