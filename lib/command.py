import sys

command_list: dict = {}


def register(command: str, process):
    command_list[command] = process


def unregister(command: str):
    command_list.pop(command)


def command(command: list):
    if command[0] == "":
        pass
    elif command[0] in command_list.keys():
        try:
            command_list[command[0]](command[1:])
        except Exception as e:
            print(e, file=sys.stderr)
    else:
        print("未知指令")
