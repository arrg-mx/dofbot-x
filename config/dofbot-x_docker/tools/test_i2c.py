import smbus2
import time

def main():
    # Use the appropriate I2C bus (e.g., 1 for /dev/i2c-1)
    bus = smbus2.SMBus(1)

    # Replace with your I2C device address and register
    DEVICE_ADDRESS = 0x15  # Example I2C address
    REGISTER = 0x06        # Example register address

    try:
        # Write a value to the device
        print("Writing to I2C device...")
        bus.write_byte_data(DEVICE_ADDRESS, REGISTER, 0x01)

        # Read a value from the device
        print("Reading from I2C device...")
        # value = bus.read_byte_data(DEVICE_ADDRESS, REGISTER)
        print(f"Read value: {value}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        bus.close()

if __name__ == "__main__":
    main()

