from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, \
    QLineEdit, QFormLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon, QIntValidator, QTransform
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
import matlab.engine
from PIL import Image, ImageTk
import threading
from functools import partial

from qtpy import QtWidgets


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
        y_button.clicked.connect(self.display_y_schema)
        main_layout.addWidget(y_button, 1, 0, 1, 1, Qt.AlignCenter)

        # label for the button
        y_label = QLabel("Y Direction", self)
        y_label.setFont(QFont('Arial', 10))
        main_layout.addWidget(y_label, 2, 0, 1, 1, Qt.AlignCenter)

        vlayout = QVBoxLayout()

        x_button = QPushButton(self)
        x_button.setMaximumSize(310, 50)
        # Load an image from file
        pixmap = QPixmap("x_direction.png")
        button_icon = QIcon(pixmap)
        x_button.setIcon(button_icon)
        x_button.setIconSize(QSize(300, 40))
        x_button.clicked.connect(self.display_x_schema)
        vlayout.addWidget(x_button)
        # label for the button
        x_label = QLabel("X Direction", self)
        x_label.setFont(QFont('Arial', 10))
        vlayout.addWidget(x_label)

        main_layout.addItem(vlayout,1,1,1,1,Qt.AlignCenter)

        vlayout = QVBoxLayout()
        z_button = QPushButton(self)
        z_button.setMaximumSize(150, 100)
        # Load an image from file
        pixmap = QPixmap("2d_space.png")
        button_icon = QIcon(pixmap)
        z_button.setIcon(button_icon)
        z_button.setIconSize(QSize(150, 150))
        z_button.clicked.connect(self.display_z_schema)
        vlayout.addWidget(z_button)

        # label for the button
        z_button = QLabel("2 D Space", self)
        z_button.setFont(QFont('Arial', 10))
        vlayout.addWidget(z_button)

        main_layout.addItem(vlayout,1,2,1,1,Qt.AlignCenter)

    def display_home(self):
        # home_page = MainWindow()
        main_window.show()
        self.hide()

    def display_y_schema(self):
        flag = False
        count = 0
        while(not flag):
            if(count==0):
                text = "Enter the number of seats from 1 to 10"
            else:
                text = "Please enter a valid Integer ranging from 1 to 10"
            seat_input, done1 = QtWidgets.QInputDialog.getText(
                self, 'Seat Coordinates', text)
            count = count+1
            if(done1):
                no_of_chair = check_coordinates(1, 10, [seat_input])
                if(type(no_of_chair) == list):
                    flag = True
            else:
                break
        if(flag):
            no_of_chair = int(no_of_chair[0])
            self.user_input = Seat_Input(0,no_of_chair)
            self.user_input.show()
    def display_x_schema(self):
        print("going to x")
    def display_z_schema(self):
        print("going to z")


def check_coordinates(min_range,max_range,entry_list):
    try:
        temp = []
        for i in entry_list:
            number = int(i)
            if (number >= min_range and number <= max_range):
                temp.append(number)
            else:
                return False

        return temp
    except:
        return False

def check_spacing(entry_list,mode):
    if(mode!=2):
        for i in range(len(entry_list) - 1):
            for j in range(i + 1, len(entry_list)):
                if abs(entry_list[i] - entry_list[j]) < 30:
                    return False
        return True
    else:
        x_coordinates = entry_list[0::2]
        y_coordinates = entry_list[1::2]
        if(check_spacing(x_coordinates,1) and check_spacing(y_coordinates,0) ):
            return True
        else:
            return False

