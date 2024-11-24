#!/usr/bin/env python3
#coding=utf-8

import time
from FakeArm_Lib import FakeArmDevice

Arm = FakeArmDevice()

# Individually control a steering gear to move to a certain angle
id = 6

resp = Arm.Arm_serial_servo_write(id, 90, 500)
# 'function_name': 'Arm_serial_servo_write', 'args': [6, 90, 500], 'servos_pos': [2000]
print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}) -> Compute pos: {resp['servos_pos'][0]}")
servo6_pos = Arm.Arm_serial_servo_read(id)
print(f"Servos Pos: {Arm.get_servo_pos()} -> {servo6_pos.get('servos_pos')[0]}")

# Control a steering gear cycle switching angle
# id = 6

def main():
    print(f"Arm.Arm_serial_servo_write({id}, 120, 500)")
    resp = Arm.Arm_serial_servo_write(id, 120, 500)
    # print(resp)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}) -> Compute pos: {resp['servos_pos'][0]}")
    servo6_pos = Arm.Arm_serial_servo_read(id)
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo6_pos.get('servos_pos')[0]})")
    time.sleep(1)

    print(f"Arm.Arm_serial_servo_write({id}, 50, 500)")
    resp = Arm.Arm_serial_servo_write(id, 50, 500)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}) -> Compute pos: {resp['servos_pos'][0]}")
    servo6_pos = Arm.Arm_serial_servo_read(id)
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo6_pos.get('servos_pos')[0]})")
    time.sleep(1)

    print(f"Arm.Arm_serial_servo_write({id}, 120, 500)")
    resp = Arm.Arm_serial_servo_write(id, 120, 500)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}) -> Compute pos: {resp['servos_pos'][0]}")
    servo6_pos = Arm.Arm_serial_servo_read(id)
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo6_pos.get('servos_pos')[0]})")
    time.sleep(1)

    print(f"Arm.Arm_serial_servo_write({id}, 180, 500)")
    resp = Arm.Arm_serial_servo_write(id, 180, 500)
    print(f"{resp['function_name']}({resp['args'][0]}, {resp['args'][1]}, {resp['args'][2]}) -> Compute pos: {resp['servos_pos'][0]}")
    servo6_pos = Arm.Arm_serial_servo_read(id)
    print(f"Servos Pos: {Arm.get_servo_pos()}, target({resp.get('args')[1]}) -> reads({servo6_pos.get('servos_pos')[0]})")
    time.sleep(1)


try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass
