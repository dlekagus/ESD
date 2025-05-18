import time
import RPi.GPIO as GPIO

# PCA9685: Control 2 SG-90 and 1 MG996R 
TRAY_LEFT = 0
TRAY_RIGHT = 1
BIN = 2


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

    return (distance < 10)

# LED
def notification():
    GPIO.output(LED, True)
    time.sleep(2)
    GPIO.output(LED, False)

# cleanup
def cleanup():
    GPIO.cleanup()
