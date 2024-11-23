#!/usr/bin/env python3
#coding=utf-8
import time
from FakeArm_Lib import FakeArmDevice

Arm = FakeArmDevice()

# Control the motion of six steering gears at the same time and gradually change the angle

def get_servos_pos():
    values = []
    for id in range(1,6):
        values.append(Arm.Arm_serial_servo_read(id)["servos_pos"][0])

    return values

def ctrl_all_servo(angle, s_time = 500):
    resp = Arm.Arm_serial_servo_write6(angle, 180-angle, angle, angle, angle, angle, s_time)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}, {resp['args'][3]}, {resp['args'][4]}, {resp['args'][5]}, {resp['args'][6]}) -> Compute pos: {resp['servos_pos']}")
    time.sleep(s_time/1000)
    servo_pos = get_servos_pos()
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo_pos})")

def main():
    dir_state = 1
    angle = 90
    
    # Reset and center the steering gear
    
    resp = Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}, {resp['args'][3]}, {resp['args'][4]}, {resp['args'][5]}, {resp['args'][6]}) -> Compute pos: {resp['servos_pos']}")
    time.sleep(1)
    servo_pos = get_servos_pos()
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo_pos})")

    
    if dir_state == 1:
        angle += 1
        if angle >= 180:
            dir_state = 0
    else:
        angle -= 1
        if angle <= 0:
            dir_state = 1
    
    ctrl_all_servo(angle, 10)
    time.sleep(10/1000)
    # print(angle)

    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

