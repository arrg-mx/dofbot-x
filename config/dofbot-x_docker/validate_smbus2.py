#!/usr/bin/env python3
# Validate I2C communication using smbus2 with retries

from smbus2 import SMBus
import time

class ArmDevice:
    def __init__(self, addr=0x15):
        self.addr = addr
        self.bus = SMBus(1)

    def buzzer_on(self, delay=0xff, retries=3):
        """Turn on the buzzer with retry."""
        for attempt in range(retries):
            try:
                self.bus.write_byte_data(self.addr, 0x06, delay)
                print(f"Buzzer turned on for delay {delay}.")
                return
            except Exception as e:
                print(f"I2C error in buzzer_on attempt {attempt + 1}: {e}")
                time.sleep(0.5)
        print("Failed to turn on the buzzer after retries.")

    def buzzer_off(self, retries=3):
        """Turn off the buzzer with retry."""
        for attempt in range(retries):
            try:
                self.bus.write_byte_data(self.addr, 0x06, 0x00)
                print("Buzzer turned off.")
                return
            except Exception as e:
                print(f"I2C error in buzzer_off attempt {attempt + 1}: {e}")
                time.sleep(0.5)
        print("Failed to turn off the buzzer after retries.")

if __name__ == "__main__":
    arm = ArmDevice()
    time.sleep(0.1)

    # Test buzzer
    arm.buzzer_on(1)  # 100ms
    time.sleep(1)
    arm.buzzer_on(3)  # 300ms
    time.sleep(1)
    arm.buzzer_on()   # Continuous
    time.sleep(1)
    arm.buzzer_off()
