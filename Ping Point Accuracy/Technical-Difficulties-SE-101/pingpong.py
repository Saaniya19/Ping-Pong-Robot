from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from time import sleep
from guizero import App, Text, PushButton
from gpiozero import Robot, LED
import numpy as np

#initialize motors
motor = Robot(left=(4, 14), right=(17, 18))
motorSwitch = LED(27)

app = App(title="GUI Development", layout="grid", height=600, width=800)
message = Text(app, text="Dual Motor Control Interface", grid=[4,0])

motorSpeedForward = 0
motorSpeedBackward = 0

#motor functions
def toggleSwitch():
    if button0.text=="Start":
       motorSwitch.on()
       button0.text="Stop"
    elif button0.text == "Stop":
         motorSwitch.off()
         button0.text = "Start"

def forwardSpeedIncrease():
    global motorSpeedForward
    motor.forward(speed=motorSpeedForward)
    print("Increased speed of motor backward. Current speed = "+ str(motorSpeedForward))
    motorSpeedForward += 0.1
    if motorSpeedForward >= 1:
        motorSpeedForward = 1

def forwardSpeedReduce():
    global motorSpeedForward
    motor.forward(speed=motorSpeedForward)
    print("Reduce speed of motor forward. Current speed = "+ str(motorSpeedForward))
    motorSpeedForward -= 0.1
    if motorSpeedForward <= 0:
        motorSpeedForward = 0

def backwardSpeedIncrease():
    global motorSpeedBackward
    motor.forward(speed=motorSpeedBackward)
    print("Increased speed of motor backward. Current speed = "+ str(motorSpeedBackward))
    motorSpeedBackward += 0.1
    if motorSpeedBackward >= 1:
        motorSpeedBackward = 1

def backwardSpeedReduce():
    global motorSpeedBackward
    motor.backward(speed=motorSpeedBackward)
    print("Reduce speed of motor backward. Current speed = "+ str(motorSpeedBackward))
    motorSpeedBackward -= 0.1
    if motorSpeedBackward <= 0:
        motorSpeedBackward = 0

def isset(v):
    try:
        type (eval(v))
    except:
        return 0
    else:
        return 1

#changes hsv values to rgb values
def nothing(x):
    pass

#initializes the camera object
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

#editing PiRGBArray
rawCapture = PiRGBArray(camera, size=(320,240))

#reading frames from camera module
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    #setting up color recognition
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    B = 0
    G = 255
    R = 0

    green = np.uint8([[[B,G,R]]])
    hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
    upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

    #adjusting the threshold of the HSV image for range of selected color
    mask = cv2.inRange(hsv, lowerLimit, upperLimit)

    #actually taking out the objects of the colors in the frame
    result = cv2.bitwise_and(image, image, mask=mask)
    
    #find contours in threshold (filtered) image
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__.split('.'))
    
    #findContours() has different form for opencv2 and opencv3 (includes boolean or not)
    if major_ver == "2" or major_ver == "3":
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    #find contour with max area (most of that color, likely the object) and store it
    max_area = 0
    for cont in contours:
        area = cv2.contourArea(cont)
        if area > max_area:
            max_area = area
            best_cont = cont
    
    #find centroids of best_cont and draw a circle there
    if isset('best_cont'):
        M = cv2.moments(best_cont)
        cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
        print("Central pos: (%d, %d)" % (cx, cy))
    else:
        print("[Warning]Tag lost...")
    
    key = cv2.waitKey(1)

    #clearing the stream
    rawCapture.truncate(0)
    if key == 'f':
        break

camera.close()