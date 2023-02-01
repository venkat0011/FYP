#
# #
#
#
# # follow this structure for the tkinter app
# import tkinter as tk
# from tkinter import ttk
#
# LARGEFONT = ("Verdana", 35)
#
#
# class tkinterApp(tk.Tk):
#
#     # __init__ function for class tkinterApp
#     def __init__(self, *args, **kwargs):
#         # __init__ function for class Tk
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         # creating a container
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         # initializing frames to an empty array
#         self.frames = {}
#
#         # iterating through a tuple consisting
#         # of the different page layouts
#         for F in (StartPage, Page1, Page2):
#             frame = F(container, self)
#
#             # initializing frame of that object from
#             # startpage, page1, page2 respectively with
#             # for loop
#             self.frames[F] = frame
#
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame(StartPage)
#
#     # to display the current frame passed as
#     # parameter
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()
#
#
# # first window frame startpage
#
# class StartPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#
#         # label of frame Layout 2
#         label = ttk.Label(self, text="Startpage", font=LARGEFONT)
#
#         # putting the grid in its place by using
#         # grid
#         label.grid(row=0, column=4, padx=10, pady=10)
#
#         button1 = ttk.Button(self, text="Page 1",
#                              command=lambda: controller.show_frame(Page1))
#
#         # putting the button in its place by
#         # using grid
#         button1.grid(row=1, column=1, padx=10, pady=10)
#
#         ## button to show frame 2 with text layout2
#         button2 = ttk.Button(self, text="Page 2",
#                              command=lambda: controller.show_frame(Page2))
#
#         # putting the button in its place by
#         # using grid
#         button2.grid(row=2, column=1, padx=10, pady=10)
#
#
# # second window frame page1
# class Page1(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text="Page 1", font=LARGEFONT)
#         label.grid(row=0, column=4, padx=10, pady=10)
#
#         # button to show frame 2 with text
#         # layout2
#         button1 = ttk.Button(self, text="StartPage",
#                              command=lambda: controller.show_frame(StartPage))
#
#         # putting the button in its place
#         # by using grid
#         button1.grid(row=1, column=1, padx=10, pady=10)
#
#         # button to show frame 2 with text
#         # layout2
#         button2 = ttk.Button(self, text="Page 2",
#                              command=lambda: controller.show_frame(Page2))
#
#         # putting the button in its place by
#         # using grid
#         button2.grid(row=2, column=1, padx=10, pady=10)
#
#
# # third window frame page2
# class Page2(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text="Page 2", font=LARGEFONT)
#         label.grid(row=0, column=4, padx=10, pady=10)
#
#         # button to show frame 2 with text
#         # layout2
#         button1 = ttk.Button(self, text="Page 1",
#                              command=lambda: controller.show_frame(Page1))
#
#         # putting the button in its place by
#         # using grid
#         button1.grid(row=1, column=1, padx=10, pady=10)
#
#         # button to show frame 3 with text
#         # layout3
#         button2 = ttk.Button(self, text="Startpage",
#                              command=lambda: controller.show_frame(StartPage))
#
#         # putting the button in its place by
#         # using grid
#         button2.grid(row=2, column=1, padx=10, pady=10)
#
#
# # Driver Code
# app = tkinterApp()
# app.mainloop()
#
#
#
# # this changing between the frames should be done with the schema page itself since all will follow the same structure
# # but for the main app page and the schema page it might be better to use it as a window
from operator import itemgetter
# import numpy as np
# array = [50,230]
# array = np.floor_divide(array,50) -1
# # sorted_li = sorted(array)
# # print(sorted_li)
# if([0,0] in array):
#     print("sye")
from apscheduler.schedulers.background import BackgroundScheduler

import time
import threading

# Define the stop function
def stop_function():
    return True

# Define the loop function
def loop_function(stop_event: threading.Event):
    while not stop_event.is_set():
        print("Loop running...")

# Define the second task function
def second_task(stop_event: threading.Event):
    while not stop_event.is_set():
        print("Second task")

stop_event = threading.Event()

# Create a thread for the loop function
loop_thread = threading.Thread(target=loop_function, args=(stop_event,))

# Create a thread for the second task function
second_thread = threading.Thread(target=second_task, args=(stop_event,))

# Start the loop thread
loop_thread.start()
time.sleep(0.4)
# Start the second thread
second_thread.start()

# Wait for the stop function to be called
# while not stop_function():
#     pass
time.sleep(5)
# Set the stop event
stop_event.set()

# Join the loop thread
loop_thread.join()

# Join the second thread
second_thread.join()


# sched.add_job(lambda :second_task(sched),"interval",seconds=0.5)
# Start the scheduler
# while True:
#     sched.start()
#     #wait for the scheduler to stop
#     sched.join()

# Wait for some time before stopping the loop
# time.sleep(30)
#
# # Stop the loop
# break_loop(sched)