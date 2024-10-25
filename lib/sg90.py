import wiringpi


class sg90:
    def __init__(self, port):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(port, 2)
        wiringpi.pwmSetClock(port, 192)
        wiringpi.pwmSetRange(port, 2000)
        wiringpi.pwmWrite(2, 50)

    def deg(self, deg: int):
        pi = (deg+90)/0.9+50
        wiringpi.pwmWrite(2, int(pi))
