from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
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
        label.setFont(QFont("Arial", 20))
        self.main_layout.addWidget(label, 0, 0, 1, 1, Qt.AlignCenter)

        # progress label
        self.progress_label = QLabel("Please wait, the app is connecting to MATLAB", self)
        self.progress_label.setFont(QFont("Arial", 15))
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
        ir_uwb_button = QPushButton("Ir-uwb", self)
        ir_uwb_button.clicked.connect(self.display_schema_choice)
        ir_uwb_button.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(ir_uwb_button, 3, 0, 1, 1, Qt.AlignCenter)
        #
        # # add the FMCW button
        fmcw_button = QPushButton("FMCW", self)
        fmcw_button.clicked.connect(self.display_schema_choice)
        fmcw_button.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(fmcw_button, 4, 0, 1, 1, Qt.AlignCenter)

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
        label = QLabel("Choose a schema", self)
        label.setFont(QFont("Arial", 20))
        main_layout.addWidget(label)


# create the application
app = QApplication([])

# create the main window
main_window = MainWindow()

# show the main window
main_window.show()

# run the application
app.exec_()



