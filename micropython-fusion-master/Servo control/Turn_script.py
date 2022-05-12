#Turn_script
import numpy as np
import time
from MotorControl_main2022 import *
from CLib import *

RUNBOOL = True
try:
    while RUNBOOL == True:
        x=input()
        
        if x=='quit':
            RUNBOOL = False

        if x=='move forward':
            setSpeed('med')
            setDirection('f')

        if x=='move left':
            
            # Catch starting image
            camera, x_res, y_res = InitCamera()
            StartImage = GetGrayImage(x_res,y_res,camera)
            
            # Start steering left
            setSteering('l')

            # keep rotating until 90 degrees left
            TotalRotationAngle = 0
            while TotalRotationAngle > -90:
                NewImage = GetGrayImage(x_res,y_res,camera)
                AngleRotation, TotalRotationAngle = CalcAngleChange(StartImage,NewImage,TotalRotationAngle)
                StartImage = NewImage # image 1 is image 2
                print("the estimated angle is %.2f degrees" % AngleRotation)
                print("the estimated total is %.2f degrees" % TotalRotationAngle)
            CleanupCamera(camera) # release camera

        if x=='move right':
            setSteering('r')
            time.sleep(3.0)

        # Stop steering
        setSteering('s')
        x='z'


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