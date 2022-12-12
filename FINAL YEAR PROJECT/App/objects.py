import flet as ft
def main(page: ft.Page):
    page.title = "outline test "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # create a space for the room -> create a container

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                ft.Icon(ft.icons.CIRCLE),
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)



# this instance represent the room
# the room has 1 property which is the chairs that are stored within that room
# for 2 d room, the coordinate array will be a tuple of x and y coordinate
# the style shows the format of the room is it 1d in the x or y and is it 2d
class room:
    def __init__(self,coordinate_array,style):
        if(style=="x"):
            for i in range(0,len(coordinate_array)):
                local_chair = chair(coordinate_array[i],15);
        elif(style=="y"):
            for i in range(0,len(coordinate_array)):
                local_chair = chair(15,coordinate_array[i]);
        else:
            for i in range(0,len(coordinate_array)):
                coordinate = coordinate_array[i]
                local_chair = chair(coordinate[0],coordinate[1]);





# this is the chair class represent an instance of a chair
# the chair will have 3 properties: the x coordinate, y coodinate and the status
# the status will follow 3 states -> available, unavailable and maybe
class chair:

    def __init__(self,x_coordinate,y_coordinate):
	    # initializations
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.status = "Available"



