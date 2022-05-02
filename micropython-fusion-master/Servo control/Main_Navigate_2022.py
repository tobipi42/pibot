#Main_Navigate script
import numpy as np
import time
from Lidar import *
from servocontrol_main2022 import *
from MotorControl_main2022 import *

print('Looking forward')
# Set Pitch angle
pitchAngleDeg = 0;
yawAngleDeg = 0;
setServoPitch(0)
time.sleep(1.2)
setServoYaw(0)
time.sleep(1.2)
print('Start Navigation')
x_map =[]
y_map =[]
h_map =[]
h_current = 0
x_current = 0
y_current = 0

RUNBOOL = True
ScanCounter = 500

# MOTOR Control
try:
    while RUNBOOL == True:
        
        x=input()
        
        if x=='quit':
            RUNBOOL = False
        
        if x=='scan':
#             setServoPitch(pitchAngleDeg)
#             time.sleep(1.2)
            print('starting scan')
            dYawSweep = 5
            LoopCounter = 0
            setServoYaw(-90)
            time.sleep(abs(yawAngleDeg - -90)/50)
            
            for yawAngleDeg in range(-90, 90+1, dYawSweep):
                sweepsleep = dYawSweep /10
                setServoYaw(yawAngleDeg)
                time.sleep(sweepsleep)

                time.sleep(0.1)
                distance,strength = LidarDistance()
                print('Yaw',int(yawAngleDeg), ', Pitch',int(pitchAngleDeg), ', d=', distance, 'cm, p=', strength)

                h_new = int(distance * np.sin(pitchAngleDeg/180*np.pi)/10) * 10 - h_current
                h_project = distance * np.cos(pitchAngleDeg/180*np.pi)
                x_new = int(h_project * np.sin(yawAngleDeg/180*np.pi)/10) * 10 - x_current
                y_new = int(h_project * np.cos(yawAngleDeg/180*np.pi)/10) * 10 - y_current

                h_map.append(h_new)
                x_map.append(x_new)
                y_map.append(y_new)

                LoopCounter = LoopCounter +1
               # if LoopCounter % 100:
            output_data = np.vstack((x_map,y_map,h_map))
            np.savetxt(f'spatial_data_field_{ScanCounter}.csv',output_data,fmt='%.1d',delimiter=',')
            ScanCounter = ScanCounter + 1
             
            print('Looking forward')
            setServoYaw(0)
            time.sleep(abs(yawAngleDeg)/10)
            yawAngleDeg = 0;
            
        
        start_distance, start_strength = LidarDistance()
        if x=='move forward':
            print('start_distance',start_distance)
            
            setSpeed('med')
            
            setDirection('f')
            
            
            distance, strength = LidarDistance()
            print('distance diff:',abs(start_distance - distance))
            while abs(start_distance - distance) < 40: # WE shall move 40 cm
                distance, strength = LidarDistance()
                time.sleep(0.25)
                print('distance moved:',abs(start_distance - distance))
            
            x_current = x_current + 40 # WE shall move 40 cm
            setDirection('s') # 'f','s','b'
            
            #Look left and right
            print('Lets look around')
            time.sleep(1.0)
            setServoYaw(-90)
            time.sleep(1.0)
            setServoYaw(90)
            time.sleep(2.0)
            setServoYaw(0)
            time.sleep(1.0)
            
            setSteering('l')
            time.sleep(3.0)
            setSteering('s')
            time.sleep(1.0)
            setSteering('r')
            time.sleep(3.0)
            setSteering('s')
            x='z'
            
#             setSteering(x) # 'l','r',
#             setSpeed(x) #'low','med','high'
        
except KeyboardInterrupt:
    print("Keyboard interrupt")
    x='s'
    setDirection(x)
    x='e'
    setDirection(x)
    print("Cleaned up")
    
finally:
    print("Finished Script")
    x='s'
    setDirection(x)
    x='e'
    setDirection(x)
    print("Cleaned up")
    
