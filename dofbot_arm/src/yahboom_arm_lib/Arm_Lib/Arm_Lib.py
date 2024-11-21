#!/usr/bin/env python3
#coding: utf-8
import smbus
import time
# V0.0.4

class Arm_Device(object):

    def __init__(self):
        self.addr = 0x15
        self.bus = smbus.SMBus(1)

    # 设置总线舵机角度接口：id: 1-6(0是发6个舵机) angle: 0-180 设置舵机要运动到的角度
    # Set the bus servo angle interface: id: 1-6 (0 means sending 6 servos) angle: 0-180 Set the angle to which the servo will move.
    def Arm_serial_servo_write(self, id, angle, time):
        if id == 0:  # 此为所有舵机控制 | This is all servo controls
            self.Arm_serial_servo_write6(angle, angle, angle, angle, angle, angle, time)
        elif id == 2 or id == 3 or id == 4:  # 与实际相反角度 | Opposite angle to reality
            angle = 180 - angle
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            try:
                self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            except:
                print('Arm_serial_servo_write I2C error')
        elif id == 5:
            pos = int((3700 - 380) * (angle - 0) / (270 - 0) + 380)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            try:
                self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            except:
                print('Arm_serial_servo_write I2C error')
        else:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            try:
                self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            except:
                print('Arm_serial_servo_write I2C error')

    # 设置任意总线舵机角度接口：id: 1-250(0是群发) angle: 0-180  表示900 3100   0 - 180
    # Set any bus servo angle interface: id: 1-250 (0 is group transmission) angle: 0-180 means 900 3100 0 - 180
    def Arm_serial_servo_write_any(self, id, angle, time):
        if id != 0:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            try:
                self.bus.write_i2c_block_data(self.addr, 0x19, [id & 0xff, value_H, value_L, time_H, time_L])
            except:
                print('Arm_serial_servo_write_any I2C error')
        elif id == 0:  # 此为所有舵机控制 | This is all servo controls
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            try:
                self.bus.write_i2c_block_data(self.addr, 0x17, [value_H, value_L, time_H, time_L])
            except:
                print('Arm_serial_servo_write_any I2C error')

    # 一键设置总线舵机中位偏移，上电搬动到中位，然后发送下面函数，id:1-6(设置)，0（恢复初始）
    # Set the bus servo neutral offset with one click, power on and move to the neutral position, and then send the following function, id: 1-6 (setting), 0 (restore to initial)
    def Arm_serial_servo_write_offset_switch(self, id):
        try:
            if id > 0 and id < 7:
                self.bus.write_byte_data(self.addr, 0x1c, id)
            elif id == 0:
                self.bus.write_byte_data(self.addr, 0x1c, 0x00)
                time.sleep(.5)
        except:
            print('Arm_serial_servo_write_offset_switch I2C error')

    # 读取一键设置总线舵机中位偏移的状态，0表示找不到对应舵机ID，1表示成功，2表示失败超出范围
    # Read the status of the one-click setting bus servo mid-bit offset. 
    #   0 means that the corresponding servo ID cannot be found, 
    #   1 means success, and 2 means failure is out of range.
    def Arm_serial_servo_write_offset_state(self):
        try:
            self.bus.write_byte_data(self.addr, 0x1b, 0x01)
            time.sleep(.001)
            state = self.bus.read_byte_data(self.addr, 0x1b)
            return state
        except:
            print('Arm_serial_servo_write_offset_state I2C error')
        return None

    # 设置总线舵机角度接口：array
    # Set the bus servo angle interface: array
    def Arm_serial_servo_write6_array(self, joints, time):
        s1, s2, s3, s4, s5, s6 = joints[0], joints[1], joints[2], joints[3], joints[4], joints[5]
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")     # print("参数传入范围不在0-180之内！")
            return
        try:
            pos = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
            value1_H = (pos >> 8) & 0xFF
            value1_L = pos & 0xFF

            s2 = 180 - s2
            pos = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
            value2_H = (pos >> 8) & 0xFF
            value2_L = pos & 0xFF

            s3 = 180 - s3
            pos = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
            value3_H = (pos >> 8) & 0xFF
            value3_L = pos & 0xFF

            s4 = 180 - s4
            pos = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
            value4_H = (pos >> 8) & 0xFF
            value4_L = pos & 0xFF

            pos = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
            value5_H = (pos >> 8) & 0xFF
            value5_L = pos & 0xFF

            pos = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
            value6_H = (pos >> 8) & 0xFF
            value6_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            data = [value1_H, value1_L, value2_H, value2_L, value3_H, value3_L,
                    value4_H, value4_L, value5_H, value5_L, value6_H, value6_L]
            timeArr = [time_H, time_L]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.addr, 0x1e, timeArr)
            self.bus.write_i2c_block_data(self.addr, s_id, data)
        except:
            print('Arm_serial_servo_write6 I2C error')

    # 设置总线舵机角度接口：s1~S4和s6: 0-180，S5：0~270,time是运行的时间
    # Set the bus servo angle interface: s1~S4 and s6: 0-180, S5: 0~270, time is the running time
    def Arm_serial_servo_write6(self, s1, s2, s3, s4, s5, s6, time):
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")       # print("参数传入范围不在0-180之内！")
            return
        try:
            pos = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
            value1_H = (pos >> 8) & 0xFF
            value1_L = pos & 0xFF

            s2 = 180 - s2
            pos = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
            value2_H = (pos >> 8) & 0xFF
            value2_L = pos & 0xFF

            s3 = 180 - s3
            pos = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
            value3_H = (pos >> 8) & 0xFF
            value3_L = pos & 0xFF

            s4 = 180 - s4
            pos = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
            value4_H = (pos >> 8) & 0xFF
            value4_L = pos & 0xFF

            pos = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
            value5_H = (pos >> 8) & 0xFF
            value5_L = pos & 0xFF

            pos = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
            value6_H = (pos >> 8) & 0xFF
            value6_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF

            data = [value1_H, value1_L, value2_H, value2_L, value3_H, value3_L,
                    value4_H, value4_L, value5_H, value5_L, value6_H, value6_L]
            timeArr = [time_H, time_L]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.addr, 0x1e, timeArr)
            self.bus.write_i2c_block_data(self.addr, s_id, data)
        except:
            print('Arm_serial_servo_write6 I2C error')

    # 读取指定舵机角度，id: 1-6 返回0-180，读取错误返回None
    # Read the specified servo angle, id: 1-6, return 0-180, read error return None
    def Arm_serial_servo_read(self, id):
        if id < 1 or id > 6:
            print("id must be 1 - 6")
            return None
        try:
            self.bus.write_byte_data(self.addr, id + 0x30, 0x0)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.addr, id + 0x30)
        except:
            print('Arm_serial_servo_read I2C error')
            return None
        if pos == 0:
            return None
        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        # print(pos)
        if id == 5:
            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
            if pos > 270 or pos < 0:
                return None
        else:
            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
            if pos > 180 or pos < 0:
                return None
        if id == 2 or id == 3 or id == 4:
            pos = 180 - pos
        # print(pos)
        return pos

    # 读取总线舵机角度，id: 1-250 返回0-180
    # Read the bus servo angle, id: 1-250, return 0-180
    def Arm_serial_servo_read_any(self, id):
        if id < 1 or id > 250:
            print("id must be 1 - 250")
            return None
        try:
            self.bus.write_byte_data(self.addr, 0x37, id)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.addr, 0x37)
        except:
            print('Arm_serial_servo_read_any I2C error')
            return None
        # print(pos)
        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        # print(pos)
        pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
        # print(pos)
        return pos

    # 读取舵机状态，正常返回0xda, 读不到数据返回0x00，其他值为舵机错误
    # Read the servo status, normal return is 0xda, if no data can be read, return 0x00, other values ​​​​are servo errors.
    def Arm_ping_servo(self, id):
        data = int(id)
        if data > 0 and data <= 250:
            reg = 0x38
            self.bus.write_byte_data(self.addr, reg, data)
            time.sleep(.003)
            value = self.bus.read_byte_data(self.addr, reg)
            times = 0
            while value == 0 and times < 5:
                self.bus.write_byte_data(self.addr, reg, data)
                time.sleep(.003)
                value = self.bus.read_byte_data(self.addr, reg)
                times += 1
                if times >= 5:
                    return None
            return value
        else:
            return None

    # 读取硬件版本号
    # Read hardware version number
    def Arm_get_hardversion(self):
        try:
            self.bus.write_byte_data(self.addr, 0x01, 0x01)
            time.sleep(.001)
            value = self.bus.read_byte_data(self.addr, 0x01)
        except:
            print('Arm_get_hardversion I2C error')
            return None
        version = str(0) + '.' + str(value)
        # print(version)
        return version

    # 扭矩开关 1：打开扭矩  0：关闭扭矩（可以掰动）
    # Torque switch 1: Open torque 0: Close torque (can be turned)
    def Arm_serial_set_torque(self, onoff):
        try:
            if onoff == 1:
                self.bus.write_byte_data(self.addr, 0x1A, 0x01)
            else:
                self.bus.write_byte_data(self.addr, 0x1A, 0x00)
        except:
            print('Arm_serial_set_torque I2C error')

    # 设置总线舵机的编号
    # Set the bus servo number
    def Arm_serial_set_id(self, id):
        try:
            self.bus.write_byte_data(self.addr, 0x18, id & 0xff)
        except:
            print('Arm_serial_set_id I2C error')

    # 设置当前产品颜色 1~6，RGB灯亮对应的颜色。
    # Set the current product color to 1~6, and the RGB light will turn on corresponding color.
    def Arm_Product_Select(self, index):
        try:
            self.bus.write_byte_data(self.addr, 0x04, index & 0xff)
        except:
            print('Arm_Product_Select I2C error')

    # 设置RGB灯指定颜色
    # Set RGB lights to specify colors
    def Arm_RGB_set(self, red, green, blue):
        try:
            self.bus.write_i2c_block_data(self.addr, 0x02, [red & 0xff, green & 0xff, blue & 0xff])
        except:
            print('Arm_RGB_set I2C error')

    # 设置K1按键模式， 0：默认模式 1：学习模式
    # Set K1 button mode, 0: default mode 1: learning mode
    def Arm_Button_Mode(self, mode):
        try:
            self.bus.write_byte_data(self.addr, 0x03, mode & 0xff)
        except:
            print('Arm_Button_Mode I2C error')

    # 重启驱动板
    # Restart the driver board
    def Arm_reset(self):
        try:
            self.bus.write_byte_data(self.addr, 0x05, 0x01)
        except:
            print('Arm_reset I2C error')

    # PWD舵机控制 id:1-6(0控制所有舵机) angle：0-180
    # PWD servo control id:1-6 (0 controls all servos) angle: 0-180
    def Arm_PWM_servo_write(self, id, angle):
        try:
            if id == 0:
                self.bus.write_byte_data(self.addr, 0x57, angle & 0xff)
            else:
                self.bus.write_byte_data(self.addr, 0x50 + id, angle & 0xff)
        except:
            print('Arm_PWM_servo_write I2C error')

    # 清空动作组
    # Clear action group
    def Arm_Clear_Action(self):
        try:
            self.bus.write_byte_data(self.addr, 0x23, 0x01)
        except:
            print('Arm_Clear_Action I2C error')

    # 学习模式下，记录一次当前动作
    # In learning mode, record the current action once
    def Arm_Action_Study(self):
        try:
            self.bus.write_byte_data(self.addr, 0x24, 0x01)
        except:
            print('Arm_Action_Study I2C error')

    # 动作组运行模式  0: 停止运行 1：单次运行 2： 循环运行
    # Action group operation mode 0: Stop operation 1: Single operation 2: Cycle operation
    def Arm_Action_Mode(self, mode):
        try:
            self.bus.write_byte_data(self.addr, 0x20, mode & 0xff)
        except:
            print('Arm_Clear_Action I2C error')

    # 读取已保存的动作组数量
    # Read the number of saved action groups
    def Arm_Read_Action_Num(self):
        try:
            self.bus.write_byte_data(self.addr, 0x22, 0x01)
            time.sleep(.001)
            num = self.bus.read_byte_data(self.addr, 0x22)
            return num
        except:
            print('Arm_Read_Action_Num I2C error')

    # 打开蜂鸣器，delay默认为0xff，蜂鸣器一直响。
    # delay=1~50，打开蜂鸣器后delay*100毫秒后自动关闭蜂鸣器，最大延时时间为5秒。
    # Turn on the buzzer, delay defaults to 0xff, and the buzzer keeps sounding.
    # delay=1~50, after turning on the buzzer, it will automatically turn off after delay*100 milliseconds. The maximum delay time is 5 seconds.
    def Arm_Buzzer_On(self, delay=0xff):
        if delay != 0:
            self.bus.write_byte_data(self.addr, 0x06, delay&0xff)

    # 关闭蜂鸣器
    # Turn off the buzzer
    def Arm_Buzzer_Off(self):
        self.bus.write_byte_data(self.addr, 0x06, 0x00)

