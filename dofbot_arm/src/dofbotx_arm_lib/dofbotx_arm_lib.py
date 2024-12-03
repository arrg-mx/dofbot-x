#!/usr/bin/env python8
# coding: utf-8
from typing import Optional

import smbus
import time
import math
import logging
from .exceptions import DataTransmissionError, DataProcessError


class ArmCtrl(object):
    """
    ArmCtrl class controls Yahboom 6-DOF robot arm with serial bus servos.
    Provides methods to control individual and grouped servo angles, set servo offsets, read servo angles, and manage other hardware functions.
    """

    def __init__(self, logger: logging.Logger = None, on_debug_mode: bool = False) -> None:
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
        self.__on_debug_mode = on_debug_mode
        self.__logger = logger or logging.getLogger("ArmCtrl")
        self.__logger.setLevel(logging.DEBUG if on_debug_mode else logging.INFO)
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
        if on_debug_mode:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)
            self.__logger.debug("ArmCtrl initialized with debug mode: %s", self.__on_debug_mode)

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
            rads (float): Desired angle in radians.
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

    def __calc_servo_angle(self, servo_pos: int, is_wrist_servo: bool = False, in_radians: bool = True) -> float:

        if is_wrist_servo:
            position = (
                    self.__wrist_range_deg * (self.__wrist_servo_resolution[0] * servo_pos) /
                    self.__wrist_resolution
            )
        else:
            position = (
                    self.__arm_range_deg * (self.__arm_servos_resolution[0] * servo_pos) /
                    self.__arm_resolution
            )

        return position if not in_radians else math.radians(position)

    def serial_servo_write(
            self, servo_id: int, angle: float, duration: int, in_radians: bool = True
    ) -> list[int | float | bool]:
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
            return self.serial_servo_write_all_array(
                joints=[angle] * 6,
                duration=duration,
                in_radians=in_radians
            )
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
        try:
            self.__bus.write_i2c_block_data(self.__address, 0x10 + servo_id, [pos_h, pos_l, dur_h, dur_l])
            return [servo_id, angle, duration, in_radians, (0x10 + servo_id), pos, pos_h, pos_l, dur_h, dur_l]
        except Exception as e:
            raise DataTransmissionError(f"serial_servo_write I2C error: {str(e)}")
            # print('Arm_serial_servo_write I2C error')


    def serial_servo_write_any(
            self, servo_id: int, angle: float, duration: int, in_radians: bool = True
    ) -> list[int | float | bool]:
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

        retval = [servo_id, angle, duration, in_radians, pos]
        if servo_id == 0:
            retval.append(0x17)
            retval.append(pos_h)
            retval.append(pos_l)
            retval.append(dur_h)
            retval.append(dur_l)
        else:
            retval.append(0x19)
            retval.append(servo_id & 0xFF)
            retval.append(pos_h)
            retval.append(pos_l)
            retval.append(dur_h)
            retval.append(dur_l)

        try:
            if servo_id != 0:
                self.__bus.write_i2c_block_data(self.__address, 0x19, [servo_id & 0xff, pos_h, pos_l, dur_h, dur_l])
            else:
                self.__bus.write_i2c_block_data(self.__address, 0x17, [pos_h, pos_l, dur_h, dur_l])
        except Exception as e:
            raise DataTransmissionError(f"serial_servo_write_any I2C error: {str(e)}")
        #    print('Arm_serial_servo_write_any I2C error')

        return retval

    def serial_servo_write_all_array(
            self, joints: list[float], duration: int, in_radians: bool = True
    ) -> list[list[float] | int | bool | list[int]]:
        """
        Sets angles for all six servos in an array format.

        Args:
            joints (list of int): List of six target angles for servos [s1, s2, s3, s4, s5, s6].
            duration (int): Duration of the movement.
            in_radians (bool): Indicates if joint list angles are in radiants
        """
        # Substitutes Arm_serial_servo_write6_array
        positions = []
        servo_pos = []
        for i, angle in enumerate(joints):
            if i == 4:
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
                    if i in (1, 2, 3)
                    else angle
                )
                pos = (
                    self.__calc_servo_pos_rads(angle)
                    if in_radians
                    else self.__calc_servo_pos_deg(angle)
                )
            positions.extend([(pos >> 8) & 0xFF, pos & 0xFF])
            servo_pos.append(pos)

        dur_h, dur_l = (duration >> 8) & 0xFF, duration & 0xFF

        try:
            self.__bus.write_i2c_block_data(self.__address, 0x1e, [dur_h, dur_l])
            self.__bus.write_i2c_block_data(self.__address, 0x1d, positions)
        except Exception as e:
            raise DataTransmissionError(f"serial_servo_write_all_array I2C error: {str(e)}")
        #     print('Arm_serial_servo_write6 I2C error')
        return [joints, duration, in_radians, 0x1e, dur_h, dur_l, 0x1d, servo_pos, positions]

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
    ) -> list[list[float] | int | bool | list[int]]:
        """
        Sets angles for each of the six servos individually.

        Args:
            s1, s2, s3, s4, s6 (float): Target angles (0-180).
            s5 (float): Target angle for servo 5 (0-270).
            duration (int): Duration of the movement.
            in_radians (bool): indicates if s1-s6 values are in radiants
        """
        return self.serial_servo_write_all_array(
            [s1, s2, s3, s4, s5, s6], duration, in_radians=in_radians
        )

    def serial_servo_read(self, servo_id: int) -> int:
        """
        Reads the current angle of a specified servo.

        Args:
            servo_id (int): Servo ID (1-6).

        Returns:
            int: The angle (0-180), or -999.0 if an error occurs.
        """
        if servo_id not in range(1, 6):
            print("id must be 1 - 6")
            return -1
        pos: int = 0

        try:
            self.__bus.write_byte_data(self.__address, servo_id + 0x30, 0x0)
            time.sleep(0.003)
            pos = self.__bus.read_word_data(self.__address, servo_id + 0x30)
        except Exception as e:
        #    print('Arm_serial_servo_read I2C error')
            raise DataTransmissionError(f"serial_servo_read I2C error: {str(e)}")

        #        pos = (pos >> 8 & 0xFF) | (pos << 8 & 0xFF00)
        #        if servo_id == 5:
        #            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
        #            if pos > 270 or pos < 0:
        #                return None
        #        else:
        #            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
        #            if pos > 180 or pos < 0:
        #                return None
        #        if servo_id in [2, 3, 4]:
        #            pos = 180 - pos

        return pos

    def get_serial_servo_angle(self, servo_id: int, in_radians=True) -> float:
        try:
            servo_pos = self.serial_servo_read(servo_id=servo_id)
        except DataTransmissionError as e:
            raise DataProcessError(f"get_serial_servo_angle: {str(e)}")

        servo_angle = self.__calc_servo_angle(
            servo_pos=servo_pos,
            is_wrist_servo=(servo_id == 5),
            in_radians=in_radians
        )
        servo_angle = (
            (
                (self.__arm_range_rads - servo_angle)
                if in_radians
                else (self.__arm_range_deg - servo_angle)
            )
            if servo_id in (2, 3, 4)
            else servo_angle
        )

        return servo_angle

    def get_arm_serial_servos_angles(self, in_radians=True) -> list[float]:
        servo_angles = []
        try:
            for servo_id in range(1, 6):
                servo_angles.append(self.get_serial_servo_angle(servo_id=servo_id, in_radians=in_radians))
        except Exception  as e:
            raise DataProcessError(f"get_arm_serial_servos_angles: {str(e)}")

        return servo_angles

    def get_any_servo_pos(self, servo_id) -> int | None:
        # replace Arm_serial_servo_read_any
        servo_pos = -1
        if servo_id < 1 or servo_id > 250:
            return None

        try:
            self.__bus.write_byte_data(self.__address, 0x37, id)
            time.sleep(0.003)
            servo_pos = self.__bus.read_word_data(self.__address, 0x37)
        except Exception as e:
            raise DataProcessError(f"get_any_servo_pos: {str(e)}")

        return servo_pos

    def servo_write_offset_switch(self, servo_id: int) -> None:
        """
        Set the bus servo neutral offset with one click, power on and move to the neutral position,
        and then send the following function.

        Args:
            servo_id: 1-6 (setting), 0 (restore to initial)
        """
        try:
            if servo_id in range(1, 6):
                self.__bus.write_byte_data(self.__address, 0x1c, servo_id)
            elif id == 0:
                self.__bus.write_byte_data(self.__address, 0x1c, 0x00)
                time.sleep(.5)
            else:
                print(f"Servo ID: {servo_id}, nothing to do")
        except Exception as e:
            raise DataTransmissionError(f"servo_write_offset_switch: {str(e)}")

    def servo_write_offset_state(self) -> None:
        """
        Read the status of the one-click setting bus servo mid-bit offset.

        Notes:
            0 means that the corresponding servo ID cannot be found.
            1 means success.
            2 means failure is out of range.
        """
        try:
            self.__bus.write_byte_data(self.__address, 0x1b, 0x01)
            time.sleep(.001)
            state = self.__bus.read_byte_data(self.__address, 0x1b)
            return state
        except Exception as e:
            raise DataTransmissionError(f"servo_write_offset_state: {str(e)}")

    def ping_servo(self, servo_id: int) -> Optional[int]:
        """
        Read the servo status

        Args:
            servo_id:

        Returns:
            int
        Notes:
            0xda - normal
            0x00 - if no data can be read
            0x?? - other values are servo errors.
        """
        if servo_id <= 0 or servo_id > 250:
            return None
        else:
            try:
                reg = 0x38
                self.__bus.write_byte_data(self.__address, reg, servo_id)
                time.sleep(.003)
                value = self.__bus.read_byte_data(self.__address, reg)
                times = 0
                while value == 0 and times < 5:
                    self.__bus.write_byte_data(self.__address, reg, servo_id)
                    time.sleep(.003)
                    value = self.__bus.read_byte_data(self.__address, reg)
                    times += 1
                    if times >= 5:
                        return None
                return value
            except Exception as e:
                raise DataTransmissionError(f"ping_servo: {str(e)}")

    def get_hardware_version(self) -> str:
        """
        Read hardware version number
        Returns:
            Hardware version
        """
        try:
            self.__bus.write_byte_data(self.__address, 0x01, 0x01)
            time.sleep(.001)
            value = self.__bus.read_byte_data(self.__address, 0x01)
        except Exception as e:
            raise DataTransmissionError(f"get_hardware_version: {str(e)}")

        version = str(0) + '.' + str(value)
        return version

    def serial_set_torque(self, onoff: bool):
        """
        Torque switch 1: Open torque 0: Close torque (can be turned)

        Args:
            onoff: int

        Returns:

        """
        try:
            if onoff:
                self.__bus.write_byte_data(self.__address, 0x1A, 0x01)
            else:
                self.__bus.write_byte_data(self.__address, 0x1A, 0x00)
        except Exception as e:
            raise DataTransmissionError(f"serial_set_torque: {str(e)}")

    def serial_set_id(self, servo_id: int) -> bool:
        """
        Set the bus servo number

        Args:
            servo_id:

        Returns:

        """
        if servo_id <= 0 or servo_id > 250:
            return False

        try:
            self.__bus.write_byte_data(self.__address, 0x18, servo_id & 0xff)
            return True
        except Exception as e:
            raise DataTransmissionError(f"serial_set_id: {str(e)}")

    def get_product_select(self, index) -> int | None:
        """
        Set the current product color to 1~6, and the RGB light will turn on corresponding color.
        Args:
            index (int):

        Returns:

        """
        if index <= 0 or index > 6:
            return None

        try:
            self.__bus.write_byte_data(self.__address, 0x04, index & 0xff)
            return index
        except Exception as e:
            raise DataTransmissionError(f"get_product_select: {str(e)}")

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        """
        Set RGB lights to specify colors
        Args:
            red:
            green:
            blue:

        Returns:

        """
        if (red not in range(255)) or (green not in range(255)) or (blue not in range(255)):
            return None

        try:
            self.__bus.write_i2c_block_data(self.__address, 0x02, [red & 0xff, green & 0xff, blue & 0xff])
        except Exception as e:
            raise DataTransmissionError(f"set_rgb: {str(e)}")

    def set_button_mode(self, mode: int) -> bool:
        """
        Set K1 button mode.

        Args:
            mode:

        Returns:

        Notes:
              0: default mode
              1: learning mode
        """
        if mode not in (0, 1):
            return False

        try:
            self.__bus.write_byte_data(self.__address, 0x03, mode & 0xff)
        except Exception as e:
            raise DataTransmissionError(f"set_button_mode: {str(e)}")

    def reset_arm(self) -> None:
        """
        Restart the driver board
        Returns:
            None
        """
        try:
            self.__bus.write_byte_data(self.__address, 0x05, 0x01)
        except Exception as e:
            raise DataTransmissionError(f"reset_arm: {str(e)}")

    def servo_pwm_write(self, servo_id: int, angle: float, in_radians: bool = True) -> None:
        """
        PWD servo control
        Args:
            servo_id:
            angle:
            in_radians:

        Returns:

        Notes:
            servo_id: 1 - 6
            0: controls all servos
            angle: 0-180
        """
        if servo_id not in range(1, 6):
            return None

        position = int(math.degrees(angle) if in_radians else angle)

        # Clamp position to fit in PWD servo parameters
        if position < 0: position = 0
        if position > 180: position = 180

        try:
            if id == 0:
                self.__bus.write_byte_data(self.__address, 0x57, position & 0xff)
            else:
                self.__bus.write_byte_data(self.__address, 0x50 + servo_id, position & 0xff)
        except Exception as e:
            raise DataTransmissionError(f"servo_pwm_write: {str(e)}")

    def arm_clear_action_group(self) -> None:
        """
        Clear action group

        Returns:
            None
        """
        try:
            self.__bus.write_byte_data(self.__address, 0x23, 0x01)
        except Exception as e:
            raise DataTransmissionError(f"arm_clear_action_group: {str(e)}")

    def arm_action_study(self) -> None:
        """
        In learning mode, record the current action once
        Returns:

        """
        try:
            self.__bus.write_byte_data(self.__address, 0x24, 0x01)
        except Exception as e:
            raise DataTransmissionError(f"arm_action_study: {str(e)}")

    def arm_action_mode(self, mode: int) -> bool:
        """
        Set action group operation mode
        Args:
            mode:

        Returns:

        Notes:
             0: Stop operation
             1: Single operation
             2: Cycle operation
        """
        if mode not in (0, 1, 2):
            return False

        try:
            self.__bus.write_byte_data(self.__address, 0x20, mode & 0xff)
            return True
        except Exception as e:
            raise DataTransmissionError(f"arm_action_mode: {str(e)}")

    def arm_read_action_num(self):
        try:
            self.__bus.write_byte_data(self.__address, 0x22, 0x01)
            time.sleep(.001)
            num = self.__bus.read_byte_data(self.__address, 0x22)
            return num
        except Exception as e:
            raise DataTransmissionError(f"arm_read_action_num: {str(e)}")

    def turn_buzzer_on(self, duration: int = 0xFF) -> None:
        """
        Turn on the buzzer

        Args:
            duration:

        Returns:

        Notes:
            Duration defaults to 0xff, and the buzzer keeps sounding.
            Duration 1~50, after turning on the buzzer, it will automatically turn off after
            delay*100 milliseconds.
            The maximum delay time is 5 seconds.
        """
        if duration >= 0:
            try:
                self.__bus.write_byte_data(self.__address, 0x06, duration & 0xff)
            except Exception as e:
                raise DataTransmissionError(f"turn_buzzer_on: {str(e)}")

    # Turn off the buzzer
    def turn_buzzer_off(self) -> None:
        self.turn_buzzer_on(duration=0x00)


def main():
    arm_ctrl = ArmCtrl()
    arm_ctrl.turn_buzzer_on(500)
    arm_ctrl.turn_buzzer_off()


if __name__ == "__main__":
    main()
