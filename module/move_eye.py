from lib.lib import *
from lib.config import Config
import time
import random

default = {
    "Limit": [-0.05, 0.05],
    "Time": [0.5, 1]
}


def __init__():
    global limit, wtime

    config = Config("display_pos", default)
    conf = config.read()
    limit = conf["Limit"]
    wtime = conf["Time"]

    while not static["running"]["eye_display"]:
        continue
    mdata = dynamic["eyes"]
    static["running"]["move_eye"] = True
    dynamic['eyes'][0]["enabled"] = True
    while static["running"]["move_eye"]:
        x = random.uniform(limit[0], limit[1])
        y = random.uniform(limit[0], limit[1])
        schedule = time.time() + random.uniform(wtime[0], wtime[1])
        while time.time() <= schedule:
            mdata[0]["x"] += (x - mdata[0]["nx"]) / 20
            mdata[0]["y"] += (y - mdata[0]["ny"]) / 20
            time.sleep(0.01)
    del static["running"]["move_eye"]
    return
