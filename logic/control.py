import time
import RPi.GPIO as GPIO
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# PCA9685: Control 2 SG-90 and 1 MG996R (360 ver.)
TRAY_LEFT = 0
TRAY_RIGHT = 1
BIN = 2
PCA_DUTY = 65535
PCA_FREQ = 50

PULSE_MAX = 2500
PULSE_MIN = 500

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = PCA_FREQ

# angle -> duty cycle 
def angle_to_duty(angle):
    pulse = PULSE_MIN + (angle / 180.0) * (PULSE_MAX - PULSE_MIN)
    duty = int(pulse * PCA_DUTY / (1000000 / PCA_FREQ))
    return duty


# bin: move to 'label'
def rotate_bin(label):
    angle_map = {   # suitable values found through testing
        'can': 120,
        'plastic': 210,
        'paper': 45
    }

    target_angle = angle_map[label]

    # fixed rotation speed: 1 degree ~= 0.01 sec.
    rotation_time = target_angle * 0.01

    # rotation direction
    if label == 'paper':
        duty = 0.06  # clockwise (for shortest path)
    else:
        duty = 0.095 # counter-clockwise

    # rotate
    pca.channels[BIN].duty_cycle = int(duty * 0xFFFF)
    time.sleep(rotation_time)

    # stop
    pca.channels[BIN].duty_cycle = 0

# bin: return to the origin (cuz bin always starts rotating at the origin(re-To be Sorted class))
def return_bin(label):
    return_angle_map = {    # suitable values found through testing
        'can': 50,
        'plastic': 82,
        'paper': 100
    }

    # same angle but opposite direction
    return_angle = return_angle_map[label]
    return_rotation_time = return_angle * 0.01

    duty = 0.095 if label == 'paper' else 0.06

    pca.channels[BIN].duty_cycle = int(duty * 0xFFFF)
    time.sleep(return_rotation_time)

    pca.channels[BIN].duty_cycle = 0

# tray
def rotate_tray():
    duty_45deg = angle_to_duty(45)
    duty_90deg = angle_to_duty(90)
    duty_135deg =  angle_to_duty(135)

    pca.channels[TRAY_LEFT].duty_cycle = duty_135deg
    pca.channels[TRAY_RIGHT].duty_cycle = duty_45deg
    time.sleep(1)

    pca.channels[TRAY_LEFT].duty_cycle = duty_90deg
    pca.channels[TRAY_RIGHT].duty_cycle = duty_90deg


# GPIO: Control Ultrasonic and LED
ULTRA_TRIG = 17
ULTRA_ECHO = 27
LED = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(ULTRA_TRIG, GPIO.OUT)
GPIO.setup(ULTRA_ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

# Ultrasonic sensor
def check_full():
    GPIO.output(ULTRA_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(ULTRA_TRIG, False)

    while GPIO.input(ULTRA_ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ULTRA_ECHO) == 1:
        pulse_end = time.time()

    distance = (pulse_end - pulse_start) * (340*100) / 2
    distance = round(distance, 2)

    print(f"[ULTRA] 측정 거리: {distance}cm → {'FULL' if distance < 10 else 'OK'}")
    return (distance < 10)

# LED
def notification():
    GPIO.output(LED, True)
    time.sleep(2)
    GPIO.output(LED, False)

# cleanup
def cleanup():
    print("[CLEANUP] GPIO 정리 및 종료")
    GPIO.cleanup()

