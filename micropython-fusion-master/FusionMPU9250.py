# MPU6050 9-DoF Example Printout

from mpu9250_i2c import *
from TLib import *
import time
from fusion import Fusion
from time import perf_counter_ns

time.sleep(1) # delay necessary to allow mpu9250 to settle
fuse = Fusion()

Calibrate = True
Timing = True


if Calibrate:
    print("Calibrating")
    
    CalTime = 0
    startcalTime = time.time()
    print('recording data')
    
    magx = []
    magy = []
    magz = []
    while CalTime < 20:
        CalTime = time.time() - startcalTime
        
        mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
        magx.append(mx)
        magy.append(my)
        magz.append(mz)
        
    fuse.calibrate(magx,magy,magz)
    print(fuse.magbias)
    
if Timing:
    ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
    mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
    mag = [mx,my,mz] # Don't include blocking read in time
    accel = [ax,ay,az] # or i2c
    gyro = [wx,wy,wz]
    start = TDispTimeStart()  # Measure computation time only
    fuse.update(accel, gyro, mag, None) # 1.97mS on Pyboard
    #t = time.ticks_diff(TDsipTimeStop(), start)
    t = (TDsipTimeStop()-start)/1000000
    print("Update time (uS):", t)
    print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))

# # # print('recording data')
# # # while 1:
# # #     #t1 = perf_counter_ns()

import datetime
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot') # matplotlib visual style setting
# prepping for visualization
mpu6050_str = ['accel-x','accel-y','accel-z','gyro-x','gyro-y','gyro-z']
AK8963_str = ['mag-x','mag-y','mag-z']
Heading_str = ['heading-x','heading-y','heading-z']
mpu6050_vec,AK8963_vec,t_vec,Heading_vec = [],[],[],[]
ii = 5000 # number of points
t1p = time.time() # for calculating sample rate
print('recording data')
for ii in range(0,ii):
    t1 = TDispTimeStart()
    
    time.sleep(0.01)
    try:
        
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
        
        mag = [mx,my,mz] # Don't include blocking read in time
        accel = [ax,ay,az] # or i2c
        gyro = [wx,wy,wz]
        
        #dt = TDsipTimeDiff(t1)
        fuse.update(accel, gyro, mag, t1) # 1.97mS on Pyboard
#         print("mx,my,mz,ax,ay,az,wx,wy,wz: {:7.3f} {:7.3f} {:7.3f} {:7.3f} {:7.3f} {:7.3f} {:7.3f} {:7.3f} {:7.3f}".format(mx,my,mz,ax,ay,az,wx,wy,wz))
#         print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))
        
        
    except:
        continue
    
    #time.sleep(0.0015)
    TSetFreqHz(40,t1)
    t2 = TDsipTimeStop()
    #TDispTime(t1,t2)
    
    #TDispMeasurements(ax,ay,az,wx,wy,wz,mx,my,mz)
    
    t_vec.append(time.time()) # capture timestamp
    Heading_vec.append([fuse.heading,fuse.heading,fuse.heading])
    AK8963_vec.append([mx,my,mz])
    mpu6050_vec.append([ax,ay,az,wx,wy,wz])
    
    
fig = plt.figure()
axR = fig.add_subplot(211)
axR2 = fig.add_subplot(212)
AK8963_array = np.array(AK8963_vec)
mx_vec = AK8963_array[:,0]
my_vec = AK8963_array[:,1]
mz_vec = AK8963_array[:,2]

mx_vec_c = mx_vec - fuse.magbias[0]
my_vec_c = my_vec - fuse.magbias[1]
mz_vec_c = mz_vec - fuse.magbias[2]

print('bias is {:}',fuse.magbias)
print('X max: {:}, mean: {:}, min: {:}',max(mx_vec_c),(max(mx_vec_c)+min(mx_vec_c))/2,min(mx_vec_c))
print('Y max: {:}, mean: {:}, min: {:}',max(my_vec_c),(max(my_vec_c)+min(my_vec_c))/2,min(my_vec_c))
print('Z max: {:}, mean: {:}, min: {:}',max(mz_vec_c),(max(mz_vec_c)+min(mz_vec_c))/2,min(mz_vec_c))

axR.scatter(mx_vec, my_vec, s=10, c='r', marker="s", label='mx') # xy
axR.scatter(mx_vec,mz_vec, s=10, c='g', marker="o", label='my')  # xz
axR.scatter(my_vec,mz_vec, s=10, c='b', marker="^", label='mz')  # yz

axR2.scatter(mx_vec_c, my_vec_c, s=10, c='r', marker="s", label='mx') # xy
axR2.scatter(mx_vec_c,mz_vec_c, s=10, c='g', marker="o", label='my') # xz
axR2.scatter(my_vec_c,mz_vec_c, s=10, c='b', marker="^", label='mz') # yz
plt.draw()



t_vec = np.subtract(t_vec,t_vec[0])

print('end of script')

# plot the resulting data in 3-subplots, with each data axis
fig,axs = plt.subplots(4,1,figsize=(12,7),sharex=True)
cmap = plt.cm.Set1

ax = axs[0] # plot accelerometer data
for zz in range(0,np.shape(mpu6050_vec)[1]-3):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax.plot(t_vec,data_vec,label=mpu6050_str[zz],color=cmap(zz))
ax.legend(bbox_to_anchor=(1.12,0.9))
ax.set_ylabel('Acceleration [g]',fontsize=12)

ax2 = axs[1] # plot gyroscope data
for zz in range(3,np.shape(mpu6050_vec)[1]):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax2.plot(t_vec,data_vec,label=mpu6050_str[zz],color=cmap(zz))
ax2.legend(bbox_to_anchor=(1.12,0.9))
ax2.set_ylabel('Angular Vel. [dps]',fontsize=12)

ax3 = axs[2] # plot magnetometer data
for zz in range(0,np.shape(AK8963_vec)[1]):
    data_vec = [ii[zz] for ii in AK8963_vec]
    ax3.plot(t_vec,data_vec,label=AK8963_str[zz],color=cmap(zz+6))
ax3.legend(bbox_to_anchor=(1.12,0.9))
ax3.set_ylabel('Magn. Field [Î¼T]',fontsize=12)
ax3.set_xlabel('Time [s]',fontsize=14)

ax4 = axs[3] # plot magnetometer data
for zz in range(0,np.shape(Heading_vec)[1]):
    data_vec = [ii[zz] for ii in Heading_vec]
    ax4.plot(t_vec,data_vec,label=Heading_str[zz],color=cmap(zz+6))
ax4.legend(bbox_to_anchor=(1.12,0.9))
ax4.set_ylabel('Magn. Field [Î¼T]',fontsize=12)
ax4.set_xlabel('Time [s]',fontsize=14)


fig.align_ylabels(axs)
plt.show()