#!/usr/bin/env python3
#coding=utf-8

import time
from dofbotx_arm_lib import ArmCtrl
from math import pi

def main():
    dofbotx_arm = ArmCtrl()
    # Individually control a steering gear to move to a certain angle
    id = 5

    dofbotx_arm.serial_servo_write(id, 90.0, 500, False)
    dofbotx_arm.serial_servo_write(id, pi/2, 500, True)

if __name__ == "__main__":
    main()