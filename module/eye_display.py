import json
import sys
from time import sleep
from tkinter import *
from lib.lib import *

config_file = './config/display.json'
default = {
    "Path": "src",
    "Layer": ["eye_l1"],
    "Speed": 2
}
path = default["Path"]
file = default["Layer"]
speed = default["Speed"]
files: list = []
layer: list = []
screen_width = 0
screen_height = 0
index = -1


def __main__():
    global files, layer, file, path, speed, screen_width, screen_height, canvas

    try:
        with open(config_file, 'r') as f:
            conf = json.load(f)
        path = conf['Path']
        file = conf['Layer']
        speed = conf['Speed']
    except Exception as e:
        print("显示模块配置文件异常，正在重置")
        print("错误代码："+str(e))
        data = json.dumps(default, indent=4)
        with open(config_file, 'w') as f:
            f.write("\n"+data)

    dynamic['eyes'] = [0, 0]
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.overrideredirect(True)
    root.config(cursor="none")
    root.geometry(f'{screen_width}x{screen_height}')
    canvas = Canvas(root, width=screen_width, height=screen_height)
    if static["SYSINFO"] == "Windows":
        root.state('zoom')
    else:
        root.state('normal')
        root.attributes("-fullscreen", True)

    sys.path.append(path)
    load(file[0])
    canvas.place(x=0, y=0, width=screen_width, height=screen_height)
    while 1:
        x = int(dynamic['eyes'][0] * screen_width / 2 + screen_width / 2 - files[index].width() / 2)
        y = int(dynamic['eyes'][1] * screen_height / 2 + screen_height / 2 - files[index].height() / 2)
        dx = (x - int(canvas.coords(layer[0])[0])) / (10/speed)
        dy = (y - int(canvas.coords(layer[0])[1])) / (10/speed)
        canvas.move(layer[0], dx, dy)
        root.update()
        sleep(0.02)


def load(name):
    global index, files, layer
    index = index + 1
    files.append(PhotoImage(file=f"./{path}/{name}.png"))
    layer.append(canvas.create_image(0, 0, image=files[index], anchor=NW))
    canvas.moveto(layer[0], screen_width / 2 - files[index].width() / 2, screen_height / 2 - files[index].height() / 2)
