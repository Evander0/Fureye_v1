from lib import *
import os
import importlib
import sys
import traceback
import threading
import subprocess
import platform

plugin_suffix = "py"
path = os.path.join("module")
sys.path.append(path)
files = os.listdir(path)


def pick_module(name):
    if name.endswith(plugin_suffix):
        return name.split(".")[0]
    else:
        return ""


def install(package):
    subprocess.check_call(["pip", "install", package])


os_info = platform.system()
os_version = platform.version()
python_version = platform.python_version()
if python_version[0] != '3':
    print(f"Python version {python_version} not supported")
    exit(-1)
static["SYSINFO"] = os_info
static["SYSVER"] = os_version
static["PYVER"] = python_version
print(os_info)

plugins = map(pick_module, files)
plugins = [_ for _ in plugins if _ != ""]
print(plugins)

for name in plugins:
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

for name in plugins:
    try:
        threads[name] = threading.Thread(target=loaded_plugins[name].__main__,
                                         name=name, daemon=True)
        threads[name].start()
    except Exception as e:
        print(f"Exception running plugin {name}: {e}")
        traceback.print_exc()
        continue

while 1:
    continue
