from queue import Queue

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, \
    QLineEdit, QFormLayout, QDesktopWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon, QIntValidator, QTransform, QBrush, QColor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
import matlab.engine
import numpy as np
from PIL import Image, ImageTk
import threading
from functools import partial
import paramiko
from qtpy import QtWidgets, QtGui
import time
import os
x_sensor_ip = "155.69.148.187" # the one with the name CNCL sticker on the sensor
y_sensor_ip = "155.69.149.225" # the one with the name demo

class MatlabThread(QtCore.QThread):
    matlab_start_signal = QtCore.pyqtSignal()
    stop_event = threading.Event()
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
        y_button.clicked.connect(lambda : self.display_schema(0))
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
        x_button.clicked.connect(lambda : self.display_schema(1))
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
        z_button.clicked.connect(lambda : self.display_schema(2))
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

    def display_schema(self,mode):
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
            self.user_input = Seat_Input(mode,no_of_chair)
            self.user_input.show()


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
                main_layout.addWidget(e2, i+2, 2,1,1,Qt.AlignCenter)
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
        main_window.schema_selection_window.display_schema(self.mode)




def start_sensor(shell, seat_coordinates, file_path,array):
    print("Running start sensor")
    start_time = time.time()
    shell.send("./Runme \n")
    while (1):
        output = shell.recv(1024)
        output_str = output.decode()
        if ("done" in output_str):
            break
    print("time sensor is done",time.time()-start_time)
    # at this point the file might not have sufficent frames or it might even be stopped halfway by other threads
    excel_start = time.time()
    while(os.path.getsize(file_path)<=52000):
        # wait for 0.5 seconds and retry
        pass
    print("time taken for excel to send over",time.time()-excel_start)
    matlab_time = time.time()
    state = main_window.matlab_thread.engine.IR_UWB_function(file_path, matlab.int32(seat_coordinates))
    print("matlab time taken",time.time()-matlab_time)
    print("matlab state",state)
    array.extend(state)
    print("time taken",time.time()-start_time)
    # os.rename(file_path,"z:/radar"+str(time.localtime())+".csv")
    os.remove(file_path)

class Running_Radar(QtCore.QThread):
    def __init__(self, shell,coordinates,file_path,queue):
        super().__init__()
        self.shell = shell
        self.coordinates = coordinates
        self.file_path=  file_path
        self.queue = queue
    def run(self):
        start_sensor(self.shell,self.coordinates,self.file_path,self.queue)

class Radar_Main_Thread(QtCore.QThread):
    def __init__(self,channel_list,seat_coordinate,file_path_list,stop_event: threading.Event,canvas):
        super().__init__()
        self.channel_list = channel_list
        self.coordinates = seat_coordinate
        self.paths = file_path_list
        self.event = stop_event
        self.canvas = canvas
    def run(self):
        # this will act as the main running thread which will create the thread to run a single instance
        # before we create thread to run the radar we need to change the pwd
        for i in self.channel_list:
            i.send("cd testing_realtime/ \n")
            while not i.recv_ready():
                pass
        # now all the channels are prepped and ready to start the radar
        while not self.event.is_set():
            if(len(self.channel_list)==1):
                # create a single instance of a thread to run the code
                state_array =[]
                radar_thread = Running_Radar(self.channel_list[0],self.coordinates,self.paths[0],state_array)
                radar_thread.start()
                # after this one instance of the thread has completed so we can call the display function
                # to display the states
                radar_thread.wait()
                display_states([state_array],self.coordinates,self.canvas)
            else:
                x_coordinates = [i[0] for i in self.coordinates]
                y_coordinates = [i[1] for i in self.coordinates]
                x_state = []
                y_state = []
                radar_thread_x = Running_Radar(self.channel_list[0],x_coordinates,self.paths[0],x_state)
                radar_thread_y = Running_Radar(self.channel_list[1], y_coordinates, self.paths[1], y_state)
                radar_thread_x.start()
                radar_thread_y.start()
                # after this one instance of the thread has completed so we can call the display function
                # to display the states
                radar_thread_y.wait()
                radar_thread_x.wait()
                display_states([x_state,y_state],self.coordinates,self.canvas)
                pass



