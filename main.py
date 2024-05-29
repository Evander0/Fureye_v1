import os
import importlib
import sys
import traceback
import threading

plugin_suffix = "py"
path = os.path.join("module")

sys.path.append(path)
files = os.listdir(path)
loaded_plugins: dict = {}
dynamic: dict = {}
static: dict = {}
threads: dict = {}
command: str = ""


def pick_module(name):
    if name.endswith(plugin_suffix):
        return name.split(".")[0]
    else:
        return ""


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
        threads[name] = threading.Thread(target=loaded_plugins[name].__main__, name=name,
                                         args=(dynamic, static, threads), daemon=True)
        threads[name].start()
    except Exception as e:
        print(f"Exception running plugin {name}: {e}")
        traceback.print_exc()
        continue

while 1:
    continue
