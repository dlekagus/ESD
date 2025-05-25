import time
import RPi.GPIO as GPIO
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# PCA9685: Control 2 SG-90 and 1 MG996R 
TRAY_LEFT = 0
TRAY_RIGHT = 1
BIN = 2
PCA_DUTY = 65535
PCA_FREQ = 50

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = PCA_FREQ

current = "re"
bin_pos = {"re":0, "can":1, "plastic":2, "wastes":3}

# angle -> duty cycle 
def angle_to_duty(angle):
    pulse = 1000 + (angle / 180) * 1000
    duty = int((pulse / (1/PCA_FREQ)) * PCA_DUTY)
    return duty

# bin
def rotate_bin(target):
    global current

    if target == current:
        print(f"[BIN] {target} 방향 유지 중 → 회전 생략")
        return
    
    current_idx = bin_pos[current]
    target_idx = bin_pos[target]

    if target != "wastes":
        target_angle = target_idx * 90
    else:
        target_angle = -90
    print(f"[BIN] 현재 위치: {current} → 목표 위치: {target}, 회전 각도: {target_angle}°")
    duty = angle_to_duty(abs(target_angle))
    pca.channels[BIN].duty_cycle = duty

    time.sleep(1)
    current = target

# tray
def rotate_tray():
    duty_45deg = angle_to_duty(45)
    duty_0deg = angle_to_duty(0)

    pca.channels[TRAY_LEFT].duty_cycle = duty_45deg
    pca.channels[TRAY_RIGHT].duty_cycle = duty_45deg
    time.sleep(1)

    pca.channels[TRAY_LEFT].duty_cycle = duty_0deg
    pca.channels[TRAY_RIGHT].duty_cycle = duty_0deg
    time.sleep(0.3)


# GPIO: Control Ultrasonic and LED
ULTRA_TRIG = 3
ULTRA_ECHO = 2
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
