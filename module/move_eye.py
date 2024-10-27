from lib.lib import *
from time import sleep
import random
import json

config_file = './config/display_pos.json'
default = {
    "Limit": [-0.05, 0.05],
    "Time": [0.5, 1]
}
limit = default["Limit"]
time = default["Time"]


def __main__():
    global limit, time
    try:
        with open(config_file, 'r') as f:
            conf = json.load(f)
        limit = conf['Limit']
        time = conf['Time']
    except Exception as e:
        print("动眼模块配置文件异常，正在重置")
        print("错误代码：" + str(e))
        data = json.dumps(default, indent=4)
        with open(config_file, 'w') as f:
            f.write("\n" + data)

    sleep(0.5)
    data = dynamic["eyes"]
    static["running"]["move_eye"] = True
    while static["running"]["move_eye"]:
        x = random.uniform(limit[0], limit[1])
        y = random.uniform(limit[0], limit[1])
        data[0] = x
        data[1] = y
        sleep(random.uniform(time[0], time[1]))
    del static["running"]["move_eye"]
    return
