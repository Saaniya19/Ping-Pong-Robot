# pip3 install gpiozero

from time import sleep
from guizero import App, Text, PushButton
from gpiozero import Robot, LED

motor = Robot(left=(4, 14), right=(17, 18))
motorSwitch = LED(27)

app = App(title="GUI Development", layout="grid", height=600, width=800)
message = Text(app, text="Dual Motor Control Interface", grid=[4,0])

motorSpeedForward = 0
motorSpeedBackward = 0

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

Text(app, "Motor",grid=[2,1])
button0 = PushButton(app, command=toggleSwitch, text="Start", width=10,height=3, grid=[2,4])
button1 = PushButton(app, command=forwardSpeedIncrease, text="Frwd Speed +", width=10,height=3, grid=[2,3])
button2 = PushButton(app, command=backwardSpeedReduce, text="Bckwd Speed -", width=10,height=3, grid=[2,5])
button3 = PushButton(app, command=backwardSpeedIncrease, text = "Bckwd Speed +", width=10,height=3, grid=[1,4])
button4 = PushButton(app, command=forwardSpeedReduce, text="Frwd Speed -", width=10, height=3, grid=[3,4])

app.display()