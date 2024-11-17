from lib.lib import *
import lib.command as comm
import os
import importlib
import sys
import traceback
import threading
import subprocess
import platform
import json
import ctypes
import time
global threads, loaded_plugins

plugin_suffix = "py"
path = os.path.join("module")
sys.path.append(path)
files = os.listdir(path)

config_file = 'config/main.json'
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
        static["running"][t_name] = False
        threads[t_name] = threading.Thread(target=loaded_plugins[t_name].__init__,
                                           name=t_name, daemon=True)
        threads[t_name].start()
        static["running"][t_name] = False
        return threads[t_name]
    except Exception as e:
        print(f"Exception running module {t_name}: {e}")
        traceback.print_exc()
        return -1


def unload_module(t_name):
    t_id = threads[t_name].ident
    print(t_id)
    static["running"][t_name] = False
    threads[t_name].join(timeout=5)
    if threads[t_name].is_alive():
        print("soft quit failed")
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
        schedule = time.time() + 5
        while time.time() <= schedule:
            if not threads[t_name].is_alive():
                del threads[t_name]
                print(f"{t_name} quit")
                break
        if threads[t_name].is_alive():
            print(f"failed to quit {t_name}")
    else:
        del threads[t_name]
        print(f"{t_name} quit")
        return


def quit_all():
    try:
        tmp = threads.copy()
        for thread in tmp:
            unload_module(thread)
    except:
        pass


def thread_watcher():
    while True:
        for i in list(threads):
            if not threads[str(i)].is_alive():
                threads.pop(i)
                del static["running"][str(i)]
                err_output.write(f"\rThread {i} closed\n")
                err_output.flush()
                print(f"Thread {i} closed", file=sys.stderr)
                time.sleep(0.1)
                raw_output.write("\r$: ")
                raw_output.flush()
        time.sleep(1)


def check_log():
    num = 0
    while True:
        log_file = f"logs/{time.strftime('%Y-%m-%d', time.localtime())}-{num}.log"
        if not os.path.isfile(log_file):
            return log_file
        else:
            num += 1


def logger(msg):
    if msg == "\n":
        log.write("\n")
    elif msg not in ["", " ", "\r"]:
        msg.replace("\n", "")
        log.write(msg)
        log.flush()


class err_handler:
    thread_closed = False

    def __init__(self):
        self.old_stm = sys.stderr

    def write(self, msg):
        if str(msg).startswith("Exception in thread"):
            logger(msg)
            self.thread_closed = True
        elif self.thread_closed:
            thread = str(msg)
            self.old_stm.write(f"\rThread {thread} raised an exception\n")
            self.old_stm.flush()
            time.sleep(0.1)
            raw_output.write("$: ")
            raw_output.flush()
            logger(msg)
            self.thread_closed = False
        else:
            logger(msg)

    def flush(self):
        self.old_stm.flush()


class log_handler:
    def __init__(self):
        self.old_stm = sys.stdout

    def write(self, msg):
        self.old_stm.write('\r'+msg)
        logger(msg)

    def flush(self):
        self.old_stm.flush()


def command_handler(command):
    match command[0]:
        case "quit":
            try:
                if command[1] in threads:
                    unload_module(command[1])
                else:
                    print("未知模块")
            except IndexError:
                quit_all()
                print("主程序终止")
                quit()
        case "list":
            match command[1]:
                case "plugins":
                    print(plugins)
                case "threads":
                    print(threads)
                case _:
                    print("未知指令(plugins/threads)")
        case "command":
            match command[1]:
                case "unregister":
                    comm.unregister(command[2])
                case _:
                    print("未知指令(unregister)")


if not os.path.exists('logs'):
    print("正在创建日志文件夹")
    os.mkdir('logs')
if not os.path.exists('config'):
    print("正在创建配置文件夹")
    os.mkdir('config')
log = open(check_log(), "w+", encoding="utf-8")

raw_output = sys.stdout
err_output = sys.stderr
sys.stdout = log_handler()
sys.stderr = err_handler()

os_info = platform.system()
os_version = platform.version()
python_version = platform.python_version()
if python_version[0] != '3':
    print(f"Python version {python_version} not supported")
    exit(-1)
static["SYS_INFO"] = os_info
static["SYS_VER"] = os_version
static["PY_VER"] = python_version
static["running"] = {}
disabled = []
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

plugins = map(pick_module, files)
plugins = [_ for _ in plugins if _ != ""]
plugins_loadertemp = plugins
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

watchdog = threading.Thread(target=thread_watcher, name="watch_dog", daemon=True)
watchdog.start()
comm.register("core", command_handler)
while 1:
    try:
        raw_output.write("$: ")
        raw_output.flush()
        comm.command(input().split(" "))
    except KeyboardInterrupt:
        quit_all()
        print("主程序终止")
        quit()
