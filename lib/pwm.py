import os
import wiringpi


class Pwm_sh:
    pwm_path: str

    def __init__(self, pos):
        self.pwm_path = f"/sys/class/pwm/pwmchip{pos}"
        with open(f"{self.pwm_path}/export", 'w') as f:
            f.write("0")
        if not os.path.exists(f"{self.pwm_path}/pwm0"):
            os.mkdir(f"{self.pwm_path}/pwm0")
        with open(f"{self.pwm_path}/pwm0/polarity", 'w') as f:
            f.write("normal")

    def set_pwm(self, temp=10):
        with open(f"{self.pwm_path}/pwm0/period", 'w') as f:
            f.write("10000000")
        with open(f"{self.pwm_path}pwm0/duty_cycle", 'w') as f:
            f.write(str(temp * 10 * 10000))

    def state(self, state):
        if state:
            with open(f"{self.pwm_path}/pwm0/enable", 'w') as f:
                f.write("1")
        else:
            with open(f"{self.pwm_path}/pwm0/enable", 'w') as f:
                f.write("0")


class Pwm_os:
    pwm: int

    def __init__(self, pos):
        os.system(f"gpio mode {pos} pwm")
        self.pwm = pos
        self.duty_ratio()

    def frequency(self, hz: int):
        if hz < 500:
            self.manual_division(100)
            self.manual_frequency(hz)
        elif hz < 100:
            self.manual_division(500)
            self.manual_frequency(hz)
        elif hz < 50:
            self.manual_division(1000)
            self.manual_frequency(hz)
        elif hz < 10:
            self.manual_division(10000)
            self.manual_frequency(hz)
        else:
            self.manual_division(1)
            self.manual_frequency(hz)

    def ratio(self, ratio: int):
        self.duty_ratio(ratio * 10, 1000)

    def disable(self):
        os.system(f"gpio mode {self.pwm} out")

    def manual_division(self, ratio: int):
        os.system(f"gpio pwmc {self.pwm} {ratio}")

    def manual_frequency(self, hz: int):
        os.system(f"gpio pwmTone {self.pwm} {hz}")

    def duty_ratio(self, CCR=500, ARR=1000):
        os.system(f"gpio pwm {self.pwm} {CCR}")
        os.system(f"gpio pwmr {self.pwm} {ARR}")


class Pwm_pi:
    pwm: int
    range: int
    speed = 19200 #khz

    def __init__(self, pos, clock=1, range=1000):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(pos, 2)
        wiringpi.pwmSetClock(pos, clock)
        wiringpi.pwmSetRange(pos, range)
        wiringpi.pwmWrite(pos, int(range/2))
        self.pwm = pos
        self.range = range

    def auto_ratio(self, pct: int):
        pct = pct/100*self.range
        wiringpi.pwmWrite(self.pwm, pct)

    def frequency(self, hz):
        wiringpi.pwmSetClock(self.speed * 1000 / (hz * self.range))

    def clock(self, clock: int):
        wiringpi.pwmSetClock(self.pwm, clock)

    def duty_ratio(self, t, range):
        wiringpi.pwmWrite(self.pwm, t)
        wiringpi.pwmSetRange(self.pwm, range)
        self.range = range
