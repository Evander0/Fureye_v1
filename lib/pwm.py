import os


class Pwm_sh:
    pwm_path: str

    def __init__(self, pos=0):
        Pwm_sh.pwm_path = f"/sys/class/pwm/pwmchip{pos}"
        with open(f"{Pwm_sh.pwm_path}/export", 'w') as f:
            f.write("0")
        if not os.path.exists(f"{Pwm_sh.pwm_path}/pwm0"):
            os.mkdir(f"{Pwm_sh.pwm_path}/pwm0")
        with open(f"{Pwm_sh.pwm_path}/pwm0/polarity", 'w') as f:
            f.write("normal")

    def set_pwm(self, temp=10):
        with open(f"{Pwm_sh.pwm_path}/pwm0/period", 'w') as f:
            f.write("10000000")
        with open(f"{Pwm_sh.pwm_path}pwm0/duty_cycle", 'w') as f:
            f.write(str(temp * 10 * 10000))

    def state(self, state):
        if state:
            with open(f"{Pwm_sh.pwm_path}/pwm0/enable", 'w') as f:
                f.write("1")
        else:
            with open(f"{Pwm_sh.pwm_path}/pwm0/enable", 'w') as f:
                f.write("0")


class Pwm_os:
    pwm: int

    def __init__(self, pos):
        os.system(f"gpio mode {pos} pwm")
        Pwm_os.pwm = pos
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
        self.duty_ratio(ratio*10, 1000)

    def disable(self):
        os.system(f"gpio mode {Pwm_os.pwm} out")

    def manual_division(self, ratio: int):
        os.system(f"gpio pwmc {Pwm_os.pwm} {ratio}")

    def manual_frequency(self, hz: int):
        os.system(f"gpio pwmTone {Pwm_os.pwm} {hz}")

    def duty_ratio(self, CCR=500, ARR=1000):
        os.system(f"gpio pwm {Pwm_os.pwm} {CCR}")
        os.system(f"gpio pwmr {Pwm_os.pwm} {ARR}")
