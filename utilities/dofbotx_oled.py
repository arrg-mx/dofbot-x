#!/usr/bin/env python3
# coding=utf-8

"""
oled.py

This script displays system information (CPU usage, RAM, disk space, IP address, and system time)
on an OLED screen using the Adafruit_SSD1306 library. System information is retrieved using
the `SysInfo` class from the `arrg_utils` package, which aggregates the necessary data
into a single snapshot.

Dependencies:
- arrg_utils package (specifically, the SysInfo class for system information)
- Adafruit_SSD1306 for OLED display control
- PIL (Python Imaging Library) for rendering text on the OLED screen

"""

import time
from arrg_utils.sysinfo import SysInfo
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont


# Initialize the OLED display
try:
    RST = None
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=1, gpio=1)
    disp.begin()
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    # font = ImageFont.load_default()
    # font = ImageFont.truetype('SauceCodeProNerdFontMono-Regular.ttf', 8)
    font = ImageFont.truetype('RobotoMonoNerdFontMono-Regular.ttf', 9)
    # font = ImageFont.truetype('TerminessNerdFontMono-Regular.ttf', 8)
    padding = -2
    top = padding
    bottom = height - padding
    x = 0
except Exception as e:
    print("Error initializing display:", e)


def display_system_info(snapshot: dict) -> None:
    """
    Displays system information on the OLED screen.

    Args:
        snapshot (dict): A dictionary containing system information from SysInfo.get_system_snapshot().
            Expected keys: 'cpu', 'time', 'ram', 'disk', 'ip'.
    """
    try:
        # Clear the image buffer
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Display CPU usage and system time
        draw.text((x, top), f"CPU: {snapshot['cpu']:.2f}%", font=font, fill=255)
        draw.text((x + 50, top), snapshot["time"], font=font, fill=255)

        # Display RAM and Disk usage
        ram_info = snapshot["ram"]
        draw.text(
            (x, top + 8),
            f"RAM: {ram_info['available']:.2f}/{ram_info['total']:.2f}GB",
            font=font,
            fill=255,
        )

        disk_info = snapshot["disk"]
        draw.text(
            (x, top + 16),
            f"Disk: {disk_info['available']:.2f}/{disk_info['total']:.2f}GB",
            font=font,
            fill=255,
        )

        # Display IP address
        draw.text((x, top + 24), f"IP: {snapshot['ip']}", font=font, fill=255)

        # Update OLED display with the new image
        disp.image(image)
        disp.display()
    except Exception as e:
        print("Error displaying system information:", e)


def main():
    """
    Main loop to continuously retrieve and display system information on the OLED.
    Uses `SysInfo.get_system_snapshot()` to gather data, updating every 2 seconds.
    """
    sys_info = SysInfo()
    try:
        while True:
            snapshot = sys_info.get_system_snapshot()
            display_system_info(snapshot)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program closed by user.")
    except Exception as e:
        print("Error in main loop:", e)


if __name__ == "__main__":
    main()
