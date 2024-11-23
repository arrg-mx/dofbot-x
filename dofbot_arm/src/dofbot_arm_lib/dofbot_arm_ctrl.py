#!/usr/bin/env python8
# coding: utf-8

import smbus
import time
import math
from types import Optional


class ArmCtrl(object):
    """
    ArmCtrl class controls Yahboom 6-DOF robot arm with serial bus servos.
    Provides methods to control individual and grouped servo angles, set servo offsets, read servo angles, and manage other hardware functions.
    """

    def __init__(self) -> None:
        """
        Initializes the Arm_Device with a default I2C address and bus.
        
        Designed Dofbot Arm values - static values.
            I2C co-proccessor address: '0x15'
            Arm servos resolution: (lower_limit=900, upper_limit=3100)
                Servos 2, 3, 4 (movement inverted)
                Servos 1, 6 (direct movement)
            Arm range Deg: [0 to 180]
            Arm resolution: 2200 (Arm servo upper limit - Arm servo lower limit)
            Wrist servo resolution: (min=380, max=3700)
            Wrist range Deg: [0 to 270]
            Wrist resolution: 3400 (upper limit - bottom limit)
        """
        self.__address = 0x15
        self.__bus = smbus.SMBus(1)
        self.__arm_servos_resolution = (900, 3100)
        self.__wrist_servo_resolution = (380, 3700)
        self.__arm_range_deg = 180
        self.__wrist_range_deg = 270
        self.__arm_range_rads = math.radians(self.__arm_range_deg)
        self.__wrist_range_rads = math.radians(self.__wrist_range_deg)
        self.__arm_resolution = (
            self.__arm_servos_resolution[1] - self.__arm_servos_resolution[0]
        )
        self.__wrist_resolution = (
            self.__wrist_servo_resolution[1] - self.__wrist_servo_resolution[0]
        )

    def __calc_servo_pos_deg(self, angle: float, is_wrist_servo: bool = False) -> int:
        """
        Calculate the servo position value for a given angle in degrees.

        Args:
            angle (float): Desired angle in degrees.
            is_wrist_servo (bool): Indicates if calculation's parameter need to be
            adjusted to wrist joint servo.

        Returns:
            int: Calculated servo position, clamped within servo range.

        Notes:
            - if is_wrist_servo is false then uses arm joints parameters
            - if is_wrist_servo is true then uses wrist joint parameters
            - Also, gripper servo uses arm joint parameters

        """
        position = 0
        if is_wrist_servo:
            position = (
                self.__wrist_resolution * angle / self.__wrist_range_deg
                + self.__wrist_servo_resolution[0]
            )
            position = int(
                min(
                    max(position, self.__wrist_servo_resolution[0]),
                    self.__wrist_servo_resolution[1],
                )
            )
        else:
            position = (
                self.__arm_resolution * angle / self.__arm_range_deg
                + self.__arm_servos_resolution[0]
            )
            position = int(
                min(
                    max(position, self.__arm_servos_resolution[0]),
                    self.__arm_servos_resolution[1],
                )
            )

        return position

    def __calc_servo_pos_rads(self, rads: float, is_wrist_servo: bool = False) -> int:
        """
        Calculate the servo position value for a given angle in radians.

        Args:
            angle (float): Desired angle in radians.
            is_wrist_servo (bool): Indicates if calculation's parameter need to be
            adjusted to wrist joint servo.

        Returns:
            int: Calculated servo position, clamped within servo range.

        Notes:
            - Group 0, arm joints and gripper
            - Group 1, wrist joint, uses wrist resolution parameters
        """
        position = 0
        if is_wrist_servo:
            position = (
                self.__wrist_resolution * rads / self.__wrist_range_rads
                + self.__wrist_servo_resolution[0]
            )
            position = int(
                min(
                    max(position, self.__wrist_servo_resolution[0]),
                    self.__wrist_servo_resolution[1],
                )
            )
        else:
            position = (
                self.__arm_resolution * rads / self.__arm_range_rads
                + self.__arm_servos_resolution[0]
            )
            position = int(
                min(
                    max(position, self.__arm_servos_resolution[0]),
                    self.__arm_servos_resolution[1],
                )
            )

        return position

    def serial_servo_write(
        self, servo_id: int, angle: float, duration: int, in_radians: bool = True
    ) -> None:
        """
        Sets the angle of a specific servo or all servos.

        Args:
            servo_id (int): Servo ID (1-6 for individual servos, 0 for all servos).
            angle (int): Target angle (0-180).
            duration (int): Duration of the movement.
            in_radians (bool): Indicates if angle value is in radians.

        Notes:
            - For servos with IDs 2, 3, and 4, the angle is inverted.
            - ID 5 has a unique range from 0 to 270 degrees.
        """
        pos_l = pos_h = dur_l = dur_h = pos = 0
        if servo_id == 0:
            pass
        elif servo_id == 5:
            pos = (
                self.__calc_servo_pos_rads(angle, is_wrist_servo=True)
                if in_radians
                else self.__calc_servo_pos_deg(angle, is_wrist_servo=True)
            )
        else:
            angle = (
                (
                    (self.__arm_range_rads - angle)
                    if in_radians
                    else (self.__arm_range_deg - angle)
                )
                if servo_id in (2, 3, 4)
                else angle
            )
            pos = (
                self.__calc_servo_pos_rads(angle)
                if in_radians
                else self.__calc_servo_pos_deg(angle)
            )

        pos_h, pos_l = (pos >> 8) & 0xFF, pos & 0xFF
        dur_h, dur_l = (duration >> 8) & 0xFF, duration & 0xFF
        print(
            f"[TO_SEND]({angle}, {pos}) -> address: {self.__address:02x}, id: {(0x10 + servo_id):02x}, data: [{pos_h:02x}, {pos_l:02x}, {dur_h:02x}, {dur_l:02x}]"
        )
        # try:
        #    self.bus.write_i2c_block_data(self.__address, 0x10 + servo_id, [pos_h, pos_l, dur_h, dur_l])
        # except:
        #    print('Arm_serial_servo_write I2C error')

    def serial_servo_write_any(
        self, servo_id: int, angle: float, duration: int, in_radians: bool = True
    ) -> None:
        """
        Sets the angle of a servo with a wider ID range (1-250), or applies the same angle to all servos when ID is 0.

        Args:
            servo_id (int): Servo ID (1-250 for individual servos, 0 for all servos).
            angle (int): Target angle (0-180).
            duration (int): Duration of the movement.
            in_radians (bool): Indicates if angle value is in radians.
        """
        pos = (
            self.__calc_servo_pos_rads(angle)
            if in_radians
            else self.__calc_servo_pos_deg(angle)
        )
        pos_h, pos_l = (pos >> 8) & 0xFF, pos & 0xFF
        dur_h, dur_l = (duration >> 8) & 0xFF, duration & 0xFF

        if servo_id != 0:
            # self.bus.write_i2c_block_data(self.addr, 0x19, [id & 0xff, value_H, value_L, time_H, time_L])
            print(
                f"[TO_SEND]({angle}, {pos}) -> address: {self.__address:02x}, 0x19, data: [{(servo_id & 0xFF):02x}, {pos_h:02x}, {pos_l:02x}, {dur_h:02x}, {dur_l:02x}]"
            )
        else:
            # self.bus.write_i2c_block_data(self.addr, 0x17, [value_H, value_L, time_H, time_L])
            print(
                f"[TO_SEND]({angle}, {pos}) -> address: {self.__address:02x}, 0x17, data: [{pos_h:02x}, {pos_l:02x}, {dur_h:02x}, {dur_l:02x}]"
            )
        # try:
        #    if servo_id != 0:
        #        self.bus.write_i2c_block_data(self.addr, 0x19, [id & 0xff, value_H, value_L, time_H, time_L])
        #    else:
        #        self.bus.write_i2c_block_data(self.addr, 0x17, [value_H, value_L, time_H, time_L])
        # except:
        #    print('Arm_serial_servo_write_any I2C error')

    def serial_servo_write_all_array(
        self, joints: list[float], duration: int, in_radians: bool = True
    ) -> None:
        """
        Sets angles for all six servos in an array format.

        Args:
            joints (list of int): List of six target angles for servos [s1, s2, s3, s4, s5, s6].
            duration (int): Duration of the movement.
            in_radians (bool): Indicates if joint list angles are in radiants
        """
        positions = []
        for i, angle in enumerate(joints):
            if i == 4:
                pos = (
                    self.__calc_servo_pos_rads(angle, is_wrist_servo=True)
                    if in_radians
                    else self.__calc_servo_pos_deg(angle, is_wrist_servo=True)
                )
            else:
                if i in [1, 2, 3]:
                    angle = 180 - angle
                pos = (
                    self.__calc_servo_pos_rads(angle)
                    if in_radians
                    else self.__calc_servo_pos_deg(angle)
                )
            positions.extend([(pos >> 8) & 0xFF, pos & 0xFF])

        dur_h, dur_l = (duration >> 8) & 0xFF, duration & 0xFF

        print(
            f"[TO_SEND] -> address: {self.__address:02x}, 0x1e, data: [{dur_h:02x}, {dur_l:02x}]"
            f"[TO_SEND] -> address: {self.__address:02x}, 0x1d, data: {positions}"
        )
        # try:
        #     self.bus.write_i2c_block_data(self.addr, 0x1e, [time_H, time_L])
        #     self.bus.write_i2c_block_data(self.addr, 0x1d, positions)
        # except:
        #     print('Arm_serial_servo_write6 I2C error')

    def serial_servo_write_all(
        self,
        s1: float,
        s2: float,
        s3: float,
        s4: float,
        s5: float,
        s6: float,
        duration: int,
        in_radians: bool = True,
    ) -> None:
        """
        Sets angles for each of the six servos individually.

        Args:
            s1, s2, s3, s4, s6 (float): Target angles (0-180).
            s5 (float): Target angle for servo 5 (0-270).
            duration (int): Duration of the movement.
            in_radians (bool): indicates if s1-s6 values are in radiants
        """
        self.serial_servo_write_all_array(
            [s1, s2, s3, s4, s5, s6], duration, in_radians=in_radians
        )

    def serial_servo_read(self, servo_id: int) -> Optional[int]:
        """
        Reads the current angle of a specified servo.

        Args:
            servo_id (int): Servo ID (1-6).

        Returns:
            int: The angle (0-180), or None if an error occurs.
        """
        if servo_id < 1 or servo_id > 6:
            print("id must be 1 - 6")
            return None

        # TODO: Rewrite this part.
        # try:
        #     self.bus.write_byte_data(self.addr, id + 0x30, 0x0)
        #     time.sleep(0.003)
        #     pos = self.bus.read_word_data(self.addr, id + 0x30)
        # except:
        #     print('Arm_serial_servo_read I2C error')
        #     return None
        pos = 0
        pos = (pos >> 8 & 0xFF) | (pos << 8 & 0xFF00)
        if servo_id == 5:
            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
            if pos > 270 or pos < 0:
                return None
        else:
            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
            if pos > 180 or pos < 0:
                return None
        if servo_id in [2, 3, 4]:
            pos = 180 - pos

        return pos
