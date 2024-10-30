import json
import sys
import pathlib
from time import sleep
from tkinter import *
from lib.lib import *
from PIL import Image, ImageTk

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
            if dynamic['eyes'][i]["enabled"]:
                x = int(dynamic['eyes'][i]["x"] * screen_width / 2 + screen_width / 2 - files[i][dynamic['eyes'][index]["selected"]].width() / 2)
                y = int(dynamic['eyes'][i]["y"] * screen_height / 2 + screen_height / 2 - files[i][dynamic['eyes'][index]["selected"]].height() / 2)
                dynamic['eyes'][i]["nx"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][index]["selected"]])[0]) - screen_width / 2 + files[
                                                i][dynamic['eyes'][index]["selected"]].width() / 2) / screen_width * 2
                dynamic['eyes'][i]["ny"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][index]["selected"]])[1]) - screen_height / 2 + files[
                                                i][dynamic['eyes'][index]["selected"]].height() / 2) / screen_height * 2
                if len(layer[i]) > 1:
                    for j in layer[i]:
                        canvas.moveto(j, screen_width, screen_height)
                canvas.moveto(layer[i][dynamic['eyes'][index]["selected"]], x, y)
            else:
                for j in layer[i]:
                    canvas.moveto(j, screen_width, screen_height)
        sleep(0.02)
        root.update()
    canvas.destroy()
    root.destroy()
    del static["running"]["eye_display"]
    return


def load(name):
    global index, files, layer, path
    index = index + 1
    dynamic['eyes'].insert(index, {})
    dynamic['eyes'][index]["x"] = 0
    dynamic['eyes'][index]["y"] = 0
    dynamic['eyes'][index]["nx"] = 0
    dynamic['eyes'][index]["ny"] = 0
    dynamic['eyes'][index]["selected"] = 0
    dynamic['eyes'][index]["enabled"] = False

    file = pathlib.Path(list(pathlib.Path(f"./{path}").glob(f'{name}.*'))[0])
    files.append([])
    layer.append([])
    match file.suffix:
        case ".png" | ".jpg":
            img = Image.open(file)
            files[index].append(ImageTk.PhotoImage(img))
            layer[index].append(canvas.create_image(0, 0, image=files[index][0], anchor=NW))
            canvas.moveto(layer[index][0], screen_width / 2 - files[index][0].width() / 2,
                          screen_height / 2 - files[index][0].height() / 2)
        case ".gif":
            img = Image.open(file)
            for i in range(img.n_frames):
                img.seek(i)
                files[index].append(ImageTk.PhotoImage(img))
                layer[index].append(canvas.create_image(0, 0, image=files[index][i], anchor=NW))
                canvas.moveto(layer[index][i], screen_width / 2 - files[index][i].width() / 2,
                              screen_height / 2 - files[index][i].height() / 2)
        case _:
            print(f"Not supported file type: {file.suffix}")
