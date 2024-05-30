from lib import *
import os
import sys
from tkinter import *

path = "./src/"
il1 = None
il2 = None
il3 = None

speed = 5


def __main__():
    global il1, il2, il3
    dynamic['eyes'] = [0, 0]
    root = Tk()
    root.overrideredirect(True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if static["SYSINFO"] == "Windows":
        root.state('zoom')
    else:
        root.state('normal')
        root.attributes("-fullscreen", True)
    sys.path.append(path)
    files = os.listdir(path)
    print(f"./{path}/{files[0]}")
    il1 = PhotoImage(file=f"./{path}/{files[0]}")
    canvas = Canvas(root, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0, width=screen_width, height=screen_height)
    l1 = canvas.create_image(0, 0, image=il1, anchor=NW)

    canvas.moveto(l1, screen_width / 2 - il1.width() / 2, screen_height / 2 - il1.height() / 2)
    root.update()
    while 1:
        x = int(dynamic['eyes'][0] * screen_width / 2 + screen_width / 2 - il1.width() / 2)
        y = int(dynamic['eyes'][1] * screen_height / 2 + screen_height / 2 - il1.height() / 2)
        dx = (x - int(canvas.coords(l1)[0])) / speed
        dy = (y - int(canvas.coords(l1)[1])) / speed
        canvas.move(l1, dx, dy)
        root.update()
