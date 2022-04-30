# servo control with Adafruit PCA9685
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Import Lidar library functions
from Lidar import *

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
pulse_min = 0  # Min pulse length out of 4096
pulse_max = 4095  # Max pulse length out of 4096
servo_freq = 50

pwm.set_pwm_freq(servo_freq)

def setServoPitch(servo_angle):
    PitchChannel = 7
    servo_min = 120  # Min pulse length out of 4096 205 -90 deg
    servo_max = 506  # Max pulse length out of 4096 410 +90 deg
    servo_angle = max(servo_angle,0)
    servo_angle = min(servo_angle,180)
    
    servo_pulse = int((servo_angle)/180*(servo_max - servo_min)) + servo_min
    print('pulse',servo_pulse)
    
    pwm.set_pwm(PitchChannel, 0, servo_pulse)
    return

def setServoYaw(servo_angle):
    YawChannel = 6
    servo_min = 120  # Min pulse length out of 4096 205 -90 deg
    servo_max = 506  # Max pulse length out of 4096 410 +90 deg
    servo_angle = max(servo_angle,-90)
    servo_angle = min(servo_angle,90)
    
    correction = 3 - 3/90.0*abs(servo_angle)
    servo_pulse = int((servo_angle + 90 - correction)/180*(servo_max - servo_min)) + servo_min
    print('pulse',servo_pulse)
    
    pwm.set_pwm(YawChannel, 0, servo_pulse)
    return

# print('Moving servo to default position')
# setServoYaw(0)
# setServoPitch(0)
# while True:
#     
#     print('Moving servo on channel 6&7')
# 
#     print('set yaw angle')
#     UserAngle = int(input())
#     setServoYaw(UserAngle)
#     time.sleep(1.0)
#     
#     #Lidar part
#     distance,strength = LidarDistance()
#     print('Yaw',int(UserAngle), ', Pitch',int(0), ', d=', distance, 'cm, p=', strength)
    
#     print('set pitch angle')
#     UserAngle = int(input())
#     setServoPitch(UserAngle)
#     time.sleep(1.0)
    
#     setServoYaw(-90)
#     time.sleep(1.0)
#     setServoYaw(-5)
#     time.sleep(1.0)
#     setServoYaw(90)
#     time.sleep(1.0)
#     
#     print('Moving servo on channel 6&7')
#     setServoPitch(0)
#     time.sleep(1.0)
#     setServoPitch(90)
#     time.sleep(1.0)
#     setServoPitch(180)
#     time.sleep(1.0)
#     setServoPitch(0)
#     time.sleep(1.0)
    
#     print('prep for scan')
#     pwm.set_pwm(6, 0, servo_min)
#     pwm.set_pwm(7, 0, servo_min)
#     time.sleep(2)
#     
#     Counter = servo_min
#     while Counter < servo_max:
#         pwm.set_pwm(6, 0, Counter)
#         time.sleep(0.05)
#         Counter = Counter + 20
#         print('counter =',Counter)
#     else:
#         Counter = 1
#         pwm.set_pwm(6, 0, servo_max)
#         time.sleep(0.05)
    