class Seat_Input(QMainWindow):
    def __init__(self,mode,no_of_chair):
        super().__init__()
        self.mode = mode
        self.no_of_chair = no_of_chair
        print(no_of_chair)

        # set the title
        self.setWindowTitle("Seat Coordinates")

        # have a the text displayed based on the mode
        if(mode==0):
            text = "Enter the y coordinates of the seats in cm from 50 to 500cm"
        elif(mode==1):
            text = "Enter the x coordinates of the seats in cm from 50 to 500cm"
        else:
            text = "Enter the x & y coordinates of the seats in cm from 50 to 500cm"

        # user input page
        # create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # create a back button to go to seat page
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back)
        back_button.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(back_button, 0, 0, 1, 1, Qt.AlignCenter)


        # create a label widget to know what the user is going to type
        self.main_label = QLabel(text, self)
        self.main_label.setFont(QFont('Arial', 13))
        main_layout.addWidget(self.main_label,0,1,1,1,Qt.AlignCenter)


        self.entry_list= []
        self.entry_count = 0
        for i in range(0,no_of_chair):
            print("entering for loop")
            label= QLabel("Seat Number "+ str(i+1))
            label.setFont(QFont('Arial', 10))
            main_layout.addWidget(label, i+2, 0, 1, 1, Qt.AlignCenter)
            if(mode!=2):
                e1 = QLineEdit()
                e1.setValidator(QIntValidator())
                e1.editingFinished.connect(self.enterPress)
                main_layout.addWidget(e1, i+2, 1,1,1,Qt.AlignCenter)
                self.entry_list.append(e1)
            else:
                e1 = QLineEdit()
                e1.setValidator(QIntValidator())
                e1.editingFinished.connect(self.enterPress)
                main_layout.addWidget(e1, i+2, 1,1,1,Qt.AlignCenter)
                self.entry_list.append(e1)

                e2 = QLineEdit()
                e2.setValidator(QIntValidator())
                e2.editingFinished.connect(self.enterPress)
                main_layout.addWidget(e1, i+2, 2,1,1,Qt.AlignCenter)
                self.entry_list.append(e2)







        # the seat input from here will be passed to the schema displayed page
        # create 3 sub classes for each different schema, and we will intialise the seat canvas as well as the seat coordinates into the class attributes

        # create the schema for entering the coordinates of the seats based on the mode and the number of seats

    def enterPress(self):
        self.entry_count = self.entry_count +1
        user_input = []
        if(self.entry_count>=len(self.entry_list)):
            for i in self.entry_list:
                user_input.append(i.text())
            result = check_coordinates(50,500,user_input)
            if(type(result)!=list):
                self.main_label.setText("Please enter a valid number from 50 to 500")
            elif(check_spacing(result,self.mode) ):
                # go to the next page
                main_window.schema_selection_window.hide()
                self.hide()
                self.display_page = Schema_Page(self.mode,result)
                self.display_page.show()
            else:
                self.main_label.setText("Enter the coordinates that are 30cm apart from one another")

    def back(self):
        self.hide()
        main_window.schema_selection_window.display_y_schema()


class Schema_Page(QMainWindow):

    def __init__(self,mode,chair_coordinates):
        super().__init__()

        self.setWindowTitle("Seating Arrangement")

        self.mode = mode
        self.coordinates = chair_coordinates
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        back_button = QPushButton("Back", self)
        back_button.setFont(QFont('Arial', 10))
        back_button.clicked.connect(self.back)
        back_button.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(back_button, 0, 0, 1, 1, Qt.AlignCenter)

        top_widget = QWidget()
        top_frame = QGridLayout()
        top_widget.setLayout(top_frame)
        x_label = QLabel("Distance from the sensor in the X direction")
        x_label.setFont(QFont("Arial",13))
        top_frame.addWidget(x_label,0,6,1,1,Qt.AlignCenter)

        pixmap = QPixmap("x_arrow.png")
        pixmap = pixmap.scaled(500, 50)
        label = QLabel()
        label.setPixmap(pixmap)
        top_frame.addWidget(label,1,6,1,1,Qt.AlignCenter)
        main_layout.addWidget(top_widget,0,1,1,1,Qt.AlignCenter)


        side_widget = QWidget()
        side_frame = QGridLayout()
        side_widget.setLayout(side_frame)
        y_label = QLabel("Distance from the sensor in the Y direction")
        y_label.setFont(QFont("Arial",13))
        side_frame.addWidget(y_label,0,1,1,1,Qt.AlignCenter)
        empty_label = QLabel()
        side_frame.addWidget(empty_label, 1, 1, 1, 1, Qt.AlignCenter)
        transform = QTransform()
        transform.rotate(90)
        rotated_pixmap = pixmap.transformed(transform)
        y_label = QLabel()
        y_label.setPixmap(rotated_pixmap)
        side_frame.addWidget(y_label,6,1,1,1,Qt.AlignCenter)
        main_layout.addWidget(side_widget,1,0,1,1,Qt.AlignCenter)



        # side_frame = ttk.Frame(seat_window)
        # y_arrow = Image.open("y_arrow.png")
        # y_arrow = y_arrow.resize((50, 500))
        # y_arrow = ImageTk.PhotoImage(y_arrow)
        # y_arrow_label = ttk.Label(side_frame, image=y_arrow)
        # y_arrow_label.image = y_arrow
        # y_arrow_label.grid(row=6, column=1)
        # y_label = ttk.Label(side_frame, text="Distance from the sensor in the Y direction")
        # y_label.grid(row=0, column=1)
        # side_frame.grid(row=1, column=0)


    def back(self):
        self.hide()
        main_window.schema_selection_window.show()

# create the application
app = QApplication([])

# create the main window
main_window = MainWindow()

# show the main window
main_window.show()

# run the application
app.exec_()



