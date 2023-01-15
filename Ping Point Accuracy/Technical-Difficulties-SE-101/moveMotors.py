import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

Motor1A = 24
Motor1B = 23
Motor1E = 25

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
print("Setup complete")

error = 15
xPosition = 100
middle = 160

while abs(xPosition-middle) > error:  
    if xPosition-middle < 0:
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)
        print("Moving backwards")
    elif xPosition-middle > 0:
        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)
        print("Moving forwards")

GPIO.output(Motor1E, GPIO.LOW)
print("Stop")

print("Clean up")
GPIO.cleanup()