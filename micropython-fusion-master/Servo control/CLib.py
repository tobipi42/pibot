from picamera import PiCamera
from time import sleep
import time
import numpy as np

# Run this during initialization
def InitCamera():
    x_res = 800
    y_res = 48

    camera = PiCamera()
    camera.resolution = (x_res, y_res)  # set camera resolution

    return camera, x_res, y_res

# Release the camera resources during termination of the program
def CleanupCamera(camera):
    camera.close()
    return

# Retrieve Gray scale image from colour image
def GetGrayImage(x_res,y_res,camera):
    # Camera angle is 62.2 degrees

    #camera = PiCamera() # migrated to camera init function
    #camera.resolution = (x_res, y_res)  # set camera resolution # migrated to camera init function
    CurrentImage = np.empty((y_res, x_res, 3), dtype=np.uint8)
    camera.capture(CurrentImage,'rgb')
    CurrentImage_gray = 0.2989 * CurrentImage[:,:,0] + 0.5870 * CurrentImage[:,:,1] + 0.1140 * CurrentImage[:,:,2]

    #camera.close() # migrated to camera close function
    return CurrentImage_gray

# Calculate the angle between the two images
def CalcAngleChange(StartImage, NewImage, TotalRotationAngle=0):

    nStartImage_rows, nStartImage_cols = StartImage.shape

    half_cols = np.uint16(np.floor(nStartImage_cols/2))
    dif_vector = 9000*np.ones(nStartImage_cols)

    NewImage_ls = NewImage[:,0:half_cols] # grab the left half of the new image half_cols is not included
    NewImage_rs = NewImage[:,half_cols:nStartImage_cols] # grab the right half of the new image
    SearchStep = 1
    for i in range(0,half_cols,SearchStep): # check for first half 31.1 degrees
        dif_vector[half_cols-i-1] = np.mean( np.square(np.subtract(NewImage_ls , StartImage[:,i:i+half_cols])))
        dif_vector[i+half_cols] = np.mean( np.square(np.subtract(NewImage_rs , StartImage[:,half_cols-i:nStartImage_cols-i])))
    
    #for i in range(nStartImage_cols):
    #    print(dif_vector[i]) # Display the cost function

    #print(np.argmin(dif_vector))
    IdxMin = np.argmin(dif_vector)
    print(IdxMin)
    if IdxMin-half_cols < 2:
        print(IdxMin)
        IdxMin = half_cols
        print('no rotation')
    AngleRotation =  62.2/2 - 62.2/nStartImage_cols * (IdxMin) 
    TotalRotationAngle = TotalRotationAngle + AngleRotation

    return AngleRotation, TotalRotationAngle


# start_time = time.time()
# camera, x_res, y_res = InitCamera()
# print("Time initialize Camera is %s seconds" % (time.time() - start_time))

# start_time = time.time()
# StartImage = GetGrayImage(x_res,y_res)
# #print(wow)
# print("Time to get image 1 is %s seconds" % (time.time() - start_time))
# sleep(1)
# start_time = time.time()
# NewImage = GetGrayImage(x_res,y_res)
# print("Time to get image 2 is %s seconds" % (time.time() - start_time))
# start_time = time.time()
# AngleRotation, TotalRotationAngle = CalcAngleChange(StartImage,NewImage,0)
# print("Time to get delta angle is %s seconds" % (time.time() - start_time))
# print("the estimated angle is %s degrees" % AngleRotation)

# print('set new angle')
# start_time = time.time()
# StartImage = NewImage # image 1 is image 2
# NewImage = GetGrayImage(x_res,y_res)
# print("Time to get image 3 is %s seconds" % (time.time() - start_time))

# start_time = time.time()
# AngleRotation, TotalRotationAngle = CalcAngleChange(StartImage,NewImage,TotalRotationAngle)
# print("Time to get delta and total angle is %s seconds" % (time.time() - start_time))
# print("the estimated delta is %s degrees" % AngleRotation)
# print("the estimated total is %s degrees" % TotalRotationAngle)

# start_time = time.time()
# CleanupCamera(camera)
# print("Time initialize Camera is %s seconds" % (time.time() - start_time))