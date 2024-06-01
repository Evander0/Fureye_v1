from lib.lib import *
import os
import importlib
import sys
import traceback
import threading
import subprocess
import platform
import json
import ctypes
global threads, loaded_plugins

plugin_suffix = "py"
path = os.path.join("module")
sys.path.append(path)
files = os.listdir(path)

config_file = './config/main.json'
default = {
    "Disabled": []
}


def pick_module(name):
    if name.endswith(plugin_suffix):
        return name.split(".")[0]
    else:
        return ""


def install(package):
    subprocess.check_call(["pip", "install", package])


def load_module(t_name):
    try:
        threads[t_name] = threading.Thread(target=loaded_plugins[t_name].__main__,
                                           name=t_name, daemon=True)
        threads[t_name].start()
        return threads[t_name]
    except Exception as e:
        print(f"Exception running module {t_name}: {e}")
        traceback.print_exc()
        return -1


def unload_module(t_name):
    t_id = threads[t_name].native_id
    print(t_id)
    try:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(t_id, ctypes.py_object(SystemExit))
        if res == 0:
            print("Invalid thread id!")
            return
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(threads[t_name], 0)
            print("Exception raise failure")
            return
    except Exception as e:
        print(f"Exception stopping module {t_name}: {e}")
        traceback.print_exc()
        return
    del threads[t_name]


def main_quit():
    for thread in threads:
        unload_module(thread)
    print("主程序终止")
    quit()


os_info = platform.system()
os_version = platform.version()
python_version = platform.python_version()
if python_version[0] != '3':
    print(f"Python version {python_version} not supported")
    exit(-1)
static["SYS_INFO"] = os_info
static["SYS_VER"] = os_version
static["PY_VER"] = python_version
disabled = []

plugins = map(pick_module, files)
plugins = [_ for _ in plugins if _ != ""]

if not os.path.exists('config'):
    print("正在创建配置文件夹")
    os.mkdir('config')
try:
    with open(config_file, 'r') as f:
        conf = json.load(f)
    disabled = conf['Disabled']
except Exception as e:
    print("模块管理器配置文件异常，正在重置")
    print("错误代码：" + str(e))
    data = json.dumps(default, indent=4)
    with open(config_file, 'w') as f:
        f.write("\n" + data)

print(f"System: {os_info}")
print(f"Python: {python_version}")
print(f"Disabled: {disabled}")

for name in plugins:
    if name not in disabled:
        try:
            loaded_plugins[name] = importlib.import_module(f"{path}.{name}")
        except ModuleNotFoundError:
            traceback.print_exc()
            continue
        except ImportError:
            traceback.print_exc()
            continue
        except Exception as e:
            print(f"Exception loading plugin {name}: {e}")
            traceback.print_exc()
            continue
        load_module(name)


while 1:
    try:
        command = input("$: ").split(" ")
        match command[0]:
            case "quit":
                try:
                    if command[1] in threads:
                        unload_module(command[1])
                    else:
                        print("未知模块")
                except IndexError:
                    main_quit()
            case "list":
                match command[1]:
                    case "plugins":
                        print(plugins)
                    case "threads":
                        print(threads)
            case _:
                print("未知指令")
    except IndexError:
        print("未知指令")
    except KeyboardInterrupt:
        main_quit()
