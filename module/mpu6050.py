import time
from lib.mpu6050 import mpu6050
from lib.lib import *

error_x = 0
error_y = 0
error_z = 0

process_noise = 1e-5
measurement_noise = 6e-5
estimation_error = 2


def __init__():
    sensor = mpu6050(0x68, 3)
    kalman_filter_x = KalmanFilter(process_noise, measurement_noise, estimation_error)
    kalman_filter_y = KalmanFilter(process_noise, measurement_noise, estimation_error)
    kalman_filter_z = KalmanFilter(process_noise, measurement_noise, estimation_error)

    calibrate(10, sensor)

    static["running"]["mpu6050"] = True
    while static["running"]["mpu6050"]:
        dt = 0.01

        accel_x = sensor.get_accel_data(g=True)["x"]
        accel_y = sensor.get_accel_data(g=True)["y"]
        accel_z = sensor.get_accel_data(g=True)["z"]
        gyro_x = sensor.get_gyro_data()["x"] - error_x
        gyro_y = sensor.get_gyro_data()["y"] - error_y
        gyro_z = sensor.get_gyro_data()["z"] - error_z

        x = int(round(kalman_filter_x.update(gyro_x), 2))
        y = int(round(kalman_filter_y.update(gyro_y), 2))
        z = int(round(kalman_filter_z.update(gyro_z), 2))

        time.sleep(dt)
    del static["running"]["mpu6050"]
    return


class KalmanFilter:
    def __init__(self, p_noise, m_noise, e_error):
        self.process_noise = p_noise
        self.measurement_noise = m_noise
        self.estimation_error = e_error
        self.estimate = 0.0
        self.error_estimate = 1.0

    def update(self, measurement):
        error_estimate = self.error_estimate + self.process_noise

        kalman_gain = error_estimate / (error_estimate + self.measurement_noise)
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)
        self.error_estimate = (1 - kalman_gain) * error_estimate

        return self.estimate


def calibrate(times, sensor=None):
    global error_x, error_y, error_z
    tmp_x = 0
    tmp_y = 0
    tmp_z = 0
    for i in range(times):
        tmp_x = sensor.get_gyro_data()["x"] + tmp_x
        tmp_y = sensor.get_gyro_data()["y"] + tmp_y
        tmp_z = sensor.get_gyro_data()["z"] + tmp_z
    error_x = tmp_x / times
    error_y = tmp_y / times
    error_z = tmp_z / times
