import json
import sys
from time import sleep
from tkinter import *
from lib.lib import *

config_file = './config/display.json'
default = {
    "Path": "src",
    "Layer": ["eye_l1"],
}
path = default["Path"]
file = default["Layer"]
files: list = []
layer: list = []
screen_width = 0
screen_height = 0
index = -1


def __init__():
    global files, layer, file, path, screen_width, screen_height, canvas

    try:
        with open(config_file, 'r') as f:
            conf = json.load(f)
        path = conf['Path']
        file = conf['Layer']
    except Exception as e:
        print("动眼显示模块配置文件异常，正在重置")
        print("错误代码：" + str(e))
        data = json.dumps(default, indent=4)
        with open(config_file, 'w') as f:
            f.write("\n" + data)

    dynamic['eyes'] = []
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.overrideredirect(True)
    root.config(cursor="none")
    root.geometry(f'{screen_width}x{screen_height}')
    canvas = Canvas(root, width=screen_width, height=screen_height)
    if static["SYS_INFO"] == "Windows":
        root.state('zoom')
    else:
        root.state('normal')
        root.attributes("-fullscreen", True)

    sys.path.append(path)
    for f in file:
        load(f)
    canvas.place(x=0, y=0, width=screen_width, height=screen_height)
    static["running"]["eye_display"] = True
    while static["running"]["eye_display"]:
        for i in range(index + 1):
            x = int(dynamic['eyes'][i]["x"] * screen_width / 2 + screen_width / 2 - files[i].width() / 2)
            y = int(dynamic['eyes'][i]["y"] * screen_height / 2 + screen_height / 2 - files[i].height() / 2)
            dynamic['eyes'][i]["nx"] = (int(canvas.coords(layer[i])[0]) - screen_width / 2 + files[i].width() / 2) / screen_width * 2
            dynamic['eyes'][i]["ny"] = (int(canvas.coords(layer[i])[1]) - screen_height / 2 + files[i].height() / 2) / screen_height * 2
            dx = (x - int(canvas.coords(layer[i])[0]))
            dy = (y - int(canvas.coords(layer[i])[1]))
            canvas.move(layer[i], dx, dy)
        sleep(0.02)
        root.update()
    canvas.destroy()
    root.destroy()
    del static["running"]["eye_display"]
    return


def load(name):
    global index, files, layer
    index = index + 1
    dynamic['eyes'].insert(index, {})
    dynamic['eyes'][index]["x"] = 0
    dynamic['eyes'][index]["y"] = 0
    dynamic['eyes'][index]["nx"] = 0
    dynamic['eyes'][index]["ny"] = 0
    files.append(PhotoImage(file=f"./{path}/{name}.png"))
    layer.append(canvas.create_image(0, 0, image=files[index], anchor=NW))
    canvas.moveto(layer[index], screen_width / 2 - files[index].width() / 2,
                  screen_height / 2 - files[index].height() / 2)
