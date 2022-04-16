import serial
import time

def LidarDistance():
    #ser = serial.Serial('/dev/ttyS0',115200,timeout = 1)
    ser = serial.Serial('/dev/serial0',115200,timeout = 1)
    NoDistanceFoundBool = True
    try:
        while(NoDistanceFoundBool):
            count_buf = ser.in_waiting
            if count_buf > 8:
                recv = ser.read(9)
                ser.reset_input_buffer()
                if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                    distance = recv[2] + recv[3] * 256 # Convert hex to int
                    strength = recv[4] + recv[5] * 256 # Convert hex to int
#                     print(distance, 'cm, p=', strength)
                    ser.reset_input_buffer()
                    NoDistanceFoundBool = False
                    
                time.sleep(0.01)
                
    except:
        print("failed")
        
    return distance, strength