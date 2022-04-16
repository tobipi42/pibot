from time import perf_counter_ns
import time

def TDispTime(t1,t2):
    print("T [ms] {:08.4f} F [Hz] {:05.2f}".format((t2-t1)/1000000,1000000000/(t2-t1)))
    return 

def TDispTimeStart():
    t = perf_counter_ns()
    return t


def TDsipTimeStop():
    t = perf_counter_ns()
    return t


def TDispMeasurements(ax,ay,az,wx,wy,wz,mx,my,mz):
    print('{}'.format('-'*30))
    print('accel [g]  : x = {:08.4f}, y = {:08.4f}, z = {:08.4f}'.format(ax,ay,az))
    print('gyro  [dps]: x = {:08.4f}, y = {:08.4f}, z = {:08.4f}'.format(wx,wy,wz))
    print('mag   [uT] : x = {:08.4f}, y = {:08.4f}, z = {:08.4f}'.format(mx,my,mz))
    print('{}'.format('-'*30))
    return

def TSetFreqHz(TargetInput,t1):
    TargetT = 1/TargetInput
    t2 = TDsipTimeStop()
    print("Freq [Hz]: {:}, Max Freq [Hz]: {:05.2f}, Sleeping [s]: {:08.4f}".
          format(TargetInput,1000000000/(t2 - t1),max(0,TargetT-(t2 - t1)/1000000000)))
    time.sleep( max(0,TargetT - (t2 - t1)/1000000000 - 0.0007) )
    
    return

