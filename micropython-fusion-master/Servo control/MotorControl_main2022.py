# servo control with Adafruit PCA9685

from __future__ import division
import time
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 0  # Min pulse length out of 4096
servo_max = 4095  # Max pulse length out of 4096
servo_freq = 50

in3 = 9 # left side
in4 = 10 # left side
enB = 11

in1 = 14 # right side
in2 = 13 # right side
enA = 15

pwm.set_pwm_freq(servo_freq)

pwm.set_pwm(in1, 0, servo_min)
pwm.set_pwm(in2, 0, servo_min)
pwm.set_pwm(in3, 0, servo_min)
pwm.set_pwm(in4, 0, servo_min)
pwm.set_pwm(enA, 0, servo_max)
pwm.set_pwm(enB, 0, servo_max)
    
def setMotorPWM(channel,servo_DutyCycle):
    if servo_DutyCycle > 0 and (channel == enA or channel == enB):
        minDutyCycle = 0.3
    else:
        minDutyCycle = 0
        
    servo_DutyCycle = minDutyCycle + (1-minDutyCycle) * servo_DutyCycle
    servo_period = 1/servo_freq
    servo_resolution = servo_period/4096
    servo_pulse = int(min(4096*servo_DutyCycle,4095))
    pwm.set_pwm(channel, 0, servo_pulse)
    return

def setSteering(x):

    if x=='r':
        #print('set high power')
        setMotorPWM(enA,0.9)
        setMotorPWM(enB,0.9)
        print('go right')
        setMotorPWM(in1,1)
        setMotorPWM(in2,0)
        setMotorPWM(in3,1)
        setMotorPWM(in4,0)
        x='z'
    elif x=='l':
        #print('set high power')
        setMotorPWM(enA,0.9)
        setMotorPWM(enB,0.9)
        print('go left')
        setMotorPWM(in1,0)
        setMotorPWM(in2,1)
        setMotorPWM(in3,0)
        setMotorPWM(in4,1)
        x='z'
    elif x=='s':
        print("stop")
        setMotorPWM(in1,0)
        setMotorPWM(in2,0)
        setMotorPWM(in3,0)
        setMotorPWM(in4,0)
        x='z'
    elif x=='e':
        pwm.set_pwm(enA, 0, 0)
        pwm.set_pwm(enB, 0, 0)
    #print('set med power')
    setMotorPWM(enA,0.6)
    setMotorPWM(enB,0.6)
    return x


def setDirection(x):   
    if x=='f':
        setMotorPWM(in1,0)
        setMotorPWM(in2,1)
        setMotorPWM(in3,1)
        setMotorPWM(in4,0)
        print("forward")
        x='z'
    
    elif x=='s':
        print("stop")
        setMotorPWM(in1,0)
        setMotorPWM(in2,0)
        setMotorPWM(in3,0)
        setMotorPWM(in4,0)
        x='z'

    elif x=='b':
        print("backward")
        setMotorPWM(in1,1)
        setMotorPWM(in2,0)
        setMotorPWM(in3,0)
        setMotorPWM(in4,1)
        x='z'
    elif x=='e':
        pwm.set_pwm(enA, 0, 0)
        pwm.set_pwm(enB, 0, 0)
    return x
    
def setSpeed(x):
    if x=='low':
        print("low")
        setMotorPWM(enA,0.3)
        setMotorPWM(enB,0.3)
        x='z'

    elif x=='med':
        print("medium")
        setMotorPWM(enA,0.6)
        setMotorPWM(enB,0.6)
        x='z'

    elif x=='high':
        print("high")
        setMotorPWM(enA,0.9)
        setMotorPWM(enB,0.9)
        x='z'
    elif x=='e':
        pwm.set_pwm(enA, 0, 0)
        pwm.set_pwm(enB, 0, 0)
    return x

# print("\n")
# print("The default speed & direction of motor is LOW & Forward.....")
# print("s-stop f-forward b-backward l-low m-medium h-high e-exit")
# print("\n")    
# 
# while(1):
#     
#     x=input()
#     setSteering(x)
#     setDirection(x)
#     setSpeed(x)
#     
#     if x=='e':
#         pwm.set_pwm(enA, 0, 0)
#         pwm.set_pwm(enB, 0, 0)
#         break

