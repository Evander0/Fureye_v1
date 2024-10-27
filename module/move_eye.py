from lib.lib import *
import time
import random
import json

config_file = './config/display_pos.json'
default = {
    "Limit": [-0.05, 0.05],
    "Time": [0.5, 1]
}
limit = default["Limit"]
wtime = default["Time"]


def __init__():
    global limit, wtime
    try:
        with open(config_file, 'r') as f:
            conf = json.load(f)
        limit = conf['Limit']
        wtime = conf['Time']
    except Exception as e:
        print("动眼驱动模块配置文件异常，正在重置")
        print("错误代码：" + str(e))
        data = json.dumps(default, indent=4)
        with open(config_file, 'w') as f:
            f.write("\n" + data)
    while not static["running"]["eye_display"]:
        continue
    mdata = dynamic["eyes"]
    static["running"]["move_eye"] = True
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
