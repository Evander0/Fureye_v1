# 定义事件类
class Event:
    def __init__(self, name, **kwargs):
        self.name = name
        self.params = kwargs


# 定义事件处理类
class EventHandler:
    def __init__(self):
        self.events = {}

    def register_event(self, event_name, handler):
        if event_name in self.events:
            self.events[event_name].append(handler)
        else:
            self.events[event_name] = [handler]

    def trigger_event(self, event):
        if event.name in self.events:
            for handler in self.events[event.name]:
                handler(event)
