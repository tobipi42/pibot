import RPi.GPIO as GPIO
import time
from Lidar import *

import numpy as np
import matplotlib.pyplot as plt

# plt.axis([-300, 300,-300, 300, 0, 300])
distance = 100

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x =[]
y =[]
h =[]
PlotCounter = 0

GPIO.setwarnings(False)

servoPIN1 = 5
servoPIN2 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)

pitchServo = GPIO.PWM(servoPIN1, 50) # GPIO 5 for PWM with 50Hz
yawServo = GPIO.PWM(servoPIN2, 50) # GPIO 6 for PWM with 50Hz

yawAnglePWM = 2.5
pitchAnglePWM = 2.5

pitchServo.start(pitchAnglePWM) # Initialization
yawServo.start(yawAnglePWM) # Initialization

try:
  while True:
      #2.5 - 7 - 12
    sleeptime = 0.05
    

    dPitchSweep = 2#750/distance
    dYawSweep = 2#750/distance
    sleeptime = max( dPitchSweep,dYawSweep) /50
    
    print('dPitchSweep =',int(dPitchSweep),'dYawSweep =',int(dYawSweep))
    
    if pitchAnglePWM < 12.5 - (dPitchSweep/18):
        pitchAnglePWM = pitchAnglePWM + dPitchSweep/18
    else:
        pitchAnglePWM = 2.5
        sleeptime = 1.2;
        
        if False:
            ax.scatter(x, y, h)
            plt.draw()
            plt.pause(0.1)
            
        output_data = np.vstack((x,y,h))
        np.savetxt('spatial_data10.csv',output_data,fmt='%.1d',delimiter=',')
        
        if yawAnglePWM < 12.5 - (dYawSweep/18):
            yawAnglePWM = yawAnglePWM + dYawSweep/18
        else:
            yawAnglePWM = 2.5
            sleeptime = 3;
            print('finalized scan. Terminating script')
            break
            
#     yawAnglePWM = 7
#     pitchAnglePWM = 2.5
    
    pitchAngleDeg = (pitchAnglePWM-2.5)/10*180
    pitchServo.ChangeDutyCycle(pitchAnglePWM)
    yawAngleDeg = (yawAnglePWM-2.5)/10*180-90
    yawServo.ChangeDutyCycle(yawAnglePWM)
    time.sleep(sleeptime)
    distance,strength = LidarDistance()
    print('Yaw',int(yawAngleDeg), ', Pitch',int(pitchAngleDeg), ', d=', distance, 'cm, p=', strength)
    
    h_current = int(distance * np.sin(pitchAngleDeg/180*np.pi))
    h_project = distance * np.cos(pitchAngleDeg/180*np.pi)
    x_current = int(h_project * np.sin(yawAngleDeg/180*np.pi))
    y_current = int(h_project * np.cos(yawAngleDeg/180*np.pi))
    
    h.append(h_current)
    x.append(x_current)
    y.append(y_current)
    
#     if len(h) % 10 == 0:
#         ax.scatter(x, y, h)
#         plt.draw()
#         plt.pause(0.05)
#         print('counter',PlotCounter)
#         
#     PlotCounter = PlotCounter+1
    
except KeyboardInterrupt:
    print("Keyboard interrupt")
    pitchServo.stop()
    yawServo.stop()
    GPIO.cleanup()
  
# except:
#    print("some error") 

finally:
    print("clean up")
    pitchServo.stop()
    yawServo.stop()
    GPIO.cleanup() # cleanup all GPIO
