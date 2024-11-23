#!/usr/bin/env python3
#coding: utf-8
# import smbus
import time
# V0.0.4

class FakeArmDevice(object):

    def __init__(self):
        self.addr = 0x15
        self.servo_pos = [0, 0, 0, 0, 0, 0]
        # self.bus = smbus.SMBus(1)

    def get_bus_func_dict(self, bus_func_name, addr, reg, data):
        return {
            "bus_func": bus_func_name,
            "address_1": addr,
            "reg_1": reg, 
            "bus_data": data, 
        }

    def get_servo_pos(self):
        return self.servo_pos

    # Set the bus servo angle interface: id: 1-6 (0 means sending 6 servos) angle: 0-180 Set the angle to which the servo will move.
    def Arm_serial_servo_write(self, id, angle, time):
        if id == 0:  # This is all servo controls
            return self.Arm_serial_servo_write6(angle, angle, angle, angle, angle, angle, time)
        elif id == 2 or id == 3 or id == 4:  # Opposite angle to reality
            angle = 180 - angle
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            self.servo_pos[id-1] = pos

            return {
                "function_name": "Arm_serial_servo_write",
                "args": [id, angle, time],
                "servos_pos": [pos],
                "bus_ops": [self.get_bus_func_dict(
                    "write_i2c_block_data",
                    self.addr,
                    0x10 + id,
                    [value_H, value_L, time_H, time_L]         
                )]
            }

        elif id == 5:
            pos = int((3700 - 380) * (angle - 0) / (270 - 0) + 380)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            self.servo_pos[id-1] = pos

            return {
                "function_name": "Arm_serial_servo_write",
                "args": [id, angle, time],
                "servos_pos": [pos],
                "bus_ops": [self.get_bus_func_dict(
                    "write_i2c_block_data",
                    self.addr,
                    0x10 + id,
                    [value_H, value_L, time_H, time_L]         
                )]
            }

        else:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            self.servo_pos[id-1] = pos

            return {
                "function_name": "Arm_serial_servo_write",
                "args": [id, angle, time],
                "servos_pos": [pos],
                "bus_ops": [self.get_bus_func_dict(
                    "write_i2c_block_data",
                    self.addr,
                    0x10 + id,
                    [value_H, value_L, time_H, time_L]         
                )]
            }


    # Set any bus servo angle interface: id: 1-250 (0 is group transmission) angle: 0-180 means 900 3100 0 - 180
    def Arm_serial_servo_write_any(self, id, angle, time):
        if id != 0:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            self.servo_pos[id-1] = pos

            return {
                "function_name": "Arm_serial_servo_write_any",
                "args": [id, angle, time],
                "servos_pos": [pos],
                "bus_ops": [self.get_bus_func_dict(
                    "write_i2c_block_data",
                    self.addr,
                    0x19,
                    [id & 0xff, value_H, value_L, time_H, time_L]         
                )]
            }

        elif id == 0:  # This is all servo controls
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            self.servo_pos = [pos for element in range(6)]

            return {
                "function_name": "Arm_serial_servo_write_any",
                "args": [id, angle, time],
                "servos_pos": [pos],
                "bus_ops": [self.get_bus_func_dict(
                    "write_i2c_block_data",
                    self.addr,
                    0x17,
                    [value_H, value_L, time_H, time_L]         
                )]
            }


    # Set the bus servo neutral offset with one click, power on and move to the neutral position, and then send the following function, id: 1-6 (setting), 0 (restore to initial)
    def Arm_serial_servo_write_offset_switch(self, id):
        if id > 0 and id < 7:
            return {
                "function_name": "Arm_serial_servo_write_offset_switch",
                "args": id,
                "servos_pos": [-1],
                "bus_ops": [self.get_bus_func_dict(
                    "write_byte_data",
                    self.addr,
                    0x1c,
                    [id]         
                )]
            }
        elif id == 0:
            return {
                "function_name": "Arm_serial_servo_write_offset_switch",
                "args": id,
                "servos_pos": [-1],
                "bus_ops": [self.get_bus_func_dict(
                    "write_byte_data",
                    self.addr,
                    0x1c,
                    [0x00]         
                )]
            }

    # Read the status of the one-click setting bus servo mid-bit offset. 
    #   0 means that the corresponding servo ID cannot be found, 
    #   1 means success, and 2 means failure is out of range.
    def Arm_serial_servo_write_offset_state(self):
        return {
            "function_name": "Arm_serial_servo_write_offset_state",
            "args": None,
            "servos_pos": [-1],
            "bus_ops": [self.get_bus_func_dict(
                "write_byte_data",
                self.addr,
                0x1b,
                [0x01]         
            ), self.get_bus_func_dict(
                "read_byte_data",
                self.addr,
                0x1b,
                [0x01]  # "0 - Servo not found, 1 - Servo found, 2 - Fail (out of range)" 
            )]
        }

    # Set the bus servo angle interface: array
    def Arm_serial_servo_write6_array(self, joints, time):
        s1, s2, s3, s4, s5, s6 = joints[0], joints[1], joints[2], joints[3], joints[4], joints[5]
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")
            return None

        pos1 = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
        value1_H = (pos1 >> 8) & 0xFF
        value1_L = pos1 & 0xFF

        s2 = 180 - s2
        pos2 = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
        value2_H = (pos2 >> 8) & 0xFF
        value2_L = pos2 & 0xFF

        s3 = 180 - s3
        pos3 = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
        value3_H = (pos3 >> 8) & 0xFF
        value3_L = pos3 & 0xFF

        s4 = 180 - s4
        pos4 = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
        value4_H = (pos4 >> 8) & 0xFF
        value4_L = pos4 & 0xFF

        pos5 = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
        value5_H = (pos5 >> 8) & 0xFF
        value5_L = pos5 & 0xFF

        pos6 = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
        value6_H = (pos6 >> 8) & 0xFF
        value6_L = pos6 & 0xFF
        time_H = (time >> 8) & 0xFF
        time_L = time & 0xFF

        data = [value1_H, value1_L, value2_H, value2_L, value3_H, value3_L,
                value4_H, value4_L, value5_H, value5_L, value6_H, value6_L]
        timeArr = [time_H, time_L]
        s_id = 0x1d

        self.servo_pos = [pos1, pos2, pos3, pos4, pos5, pos6]

        return {
            "function_name": "Arm_serial_servo_write6_array",
            "args": [joints, time],
            "servos_pos": self.servo_pos,
            "bus_ops": [self.get_bus_func_dict(
                "write_i2c_block_data",
                self.addr,
                0x1e,
                timeArr         
            ), self.get_bus_func_dict(
                "write_i2c_block_data",
                self.addr,
                s_id,
                data         
            )]
        }

    # Set the bus servo angle interface: s1~S4 and s6: 0-180, S5: 0~270, time is the running time
    def Arm_serial_servo_write6(self, s1, s2, s3, s4, s5, s6, time):
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")
            return None
        
        pos1 = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
        value1_H = (pos1 >> 8) & 0xFF
        value1_L = pos1 & 0xFF

        s2 = 180 - s2
        pos2 = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
        value2_H = (pos2 >> 8) & 0xFF
        value2_L = pos2 & 0xFF

        s3 = 180 - s3
        pos3 = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
        value3_H = (pos3 >> 8) & 0xFF
        value3_L = pos3 & 0xFF

        s4 = 180 - s4
        pos4 = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
        value4_H = (pos4 >> 8) & 0xFF
        value4_L = pos4 & 0xFF

        pos5 = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
        value5_H = (pos5 >> 8) & 0xFF
        value5_L = pos5 & 0xFF

        pos6 = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
        value6_H = (pos6 >> 8) & 0xFF
        value6_L = pos6 & 0xFF
        time_H = (time >> 8) & 0xFF
        time_L = time & 0xFF

        data = [value1_H, value1_L, value2_H, value2_L, value3_H, value3_L,
                value4_H, value4_L, value5_H, value5_L, value6_H, value6_L]
        timeArr = [time_H, time_L]
        s_id = 0x1d

        self.servo_pos = [pos1, pos2, pos3, pos4, pos5, pos6]

        return {
            "function_name": "Arm_serial_servo_write6",
            "args": [s1, s2, s3, s4, s5, s6, time],
            "servos_pos": self.servo_pos,
            "bus_ops": [self.get_bus_func_dict(
                "write_i2c_block_data",
                self.addr,
                0x1e,
                timeArr         
            ), self.get_bus_func_dict(
                "write_i2c_block_data",
                self.addr,
                s_id,
                data         
            )]
        }


    # Read the specified servo angle, id: 1-6, return 0-180, read error return None
    def Arm_serial_servo_read(self, id):
        if id < 1 or id > 6:
            print("id must be 1 - 6")
            return None

        pos = self.servo_pos[id-1]

        retval = {
            "function_name": "Arm_serial_servo_read",
            "args": id,
            "servos_pos": [],
            "bus_ops": [self.get_bus_func_dict(
                "write_byte_data",
                self.addr,
                id + 0x30,
                [0x00]         
            ), self.get_bus_func_dict(
                "read_word_data",
                self.addr,
                id + 0x30,
                [0x00]         
            )]
        }

        if pos == 0:
            return retval

        if id == 5:
            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
            if pos > 270 or pos < 0:
                retval["servos_pos"] = [-1]
                return retval
        else:
            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
            if pos > 180 or pos < 0:
                retval["servos_pos"] = [-1]
                return retval
        if id == 2 or id == 3 or id == 4:
            pos = 180 - pos

        retval["servos_pos"] = [pos]
        return retval

    # Read the bus servo angle, id: 1-250, return 0-180
    def Arm_serial_servo_read_any(self, id):
        if id < 1 or id > 250:
            print("id must be 1 - 250")
            return None

        pos = self.servo_pos[id-1]

        retval = {
            "function_name": "Arm_serial_servo_read_any",
            "args": id,
            "servos_pos": [],
            "bus_ops": [self.get_bus_func_dict(
                "write_byte_data",
                self.addr,
                0x37,
                [id]         
            ), self.get_bus_func_dict(
                "read_word_data",
                self.addr,
                0x37,
                [0x00]         
            )]
        }

        pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
        retval["servos_pos"] = [pos]
        return retval


    # Read the servo status, normal return is 0xda, if no data can be read, 
    # return 0x00, other values ​​​​are servo errors.
    def Arm_ping_servo(self, id):
        data = int(id)
        if data > 0 and data <= 250:
            reg = 0x38
            retval = {
                "function_name": "Arm_ping_servo",
                "args": id,
                "servos_pos": [],
                "bus_ops": [self.get_bus_func_dict(
                    "write_byte_data",
                    self.addr,
                    reg,
                    [data]         
                ), self.get_bus_func_dict(
                    "read_word_data",
                    self.addr,
                    0x37,
                    [0xda if (data > 0 and data < 7) else 0x00]         
                )]
            }
            return retval
        else:
            return None

    # Read hardware version number
    def Arm_get_hardversion(self):
        try:
            self.bus.write_byte_data(self.addr, 0x01, 0x01)
            time.sleep(.001)
            value = self.bus.read_byte_data(self.addr, 0x01)
        except:
            print('Arm_get_hardversion I2C error')
            return None
        retval = {
            "function_name": "Arm_get_hardversion",
            "args": id,
            "bus_time": "write_byte_data",
            "address_1": self.addr, 
            "reg_1": 0x01, 
            "byte_stream_1": 0x01, 
            "bus_pos": "read_byte_data",
            "address_2": self.addr, 
            "reg_2": 0x01, 
            "value": "V0.0.4"
        }

        return retval

    # Torque switch 1: Open torque 0: Close torque (can be turned)
    def Arm_serial_set_torque(self, onoff):
        return {
            "function_name": "Arm_serial_set_torque",
            "args": onoff,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x1A, 
            "out_byte_stream": 0x01 if onoff == 1 else 0x00
        }

    # Set the bus servo number
    def Arm_serial_set_id(self, id):
        return {
            "function_name": "Arm_serial_set_id",
            "args": id,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x18, 
            "out_byte_stream": id & 0xff
        }

    # Set the current product color to 1~6, and the RGB light will turn on corresponding color.
    def Arm_Product_Select(self, index):
        return {
            "function_name": "Arm_Product_Select",
            "args": index,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x04, 
            "out_byte_stream": index & 0xff
        }

    # Set RGB lights to specify colors
    def Arm_RGB_set(self, red, green, blue):
        return {
            "function_name": "Arm_RGB_set",
            "args": [red, green, blue],
            "call": "write_i2c_block_data",
            "address": self.addr, 
            "register": 0x02, 
            "out_byte_stream": [red & 0xff, green & 0xff, blue & 0xff]
        }

    # Set K1 button mode, 0: default mode 1: learning mode
    def Arm_Button_Mode(self, mode):
        return {
            "function_name": "Arm_Button_Mode",
            "args": mode,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x03, 
            "out_byte_stream": mode & 0xff
        }

    # Restart the driver board
    def Arm_reset(self):
        return {
            "function_name": "Arm_reset",
            "args": "",
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x05, 
            "out_byte_stream": 0x01
        }

    # PWD servo control id:1-6 (0 controls all servos) angle: 0-180
    def Arm_PWM_servo_write(self, id, angle):
        return {
            "function_name": "Arm_PWM_servo_write",
            "args": [id, angle],
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x57 if id == 0 else (0x50 + id), 
            "out_byte_stream": angle & 0xff
        }

    # Clear action group
    def Arm_Clear_Action(self):
        return {
            "function_name": "Arm_Clear_Action",
            "args": "",
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x23, 
            "out_byte_stream": 0x01
        }

    # In learning mode, record the current action once
    def Arm_Action_Study(self):
        return {
            "function_name": "Arm_Action_Study",
            "args": "",
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x24, 
            "out_byte_stream": 0x01
        }

    # Action group operation mode 0: Stop operation 1: Single operation 2: Cycle operation
    def Arm_Action_Mode(self, mode):
        return {
            "function_name": "Arm_Action_Mode",
            "args": mode,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x20, 
            "out_byte_stream": mode & 0xff
        }

    # Read the number of saved action groups
    def Arm_Read_Action_Num(self):
        return {
            "function_name": "Arm_Read_Action_Num",
            "args": id,
            "bus_time": "write_byte_data",
            "address_1": self.addr, 
            "reg_1": 0x22, 
            "byte_stream_1": 0x01, 
            "bus_pos": "read_byte_data",
            "address_2": self.addr, 
            "reg_2": 0x22, 
            "value": 0
        }

    # Turn on the buzzer, delay defaults to 0xff, and the buzzer keeps sounding.
    # delay=1~50, after turning on the buzzer, it will automatically turn off after delay*100 milliseconds. The maximum delay time is 5 seconds.
    def Arm_Buzzer_On(self, delay=0xff):
        if delay != 0:
            return {
                "function_name": "Arm_Buzzer_On",
                "args": delay,
                "call": "write_byte_data",
                "address": self.addr, 
                "register": 0x06, 
                "out_byte_stream": delay&0xff
            }
        
        return None

    # Turn off the buzzer
    def Arm_Buzzer_Off(self):
        return {
            "function_name": "Arm_Buzzer_Off",
            "args": None,
            "call": "write_byte_data",
            "address": self.addr, 
            "register": 0x06, 
            "out_byte_stream": 0x00
        }

