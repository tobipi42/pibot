from picamera import PiCamera
from time import sleep
import time
import numpy as np

def GetGrayImage(x_res,y_res):
    # Camera angle is 62.2 degrees
    if x_res is None:
        x_res = 320

    if y_res is None:
        y_res = 240

    camera = PiCamera()
    camera.resolution = (x_res, y_res)  # set camera resolution
    CurrentImage = np.empty((y_res, x_res, 3), dtype=np.uint8)
    camera.capture(CurrentImage,'rgb')
    CurrentImage_gray = 0.2989 * CurrentImage[:,:,0] + 0.5870 * CurrentImage[:,:,1] + 0.1140 * CurrentImage[:,:,2]
    #print(CurrentImage_gray)
    #Diff_CurrentImage = np.diff(CurrentImage_gray)

    camera.close()
    return CurrentImage_gray

def CalcAngleChange(StartImage,NewImage):
    nStartImage_rows, nStartImage_cols = StartImage.shape

    half_cols = np.uint16(np.floor(nStartImage_cols/2))
    dif_vector = 255*np.ones(nStartImage_cols)

    NewImage_ls = NewImage[:,0:half_cols] # grab the left half of the new image half_cols is not included
    NewImage_rs = NewImage[:,half_cols:nStartImage_cols] # grab the right half of the new image
    for i in range(half_cols): # check for first half 31.1 degrees

        dif_vector[half_cols-i-1] = np.mean( np.square(np.subtract(NewImage_ls , StartImage[:,i:i+half_cols])))
        #dif_vector[i] = np.mean( np.square(np.subtract(NewImage_ls , StartImage[:,i:i+half_cols])))
        #dif_vector[i+half_cols] = np.mean( np.square(np.subtract(NewImage_rs , StartImage[:,i:i+half_cols])))
        dif_vector[i+half_cols] = np.mean( np.square(np.subtract(NewImage_rs , StartImage[:,half_cols-i:nStartImage_cols-i])))
    
    #for i in range(nStartImage_cols):
    #    print(dif_vector[i])

    print(np.argmin(dif_vector))
    AngleRotation =  62.2/2 - 62.2/nStartImage_cols * (np.argmin(dif_vector)+1) 

    return AngleRotation


x_res = 800
y_res = 48

start_time = time.time()
StartImage = GetGrayImage(x_res,y_res)
#print(wow)
print("Time to get image 1 is %s seconds" % (time.time() - start_time))
start_time = time.time()
NewImage = GetGrayImage(x_res,y_res)
print("Time to get image 2 is %s seconds" % (time.time() - start_time))
start_time = time.time()
AngleRotation = CalcAngleChange(StartImage,NewImage)
print("Time to get delta angle is %s seconds" % (time.time() - start_time))
print("the estimated angle is %s degrees" % AngleRotation)