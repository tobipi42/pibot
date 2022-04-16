# MPU6050 9-DoF Example Printout

from mpu9250_i2c import *
from TLib import *

time.sleep(1) # delay necessary to allow mpu9250 to settle

from time import perf_counter_ns

print('recording data')
while 1:
    #t1 = perf_counter_ns()
    
    t1 = TDispTimeStart()
    
    time.sleep(0.01)
    try:
        
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
    except:
        continue
    
    
    #time.sleep(0.0015)
    TSetFreqHz(50,t1)
    t2 = TDsipTimeStop()
    TDispTime(t1,t2)
    
    TDispMeasurements(ax,ay,az,wx,wy,wz,mx,my,mz)
    