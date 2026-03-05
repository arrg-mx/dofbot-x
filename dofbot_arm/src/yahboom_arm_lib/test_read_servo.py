#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

Arm = Arm_Device()
time.sleep(.1)
# Read the angles of all steering gears and print them out circularly
def main():
    n = 0
    aa = [0,0,0,0,0,0]
    while True:
        for i in range(6):
            aa[i] = Arm.Arm_serial_servo_read(i+1)
#            print(aa)
            time.sleep(.01)
        print(f"[{n}] Servo Read: {aa}")
        time.sleep(.5)
        n += 1
        #print(" END OF LINE! ")

    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass
