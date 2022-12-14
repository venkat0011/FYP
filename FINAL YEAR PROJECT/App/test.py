# the app will have the overall flow like this
# the main page to indicate which type of sensors to be experimented on
# then it will direct to the next frame ( use the frame method here )
# the next frame will have different options which will indicate which schema type they want
# after the schema type is asked for it will ask to enter the number of chairs and thier coordinates
# it will direct to the new window which will display the seats in a 5m by 5m display and highlighting those seats in green
# next to it should be the start and stop buttons -> they can change their view from this page as well and it will redirect the same question

import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
import math
import matlab.engine
import _thread

LARGEFONT = ("Verdana", 15)


class Button:
    """button1 = Button("Testo", "4ce", 0, 0)"""

    def __init__(self, window, text, func, size, row, col, image, padx, pady):
        image2 = Image.open(image)
        image3 = image2.resize(size)
        image3 = ImageTk.PhotoImage(image3)
        self.button = ttk.Button(
            window,
            text=text,
            image=image3,
            compound=tk.TOP,
            command=func)
        # self.button.pack()
        self.button.grid(row=row, column=col, sticky=tk.NW, padx=padx, pady=pady)
        self.button.image = image3



def display_window(old_window, new_window):
    old_window.withdraw()
    new_window.deiconify()


def start_ir_uwb(button_frame,seat_coordinates,seat_canvas,seat_frame):
    progress_label = ttk.Label(button_frame,text="Press the button below to start the sensors")
    progress_label.grid(row=0,column=0)
    stop_button = ttk.Button(button_frame,text="Stop",command=stop_ir_uwb(button_frame))
    stop_button.grid(row=1,column=0)
    button_frame.update()
    # check the seat coordinates
    # ssh into the rpi

    #download the file from rpi

    # run the matlab code and obtain the state of each seat
    state = eng.IR_UWB_function(matlab.int32(seat_coordinates)) # nice to know which stage it is at -> like is it at ssh into it or running matlab code
    # # we will be displaying the last known information
    # # the result return is a list of list so to get the states we need [0] and we will use[-1] to get the last known state
    for i in range(len(seat_coordinates)):
    #     # this will give us the number of seat, and we can access the relevant frame
        if(state[i][-1]==2):
            seat_canvas[i].create_rectangle(0, 0, 100, 100, fill="red")

def stop_ir_uwb(button_frame):
    start_button = ttk.Button(button_frame, text="Start", command=lambda: start_ir_uwb(button_frame))
    start_button.grid(row=0, column=0)
    return

