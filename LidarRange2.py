import serial
import time

# Python program to show time by process_time_ns() 
from time import process_time_ns 

#ser = serial.Serial('/dev/ttyS0',115200,timeout = 1)
ser = serial.Serial('/dev/serial0',115200,timeout = 1)

try:
    while(True):
        count_buf = ser.in_waiting
        if count_buf > 8:
            
            # Start the timer
            t1_start = process_time_ns() 
            
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                distance = recv[2] + recv[3] * 256 # Convert hex to int
                strength = recv[4] + recv[5] * 256 # Convert hex to int
                print(distance, 'cm, p=', strength)
                ser.reset_input_buffer()
                time.sleep(0.1)
                
            # Stop the timer 
            t1_stop = process_time_ns()
            #print("Elapsed time:", t1_stop, t1_start) 
            print("Time :",(t1_stop-t1_start)/1000000," [s]") 
            
except:
        print("failed")
    
    
    









