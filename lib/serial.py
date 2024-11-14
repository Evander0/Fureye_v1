import threading
import wiringpi
import lib.Event


class Serial:
    serial = None
    rate = None
    mode = "HEX"
    encoding = "Utf-8"
    listening = False
    thread = None
    eventHandler = lib.Event.EventHandler()

    def __init__(self, device=0, rate=115200):
        self.rate = rate
        wiringpi.wiringPiSetup()
        self.serial = wiringpi.serialOpen(f"/dev/ttyS{device}", self.rate)
        if self.serial < 0:
            print(f"Unable to open serial device: /dev/ttyS{device}")
            return

    def set(self, Mode="HEX", Encoding="Utf-8"):
        """
        :param Mode: "HEX", "Text"
        :param Encoding: "Utf-8", "gbk"
        :return:
        """
        match Mode:
            case "Text":
                self.mode = Mode
            case "HEX":
                self.mode = Mode
            case _:
                raise ValueError(f"Unexpected Mode: {self.mode}")

        match Encoding:
            case "Utf-8":
                self.encoding = Encoding
            case "gbk":
                self.encoding = Encoding
            case _:
                raise ValueError(f"Unexpected Encoding: {self.encoding}")

    def send(self, msg):
        if self.mode == "HEX":
            msgn = int(msg)
            wiringpi.serialFlush(self.serial)
            wiringpi.serialPutchar(self.serial, msgn)
        elif self.mode == "Text":
            for t in msg:
                msgn = ord(str(t).encode(self.encoding))
                wiringpi.serialFlush(self.serial)
                wiringpi.serialPutchar(self.serial, msgn)
                wiringpi.delayMicroseconds(100)
            wiringpi.serialFlush(self.serial)
            wiringpi.serialPutchar(self.serial, 4)

    def send_raw(self, msg):
        wiringpi.serialFlush(self.serial)
        wiringpi.serialPutchar(self.serial, msg)

    def close(self):
        wiringpi.serialClose(self.serial)
        self.listening = False
        del self.eventHandler

    def start(self, func):
        self.listening = True
        self.thread = threading.Thread(target=self.__listen__,
                                       name="uart_daemon")
        self.thread.start()
        self.eventHandler.register_event("uart_listen", func)

    def __listen__(self):
        msg = ""
        try:
            while self.listening:
                if wiringpi.serialDataAvail(self.serial):
                    if self.mode == "HEX":
                        msg = wiringpi.serialGetchar(self.serial)
                        event = lib.Event.Event("uart_listen", msg=msg)
                        self.eventHandler.trigger_event(event)
                    elif self.mode == "Text":
                        tmp = int(wiringpi.serialGetchar(self.serial))
                        if tmp == 4:
                            event = lib.Event.Event("uart_listen", msg=msg)
                            self.eventHandler.trigger_event(event)
                            msg = ""
                            continue
                        msg += tmp.to_bytes(1, 'little').decode(self.encoding)
            return
        finally:
            self.listening = False