def display_schema(mode, entry_list, text_label,entry_window,schema_window):
    # the overall structure will be the same but the schema will change based on the
    print("button pressed")  # need to check the input to see if it is between 50cm and 500 cm
    coordinates = check_coordinates(50,500,entry_list)
    seat_canvas = []
    if (type(coordinates) != list ):
        if("Invalid" not in text_label["text"]):
            text_label["text"] = "Invalid Input, please enter a range between 50cm to 500cm\n" + text_label['text']
    else:
        # we need to sort the coordinates -> the way we sort will depend on the mode to visualise it later on and for the matlab code
        entry_window.withdraw()
        seat_window = tk.Toplevel(schema_window)
        seat_window.title("Seating Arrangement")
        display_window(schema_window,seat_window)

        top_frame = ttk.Frame(seat_window)
        x_arrow = Image.open("x_arrow.png")
        x_arrow = x_arrow.resize((500, 50))
        x_arrow = ImageTk.PhotoImage(x_arrow)
        x_label_arrow = ttk.Label(top_frame, image=x_arrow)
        x_label_arrow.image = x_arrow
        x_label_arrow.grid(row=1, column=6)
        x_label = ttk.Label(top_frame, text="Distance from the sensor in the X direction")
        x_label.grid(row=0, column=6)
        back_button = ttk.Button(seat_window, text="Back", command=lambda: display_window(seat_window, schema_window))
        back_button.grid(row=0, column=0)
        top_frame.grid(row=0, column=1)

        side_frame = ttk.Frame(seat_window)
        y_arrow = Image.open("y_arrow.png")
        y_arrow = y_arrow.resize((50, 500))
        y_arrow = ImageTk.PhotoImage(y_arrow)
        y_arrow_label = ttk.Label(side_frame, image=y_arrow)
        y_arrow_label.image = y_arrow
        y_arrow_label.grid(row=6, column=1)
        y_label = ttk.Label(side_frame, text="Distance from the sensor in the Y direction")
        y_label.grid(row=0, column=1)
        side_frame.grid(row=1, column=0)


        seat_frame = ttk.Frame(seat_window)
        seat_frame.grid(row=1, column=1)

        if(mode!=2):
            seat_coordinates = sorted(coordinates)
            temp_coordinates = np.floor_divide(seat_coordinates,50) -1
            temp_coordinates = temp_coordinates.tolist()
            print(temp_coordinates)
            if(mode==0):
                top_frame.destroy()
                for r in range(10):
                    l = tk.Label(seat_frame, text=str((r + 1) * 50))
                    l.grid(row=r + 3, column=0)
                    Frame = tk.Frame(seat_frame, width=100, height=50)  # 5 chars
                    w = tk.Canvas(Frame, width=100, height=50)
                    if(r in temp_coordinates):
                        fill = "green"
                        seat_canvas.append(w)
                    else:
                        fill = "grey"
                    w.create_rectangle(0, 0, 100, 100, fill=fill)
                    w.pack()
                    Frame.grid(row=r+3, column=5)
            else:
                side_frame.destroy()
                for r in range(10):
                    l = tk.Label(seat_frame, text=str((r + 1) * 50))
                    l.grid(row=3, column=r+1)
                    Frame = tk.Frame(seat_frame, width=100, height=50)  # 5 chars
                    w = tk.Canvas(Frame, width=100, height=50)
                    if(r in temp_coordinates):
                        fill = "green"
                        seat_canvas.append(w)
                    else:
                        fill = "grey"
                    w.create_rectangle(0, 0, 100, 100, fill=fill)
                    w.pack()
                    Frame.grid(row=5, column=r+1)

        # for 2 dimensional space we will create 2 list x coordinates and y coordinates and send it to the matlab code repectively
        else:
            x_coordinates = coordinates[0::2]
            y_coordinates = coordinates[1::2]
            seat_coordinates = []
            for i in range(len(coordinates)//2):
                seat_coordinates.append( [ x_coordinates[i], y_coordinates[i] ] )

        # schema on the seat window depends on the mode
            seat_coordinates = sorted(seat_coordinates)
        # 5m by 5m is equally split into 100 seats -> so first thing is to find which block does each one of them belong to
        # the top frame is common for all
            for c in range(10):
                l = tk.Label(seat_frame, text=str((c+1) * 50))
                l.grid(row=2, column=c + 1,pady=10)
            temp_coordinates = np.floor_divide(seat_coordinates,50) -1
            temp_coordinates = temp_coordinates.tolist()
            for r in range(10):
                l = tk.Label(seat_frame, text=str((r+1) * 50))
                l.grid(row=r + 3, column=0)
                for c in range(10):
                    Frame = tk.Frame(seat_frame, width=100, height=50)  # 5 chars
                    w = tk.Canvas(Frame, width=100, height=50)
                    # find the seats based on the seat array -> store these canvas in an array so we can change the colour later on
                    if([r,c] in temp_coordinates):
                        fill = "green"
                        seat_canvas.append(w)
                    else:
                        fill = "grey"
                    w.create_rectangle(0, 0, 100, 100, fill=fill)
                    w.pack()
                    Frame.grid(row=r + 3, column=c + 1)

            # create a new frame to position all the buttons and stuff
        button_frame = ttk.Frame(seat_window)
        start_button = ttk.Button(button_frame, text="Start",
                                  command=lambda: start_ir_uwb(button_frame, seat_coordinates, seat_canvas,
                                                               seat_frame))
        start_button.grid(row=0, column=0)
        button_frame.grid(row=1, column=2)



def check_coordinates(min_range,max_range,entry_list):
    try:
        temp = []
        for i in entry_list:
            number = int(i.get())
            if (number >= min_range and number <= max_range):
                temp.append(number)
            else:
                return False
        return temp
    except:
        return False


def display_schema_choice(parent_window):
    # display the schema type to test for ir-uwb

    # this window needs to have the 3 schema types and once they click on each of the schemas they need to enter the coordinate
    # and a back button to go back home
    new_window = tk.Toplevel(parent_window)
    display_window(parent_window, new_window)
    new_window.title("IR-UWB")
    Frame = ttk.Frame(new_window)
    Frame.grid(row=0, column=0)
    label = ttk.Label(Frame, text="Please select the orientation of the seats", font=LARGEFONT)
    label.grid(row=0, column=1, padx=10, pady=10)

    # button to show frame 2 with text
    # layout2
    button1 = ttk.Button(Frame, text="Home Page",
                         command=lambda: display_window(new_window, parent_window))

    # putting the button in its place
    # by using grid
    button1.grid(row=0, column=0, padx=0, pady=0)

    # # display the 3 different orientation
    Button(Frame, "Y Direction", lambda: get_coordinates(0, new_window), (60, 266), 1, 0, "y_direction.png", 20, 20)
    Button(Frame, "X Direction", lambda: get_coordinates(1, new_window), (300, 40), 1, 1, "x_direction.png", 35, 140)
    Button(Frame, "2 Dimension", lambda: get_coordinates(2, new_window), (106, 200), 1, 2, "2d_space.png", 30, 50)


def get_coordinates(mode, parent_window):
    # get the total number of seats
    new_window = tk.Toplevel(parent_window)
    new_window.title("Seat input")
    label = ttk.Label(new_window, text="Enter the number of seats  from 1 to 10 ( press enter once done)")
    label.grid(row=0, column=0)
    seat_input = ttk.Entry(new_window)
    seat_input.insert('end', 0)
    seat_input.grid(row=1, column=0)

    def print_seat(event):
        # check the number of seats first
        test = check_coordinates(1,10,[seat_input])
        if(type(test)!= list):
            label["text"] = "Please enter a valid number of seats"
        else:
            if (mode == 0):
                text = "Enter the y coordinates of the seats in cm and click the next button to continue"
            elif (mode == 1):
                text = "Enter the x coordinates of the seats in cm and click the next button to continue"
            else:
                text = "Enter the x and y coodinates of the seats in cm and click the next button to continue"
            label['text'] = text
            number_of_seats = int(seat_input.get())
            seat_input.destroy()
            entry_list = []  # need to reset the coordiante everytime this is called
            if (mode != 2):

                for i in range(number_of_seats):
                    l = ttk.Label(new_window, text="seat number " + str(i + 1))
                    l.grid(row=i + 2, column=0)
                    e = tk.Entry(new_window, width=5)  # 5 chars
                    e.insert('end', 0)
                    e.grid(row=i + 2, column=1)
                    entry_list.append(e)
            else:
                for i in range(number_of_seats):
                    l = ttk.Label(new_window, text="seat number " + str(i + 1))
                    l.grid(row=i + 3, column=0)
                    label2 = ttk.Label(new_window, text="X Coordinate")
                    label2.grid(row=1, column=1, pady=15)
                    label3 = ttk.Label(new_window, text="Y Coodinates")
                    label3.grid(row=1, column=2, pady=15)
                    e = tk.Entry(new_window, width=5)  # 5 chars
                    e.insert('end', 0)
                    e.grid(row=i + 3, column=1)

                    e1 = tk.Entry(new_window, width=5)  # 5 chars
                    e1.insert('end', 0)
                    e1.grid(row=i + 3, column=2)
                    entry_list.append(e)
                    entry_list.append(e1)

            # add in the button that will get all the input from the entry box
            # destroy this old window and get the parent window in the background ( which will be the schema choices)
            # display the new window which will show the schema chosen in a big frame with the start and stop  buttons at the side
            # and a home page button at the top, once we click start -> it should either turn to a stop button or the button is unclickable
            # below it will be the schema choices and once those are clicked we will display this window again

            button = ttk.Button(new_window, text="Next", command=lambda: display_schema(mode, entry_list,label,new_window,parent_window))
            button.grid(row=number_of_seats + 4, column=3)

    seat_input.bind('<Return>', print_seat)


# using window method

main_app = tk.Tk()
main_app.title("welcome")
label = ttk.Label(main_app, text="Occupancy Sensing Using RF sensing", font=LARGEFONT)
label.grid(row=0, column=4, padx=10, pady=10)
label1 = ttk.Label(main_app, text="Please wait, the app is connecting to MATLAB")
label1.grid(row=1, column=4, padx=10, pady=10)
main_app.update()
eng = matlab.engine.start_matlab()
label1["text"] = "Please select the type of RF sensor to be used"
button1 = ttk.Button(main_app, text="Ir-uwb",
                     command=lambda: display_schema_choice(main_app))

button1.grid(row=3, column=4, padx=10, pady=10)
main_app.update()

#
# ## button to show frame 2 with text layout2
# button2 = ttk.Button(main_app, text="Page 2",
#                      command=lambda: controller.show_frame(Page2))
#
# # putting the button in its place by
# # using grid
# button2.grid(row=4, column=4, padx=10, pady=10)
main_app.mainloop()
