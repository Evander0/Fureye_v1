command_list: dict = {}


def register(command: str, process):
    command_list[command] = process


def unregister(command: str):
    command_list.pop(command)


def command(command: list):
    if command[0] is "":
        pass
    elif command[0] in command_list.keys():
        command_list[command[0]](command[1:])
    else:
        print("未知指令")