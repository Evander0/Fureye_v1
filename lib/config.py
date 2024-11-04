import json


class Config:
    config = None
    file: str = None
    default: dict = None

    def __init__(self, file: str, default: dict = None):
        self.default = default
        self.file = "./config/"+file+".json"
        try:
            self.config = open(self.file, 'r+')
        except Exception as e:
            print("配置文件异常，正在重置")
            print("错误代码：" + str(e))
            data = json.dumps(default, indent=4)
            with open(self.file, 'w') as f:
                f.write("\n" + data)

    def read(self):
        try:
            conf = json.load(self.config)
            return conf
        except Exception as e:
            print("读取配置文件异常")
            print("错误代码：" + str(e))
            return -1

    def write(self, t: dict):
        try:
            conf = json.load(self.config)
            conf.update(t)
            data = json.dumps(conf, indent=4)
            self.config.write("\n" + data)
            self.config.flush()
        except Exception as e:
            print("读取配置文件异常")
            print("错误代码：" + str(e))
            return -1

    def wipe(self):
        data = json.dumps({}, indent=4)
        with open(self.file, 'w') as f:
            f.write("\n" + data)
            f.flush()

    def close(self):
        self.config.close()
