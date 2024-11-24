import glob
import sys
import pathlib
from time import sleep
from tkinter import *
from lib.lib import *
from lib.config import Config
from PIL import Image, ImageTk

default = {
    "Path": "src",
    "Layer": ["eye_l1"],
    "Scale": ["1"],
}
files: list = []
layer: list = []
screen_width = 0
screen_height = 0
index = -1


def __init__():
    global files, layer, screen_width, screen_height, path, conf, config, canvas
    config = Config("display", default)
    conf = config.read()
    path = conf["Path"]
    file = conf["Layer"]

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
                x = int(dynamic['eyes'][i]["x"] * screen_width / 2 + screen_width / 2 - files[i][
                    dynamic['eyes'][index]["selected"]].width() / 2)
                y = int(dynamic['eyes'][i]["y"] * screen_height / 2 + screen_height / 2 - files[i][
                    dynamic['eyes'][index]["selected"]].height() / 2)
                dynamic['eyes'][i]["nx"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][index]["selected"]])[0]) - screen_width / 2 + files[i][
                                                dynamic['eyes'][index]["selected"]].width() / 2) / screen_width * 2
                dynamic['eyes'][i]["ny"] = (int(
                    canvas.coords(layer[i][dynamic['eyes'][index]["selected"]])[1]) - screen_height / 2 + files[i][
                                                dynamic['eyes'][index]["selected"]].height() / 2) / screen_height * 2
                if len(layer[i]) > 1:
                    for j in layer[i]:
                        canvas.moveto(j, screen_width, screen_height)
                canvas.moveto(layer[i][dynamic['eyes'][index]["selected"]], x, y)
            else:
                for j in layer[i]:
                    canvas.moveto(j, screen_width, screen_height)
        sleep(0.02)
        root.update()
    canvas.delete("all")
    canvas.destroy()
    root.destroy()
    return


def load(name):
    global index, files, layer
    try:
        file = pathlib.Path(list(glob.glob(f'{path}/{name}.*'))[0])
    except IndexError:
        print(f"File {name} not found")
        return -1

    index = index + 1
    dynamic['eyes'].insert(index, {})
    dynamic['eyes'][index]["x"] = 0
    dynamic['eyes'][index]["y"] = 0
    dynamic['eyes'][index]["nx"] = 0
    dynamic['eyes'][index]["ny"] = 0
    dynamic['eyes'][index]["selected"] = 0
    dynamic['eyes'][index]["enabled"] = False
    try:
        scale = int(float(conf["Scale"][index])*screen_height)
    except ValueError:
        scale = int(screen_height / 2)
    except IndexError:
        config.write({'Scale': conf["Scale"].insert(index, 1)})
        scale = int(screen_height / 2)
    files.append([])
    layer.append([])

    match file.suffix:
        case ".png" | ".jpg":
            img = Image.open(file)
            img = img.resize((int(img.size[0] * scale / img.size[1]), scale))
            files[index].append(ImageTk.PhotoImage(img))
            layer[index].append(canvas.create_image(0, 0, image=files[index][0], anchor=NW))
            canvas.moveto(layer[index][0], screen_width / 2 - files[index][0].width() / 2,
                          screen_height / 2 - files[index][0].height() / 2)
        case ".gif":
            img = Image.open(file)
            for i in range(img.n_frames):
                img.seek(i)
                frame = img.resize((int(img.size[0] * scale / img.size[1]), scale))
                files[index].append(ImageTk.PhotoImage(frame))
                layer[index].append(canvas.create_image(0, 0, image=files[index][i], anchor=NW))
                canvas.moveto(layer[index][i], screen_width / 2 - files[index][i].width() / 2,
                              screen_height / 2 - files[index][i].height() / 2)
        case _:
            print(f"Not supported file type: {file.suffix}")