class Schema_Page(QMainWindow):
    def __init__(self,mode,chair_coordinates):
        super().__init__()

        self.setWindowTitle("Seating Arrangement")

        self.mode = mode
        self.coordinates = chair_coordinates
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.canvas = []
        self.queue = Queue()
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)
        main_layout.setSpacing(10)

        back_button = QPushButton("Back", self)
        back_button.setFont(QFont('Arial', 10))
        back_button.clicked.connect(self.back)
        back_button.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(back_button, 0, 0, 1, 1, Qt.AlignLeft)

        #top frame
        top_widget = QWidget()
        top_frame = QGridLayout()
        top_widget.setLayout(top_frame)
        x_label = QLabel("Distance from the sensor in the X direction")
        x_label.setFont(QFont("Arial",13))
        top_frame.addWidget(x_label,0,1,1,1,Qt.AlignCenter)

        pixmap = QPixmap("x_arrow.png")
        pixmap = pixmap.scaled(500, 50)
        label = QLabel()
        label.setPixmap(pixmap)
        top_frame.addWidget(label,1,1,1,1,Qt.AlignCenter)
        main_layout.addWidget(top_widget,0,1,1,1,Qt.AlignCenter)

        #side frame
        side_widget = QWidget()
        side_frame = QGridLayout()
        side_widget.setLayout(side_frame)
        y_label = QLabel("Distance from the sensor in the Y direction")
        y_label.setFont(QFont("Arial",13))
        side_frame.addWidget(y_label,0,1,1,1,Qt.AlignCenter)
        transform = QTransform()
        transform.rotate(90)
        rotated_pixmap = pixmap.transformed(transform)
        y_label = QLabel()
        y_label.setPixmap(rotated_pixmap)
        side_frame.addWidget(y_label,1,1,1,1,Qt.AlignCenter)
        main_layout.addWidget(side_widget,1,0,1,1,Qt.AlignLeft)

        #side frame
        rightSide = QWidget()
        self.rightFrame = QGridLayout()
        rightSide.setLayout(self.rightFrame)

        self.start_label = QLabel("Press Start to Begin")
        self.start_label.setFont(QFont("Arial",9))
        self.rightFrame.addWidget(self.start_label,0,0,1,1,Qt.AlignCenter)
        start_button = QPushButton("Start", self)
        start_button.setFont(QFont('Arial', 10))
        start_button.clicked.connect(self.start)
        start_button.setContentsMargins(10, 10, 10, 10)
        self.rightFrame.addWidget(start_button, 1, 0, 1, 1, Qt.AlignCenter)
        main_layout.addWidget(rightSide,1,2,1,1,Qt.AlignCenter)

        seat_widget = QWidget()
        seat_frame = QGridLayout()
        seat_widget.setLayout(seat_frame)
        main_layout.addWidget(seat_widget, 1, 1, 1, 1, Qt.AlignLeft)

        desktop = QDesktopWidget()
        screen_size = desktop.screenGeometry(0).size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        if(mode!=2):
            seat_coordinates = sorted(self.coordinates)
            self.coordinates = seat_coordinates
            temp_coordinates = np.divide(seat_coordinates, 50) - 1
            temp_coordinates = temp_coordinates.tolist()
            temp_coordinates = [round(i) for i in temp_coordinates]
            print(temp_coordinates)

            if(mode):
                self.setFixedSize(screen_width / (1366 / 1200), screen_height / (768 / 250))
                side_widget.deleteLater()
                for r in range(10):
                    vertical_layout = QVBoxLayout()
                    vertical_widget = QWidget()
                    vertical_widget.setLayout(vertical_layout)
                    label = QLabel(str((r + 1) * 50))
                    vertical_layout.addWidget(label)
                    scene = QtWidgets.QGraphicsScene()
                    view = QtWidgets.QGraphicsView(scene)
                    view.setFixedSize(105,55)
                    rect = scene.addRect(0, 0, 100,  50)
                    pen = QtGui.QPen(QtCore.Qt.black)
                    brush = QtGui.QBrush(QtCore.Qt.gray)
                    if(r in temp_coordinates):
                        brush.setColor(QtCore.Qt.darkGreen)
                        self.canvas.append(rect)

                    rect.setPen(pen)
                    rect.setBrush(brush)
                    vertical_layout.addWidget(view)
                    seat_frame.addWidget(vertical_widget,0,r+1,1,1,Qt.AlignTop)
            else:
                # the laptop used have a resolution of 1366 768
                # so if 1366 is mapped to 500 and 768 is mapped to 650

                self.setFixedSize(screen_width / ( 1366/700), screen_height/(768/680))
                top_widget.deleteLater()
                for r in range(10):
                    label = QLabel(str((r + 1) * 50))
                    seat_frame.addWidget(label, r+3,0,1,1,Qt.AlignCenter)
                    scene = QtWidgets.QGraphicsScene()
                    view = QtWidgets.QGraphicsView(scene)
                    view.setFixedSize(105,55)
                    rect = scene.addRect(0, 0, 100,  50)
                    pen = QtGui.QPen(QtCore.Qt.black)
                    brush = QtGui.QBrush(QtCore.Qt.gray)
                    if(r in temp_coordinates):
                        brush.setColor(QtCore.Qt.darkGreen)
                        self.canvas.append(rect)

                    rect.setPen(pen)
                    rect.setBrush(brush)
                    seat_frame.addWidget(view, r+3, 1, 1, 1, Qt.AlignCenter)

        else:
            # self.setFixedSize(1000, 700)
            x_coordinates = self.coordinates[0::2]
            y_coordinates = self.coordinates[1::2]
            seat_coordinates = []
            for i in range(len(self.coordinates) // 2):
                seat_coordinates.append([x_coordinates[i], y_coordinates[i]])
            seat_coordinates = sorted(seat_coordinates)
            # need to assign it back to seat_coordinates
            self.coordinates = seat_coordinates
            temp_coordinates = np.divide(seat_coordinates, 50) - 1
            temp_coordinates = temp_coordinates.tolist()
            temp_coordinates = [[round(j) for j in i] for i in temp_coordinates]
            for c in range(10):
                label = QLabel(str((c + 1) * 50))
                seat_frame.addWidget(label,  2, c+1, 1, 1, Qt.AlignCenter)
            for r in range(10):
                label = QLabel(str((r+1) *50))
                seat_frame.addWidget(label,r+3,0)

                for c in range(10):
                    scene = QtWidgets.QGraphicsScene()
                    view = QtWidgets.QGraphicsView(scene)
                    view.setFixedSize(75, 55)
                    rect = scene.addRect(0, 0, 70, 50)
                    pen = QtGui.QPen(QtCore.Qt.black)
                    brush = QtGui.QBrush(QtCore.Qt.gray)
                    if ([r, c] in temp_coordinates):
                        brush.setColor(QtCore.Qt.darkGreen)
                        self.canvas.append(rect)

                    rect.setPen(pen)
                    rect.setBrush(brush)
                    seat_frame.addWidget(view, r + 3, c+1, 1, 1, Qt.AlignCenter)

    def back(self):
        self.hide()
        main_window.schema_selection_window.show()
    def start(self):
        main_window.matlab_thread.stop_event.clear()
        self.start_label.setText("SSH into RPI")
        stop_button = QPushButton("Stop", self)
        stop_button.setFont(QFont('Arial', 10))
        stop_button.clicked.connect(self.stop)
        stop_button.setContentsMargins(10, 10, 10, 10)
        self.rightFrame.addWidget(stop_button, 1, 0, 1, 1, Qt.AlignCenter)
        QApplication.processEvents() # Force GUI to update
        if(self.mode!=2):
            ssh_x = paramiko.SSHClient()
            ssh_x.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_x.connect(x_sensor_ip, 22, username="pi", password="raspberry", look_for_keys=False)
            channel = ssh_x.invoke_shell()
            self.start_label.setText("Running RADAR \n              &\n MATLAB CODE")
            radar_thread = Radar_Main_Thread([channel],self.coordinates,["z:/radar_x.csv"],
                                             main_window.matlab_thread.stop_event,self.canvas)
            radar_thread.start()
        else:
            ssh_x = paramiko.SSHClient()
            ssh_x.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_x.connect(x_sensor_ip, 22, username="pi", password="raspberry", look_for_keys=False)
            channelx = ssh_x.invoke_shell()

            ssh_y = paramiko.SSHClient()
            ssh_y.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_y.connect(y_sensor_ip, 22, username="pi", password="raspberry", look_for_keys=False)
            channely = ssh_y.invoke_shell()

            self.start_label.setText("Running RADAR \n              &\n MATLAB CODE")
            radar_thread = Radar_Main_Thread([channelx, channely], self.coordinates,
                                             ["z:/radar_x.csv", "Y:/radar_y.csv"],
                                             main_window.matlab_thread.stop_event, self.canvas)
            radar_thread.start()

    def stop(self):
        main_window.matlab_thread.stop_event.set()
        self.start_label.setText("Press Start to begin")
        start_button = QPushButton("Start", self)
        start_button.setFont(QFont('Arial', 10))
        start_button.clicked.connect(self.start)
        start_button.setContentsMargins(10, 10, 10, 10)
        self.rightFrame.addWidget(start_button, 1, 0, 1, 1, Qt.AlignCenter)
        QApplication.processEvents() # Force GUI to update
        print("Stopping")

def display_states(queue,coordinates,canvas):
    if(len(queue)==1):
        state = queue[0]
        for i in range(len(coordinates)):
                #     # this will give us the number of seat, and we can access the relevant frame
            if (state[i][-1] == 2):
                brush = QtGui.QBrush(QtCore.Qt.red)
                canvas[i].setBrush(brush)
            else:
                brush = QtGui.QBrush(QtCore.Qt.darkGreen)
                canvas[i].setBrush(brush)
    else:
        x_state = queue[0]
        y_state = queue[1]
        x_state = np.array(x_state)
        y_state = np.array(y_state)
        # min_size = min(len(x_state[0]),len(y_state[0]))
        sum_state = x_state+y_state
        # if both is 1 then the sum is 2 -> so it is available
        # if both is 2 then the sum is 4-> so it is not available
        # if the sum is 3 it is stationary in 1 d but not in the other
        # so there might be an error so we will label it as yellow
        for i in range(len(coordinates)):
            #     # this will give us the number of seat, and we can access the relevant frame
            if (sum_state[i][-1] == 4):
                brush = QtGui.QBrush(QtCore.Qt.red)
                canvas[i].setBrush(brush)
            elif (sum_state[i][-1] == 2):
                brush = QtGui.QBrush(QtCore.Qt.darkGreen)
                canvas[i].setBrush(brush)
            else:
                brush = QtGui.QBrush(QtCore.Qt.yellow)
                canvas[i].setBrush(brush)


# create the application
app = QApplication([])

# create the main window
main_window = MainWindow()

# show the main window
main_window.show()

# run the application
app.exec_()


