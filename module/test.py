from lib import *
import tkinter

data: list


def motion(event):
    x, y = event.x / 300 - 1, event.y / 300 - 1
    data[0] = x
    data[1] = y
    # print(f"{x}, {y}")


def __main__():
    return

    global data
    data = dynamic["eyes"]
    window = tkinter.Tk()
    window.attributes("-alpha", 1)
    window.geometry('600x600')
    window.config(background='#2B2D30')
    window.bind('<Motion>', motion)
    window.mainloop()
