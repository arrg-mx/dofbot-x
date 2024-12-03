#!/usr/bin/env python3
#coding=utf-8

import time

from dofbotx_arm_lib import ArmCtrl
from math import pi
# import logging


def main():
    arm_device = ArmCtrl()
    # Individually control a steering gear to move to a certain angle
    id = 1

    print("Inspect 'serial_servo_write'")
    inspect = arm_device.serial_servo_write(id, 225.0, 500, False)
    if inspect or len(inspect)>0: print(
        f"[TO_SEND (id: {inspect[0]} pos: {inspect[1]}, {'rads' if inspect[3] else 'deg'})] -> servo pos: {inspect[5]}, reg: {inspect[4]:02x}, data: [{inspect[6]:02x}, {inspect[7]:02x}, {inspect[8]:02x}, {inspect[9]:02x}]"
    )
    inspect = arm_device.serial_servo_write(id, (5*pi)/4, 500, True)
    print(
        f"[TO_SEND (id: {inspect[0]} pos: {inspect[1]}, {'rads' if inspect[3] else 'deg'})] -> servo pos: {inspect[5]}, reg: {inspect[4]:02x}, data: [{inspect[6]:02x}, {inspect[7]:02x}, {inspect[8]:02x}, {inspect[9]:02x}]"
    )

    time.sleep(1.0)
    id = 0
    print("Inspect 'serial_servo_write' for all servos (id=0)")
    inspect = arm_device.serial_servo_write(id, 60.0, 500, False)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )
    inspect = arm_device.serial_servo_write(id, pi/3, 500, True)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )

    time.sleep(1.0)
    print("Inspect 'serial_servo_write_any'")
    id = 2
    inspect = arm_device.serial_servo_write_any(id, 60.0, 500, False)
    print(
        f"[TO_SEND (id: {inspect[0]} pos: {inspect[1]}, {'rads' if inspect[3] else 'deg'})] -> servo pos: {inspect[4]}, reg: {inspect[5]:02x}, data: [{inspect[6]:02x}, {inspect[7]:02x}, {inspect[8]:02x}, {inspect[9]:02x}, {inspect[10]:02x}]"
    )
    inspect = arm_device.serial_servo_write_any(id, pi/3, 500, True)
    print(
        f"[TO_SEND (id: {inspect[0]} pos: {inspect[1]}, {'rads' if inspect[3] else 'deg'})] -> servo pos: {inspect[4]}, reg: {inspect[5]:02x}, data: [{inspect[6]:02x}, {inspect[7]:02x}, {inspect[8]:02x}, {inspect[9]:02x}, {inspect[10]:02x}]"
    )
    id = 0
    inspect = arm_device.serial_servo_write_any(id, 60.0, 500, False)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )

    time.sleep(1.0)
    print("Inspect 'serial_servo_write_all_array'")
    inspect = arm_device.serial_servo_write_all_array([120, 120, 120, 120, 120, 120], duration=500, in_radians=False)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )
    inspect = arm_device.serial_servo_write_all_array([(2*pi)/3, (2*pi)/3, (2*pi)/3, (2*pi)/3, (2*pi)/3, (2*pi)/3], duration=500, in_radians=True)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )

    time.sleep(1.0)
    print("Inspect 'serial_servo_write_all'")
    inspect = arm_device.serial_servo_write_all(s1=150, s2=150, s3=150, s4=150, s5=150, s6=150, duration=500, in_radians=False)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )
    inspect = arm_device.serial_servo_write_all(s1=(5*pi)/6, s2=(5*pi)/6, s3=(5*pi)/6, s4=(5*pi)/6, s5=(5*pi)/6, s6=(5*pi)/6, duration=500, in_radians=True)
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> duration: {inspect[1]}, reg: {inspect[3]:02x}, data: [{inspect[4]:02x}, {inspect[5]:02x}]"
    )
    print(
        f"[TO_SEND (joints: {inspect[0]}, {'rads' if inspect[2] else 'deg'})] -> servo pos: {inspect[7]}, reg: {inspect[6]:02x}, data: {inspect[8]}"
    )


if __name__ == "__main__":
    main()