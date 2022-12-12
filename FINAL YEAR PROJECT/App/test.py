# import flet as ft
#
# def main(page: ft.Page):
#     page.title = "Flet counter example "
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
#
#     # 5 seats in both the x and y direction -> 1000/5 = 200 is the width and height of each
#
#     container_main = ft.Container(ft.Stack(),width=1000,height=1000,bgcolor="white")
#     # container_array = []
#     # for i in range(0,6):
#     #     container = ft.Container(width=200,height=200,bgcolor="red")
#     #     container_array.append(container)
#     def minus_click(e):
#         txt_number.value = str(int(txt_number.value) - 1)
#         page.update()
#
#     def plus_click(e):
#         txt_number.value = str(int(txt_number.value) + 1)
#         page.update()
#
#     # comtainer_main = ft.Row(container_array)
#     menu = ft.Column(
#             [
#                 ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
#                 ft.Icon(ft.icons.CIRCLE),
#                 txt_number,
#                 ft.IconButton(ft.icons.ADD, on_click=plus_click),
#             ] )
#
#     #
#     page.add(ft.Row( [container_main,menu]))
#     # page.add(ft.Row( [ comtainer_main,         ft.Column(
#     #         [
#     #             ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
#     #             ft.Icon(ft.icons.CIRCLE),
#     #             txt_number,
#     #             ft.IconButton(ft.icons.ADD, on_click=plus_click),
#     #         ]
#     #                     ) ] ) )
#
#
#
# ft.app(target=main)




# # testing grid view
# import flet as ft
#
# def main(page: ft.Page):
#     page.title = "GridView Example"
#     page.theme_mode = ft.ThemeMode.DARK
#     page.update()
#
#     grid = ft.GridView(
#         expand=1,
#         runs_count=10,
#         max_extent=110,
#         child_aspect_ratio=1.0,
#         spacing=0,
#         run_spacing=0,
#     )
#     container = ft.Container(grid,width=1000,height=1000)
#     page.add(container)
#
#     for i in range(0, 100):
#         if i%2==0:
#             colour = "blue"
#         else:
#             colour="red"
#         grid.controls.append(
#             ft.Container(width=10,height=10,bgcolor=colour)
#             )
#
#     page.update()
#
# ft.app(target=main)



# ussing tkinter for grid view
import tkinter
# import tkinter module

# creating main tkinter window/toplevel
import numpy as np
import tkinter as tk  # PEP8: `import *` is not preferred


# --- functions ---

def get_data():
    for r, row in enumerate(all_entries):
        for c, entry in enumerate(row):
            text = entry.get()
            demand[r, c] = float(text)

    print(demand)


# --- main ---

rows = 10
cols = 10

demand = np.zeros((rows, cols))

window = tk.Tk()

for c in range(cols):
    l = tk.Label(window, text=str(c))
    l.grid(row=0, column=c + 1)

all_entries = []
for r in range(rows):
    entries_row = []
    l = tk.Label(window, text=str(r + 1))
    l.grid(row=r + 1, column=0)
    for c in range(cols):

        Frame = tk.Frame(window, width=100,height=50)  # 5 chars
        w = tk.Canvas(Frame, width=100, height=50)
        w.create_rectangle(0, 0, 100, 100, fill="green") # these will represent the seats already
        w.pack()
        Frame.grid(row=r + 1, column=c + 1)
        entries_row.append(Frame)
    all_entries.append(entries_row)

b = tk.Button(window, text='GET DATA', command=get_data)
b.grid(row=rows + 1, column=0, columnspan=cols)

window.mainloop()