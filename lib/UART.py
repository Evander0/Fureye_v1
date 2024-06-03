import threading
import wiringpi
import Event


class UART:
    serial = None
    rate = None
    mode = "HEX"
    encoding = "Utf-8"
    listening = False
    eventHandler = Event.EventHandler()

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
        match self.mode:
            case "Text":
                msgn = msg.encode()
            case "HEX":
                msgn = int(msg)
            case _:
                raise ValueError(f"Unexpected Mode: {self.mode}")
        wiringpi.serialFlush(self.serial)
        wiringpi.serialPutchar(self.serial, msgn)

    def close(self):
        wiringpi.serialClose(self.serial)
        self.listening = False
        del self.eventHandler

    def start(self, func):
        self.listening = True
        threading.Thread(target=self.__listen__,
                         name="uart_daemon", daemon=True)
        self.eventHandler.register_event("uart_listen", func)

    def __listen__(self):
        try:
            while self.listening:
                if wiringpi.serialDataAvail(self.serial):
                    msg = wiringpi.serialGetchar(self.serial)
                    event = Event.Event("event1", data=msg)
                    self.eventHandler.trigger_event(event)
            return
        finally:
            self.listening = False
