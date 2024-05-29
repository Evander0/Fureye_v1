from time import sleep
import random


def __main__(dynamic, static, NULL):
    sleep(0.1)
    data = dynamic["eyes"]
    while 1:
        x = random.uniform(-0.05, 0.05)
        y = random.uniform(-0.05, 0.05)
        data[0] = x
        data[1] = y
        sleep(random.uniform(0.5, 1))
