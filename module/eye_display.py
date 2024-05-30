from lib import *
from time import sleep
import sys
from tkinter import *

path = "src"
file = "eye_l1"
files: list = []
layer: list = []
index = -1
screen_width = 0
screen_height = 0
speed = 5


def __main__():
    global files, layer, screen_width, screen_height, canvas
    dynamic['eyes'] = [0, 0]
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.overrideredirect(True)
    root.geometry(f'{screen_width}x{screen_height}')
    canvas = Canvas(root, width=screen_width, height=screen_height)
    if static["SYSINFO"] == "Windows":
        root.state('zoom')
    else:
        root.state('normal')
        root.attributes("-fullscreen", True)

    sys.path.append(path)
    load(file)
    canvas.place(x=0, y=0, width=screen_width, height=screen_height)
    while 1:
        x = int(dynamic['eyes'][0] * screen_width / 2 + screen_width / 2 - files[index].width() / 2)
        y = int(dynamic['eyes'][1] * screen_height / 2 + screen_height / 2 - files[index].height() / 2)
        dx = (x - int(canvas.coords(layer[0])[0])) / speed
        dy = (y - int(canvas.coords(layer[0])[1])) / speed
        canvas.move(layer[0], dx, dy)
        root.update()
        sleep(0.02)


def load(name):
    global index, files, layer
    index = index+1
    files.append(PhotoImage(file=f"./{path}/{name}.png"))
    layer.append(canvas.create_image(0, 0, image=files[index], anchor=NW))
    canvas.moveto(layer[0], screen_width / 2 - files[index].width() / 2, screen_height / 2 - files[index].height() / 2)
