from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
import matlab.engine
import threading
from functools import partial
class MatlabThread(QtCore.QThread):
    matlab_start_signal = QtCore.pyqtSignal()
    engine = None
    def run(self):
        # Start Matlab engine here
        self.engine = matlab.engine.start_matlab()
        self.matlab_start_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Welcome")

        # create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # create the main layout
        self.main_layout = QGridLayout()
        central_widget.setLayout(self.main_layout)

        # add the label
        label = QLabel("Occupancy Sensing Using RF sensing", self)
        label.setFont(QFont("Arial", 15))
        self.main_layout.addWidget(label, 0, 0, 1, 1, Qt.AlignCenter)

        # progress label
        self.progress_label = QLabel("Please wait, the app is connecting to MATLAB", self)
        self.progress_label.setFont(QFont("Arial", 12))
        self.progress_label.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(self.progress_label, 1, 0, 1, 1, Qt.AlignCenter)

        self.matlab_thread = MatlabThread()
        self.matlab_thread.matlab_start_signal.connect(self.on_matlab_started)
        self.matlab_thread.start()

        # establish connection to matlab
        # self.stop_event = threading.Event()
    def on_matlab_started(self):
        # add the schema selection label

        self.progress_label.setText("Please select the type of RF sensor to be used")
        #
        # # add the Ir-uwb button
        ir_uwb_button = QPushButton("IR-UWB", self)
        ir_uwb_button.setFont(QFont('Arial',11))
        ir_uwb_button.clicked.connect(self.display_schema_choice)
        ir_uwb_button.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(ir_uwb_button, 3, 0, 1, 1, Qt.AlignCenter)
        #
        # # add the FMCW button
        fmcw_button = QPushButton("FMCW", self)
        fmcw_button.setFont(QFont('Arial', 11))
        fmcw_button.clicked.connect(self.display_schema_choice)
        fmcw_button.setContentsMargins(10, 15, 10, 10)
        self.main_layout.addWidget(fmcw_button, 4, 0, 1, 1, Qt.AlignCenter)

        self.main_layout.setRowMinimumHeight(3, 50 )
    def display_schema_choice(self):
        # implement the display_schema_choice function
        self.schema_selection_window = SchemaSelection()
        self.schema_selection_window.show()
        self.hide()
        pass


class SchemaSelection(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("IR-UWB")

        # create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # create the main layout
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # add the label
        label = QLabel("Please select the orientation of the seats", self)
        label.setFont(QFont("Arial", 15))
        label.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(label, 0, 1, 1, 1, Qt.AlignCenter)
        #
        home_page_button = QPushButton("Home Page", self)
        home_page_button.clicked.connect(self.display_home)
        home_page_button.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(home_page_button, 0, 0, 1, 1, Qt.AlignCenter)

        # creating the image button for the 3 different orientation
        y_button = QPushButton(self)
        y_button.setMaximumSize(65, 270)
        # Load an image from file
        pixmap = QPixmap("y_direction.png")
        button_icon = QIcon(pixmap)
        y_button.setIcon(button_icon)
        y_button.setIconSize(QSize(60, 266))
        main_layout.addWidget(y_button, 1, 0, 1, 1, Qt.AlignCenter)

        # label for the button
        y_label = QLabel("Y Direction", self)
        y_label.setFont(QFont('Arial', 10))
        main_layout.addWidget(y_label, 2, 0, 1, 1, Qt.AlignCenter)

    def display_home(self):
        home_page = MainWindow()
        home_page.show()
        self.hide()

    def display_y_schema(self):
        print('hello')



    # putting the button in its place
    # by using grid
    # button1.grid(row=0, column=0, padx=0, pady=0)
    # window_count = len(new_window.children)
    # print("before entry page ",window_count)
    # # # display the 3 different orientation
    # Button(Frame, "Y Direction", lambda: get_coordinates(0, new_window,window_count), (60, 266), 1, 0, "y_direction.png", 20, 20)
    # Button(Frame, "X Direction", lambda: get_coordinates(1, new_window,window_count), (300, 40), 1, 1, "x_direction.png", 35, 140)
    # Button(Frame, "2 Dimension", lambda: get_coordinates(2, new_window,window_count), (106, 200), 1, 2, "2d_space.png", 30, 50)

# create the application
app = QApplication([])

# create the main window
main_window = MainWindow()

# show the main window
main_window.show()

# run the application
app.exec_()


