#!/usr/bin/env python3

import time
from jtop import jtop
from jetson_stats import jetson_variables, jetson_release

def get_board_info():
    """
    Returns static board information: hardware model, JetPack / L4T version etc.
    """
    vars = jetson_variables()   # environment / variable info
    rel = jetson_release()      # release info
    info = {
        "BOARD": vars["BOARD"] if "BOARD" in vars else vars.get("JETSON_BOARD", None),
        "JETSON_MODEL": vars.get("JETSON_MODEL", None),
        "JETPACK": rel["JETPACK"] if "JETPACK" in rel else None,
        "L4T": rel["L4T"] if "L4T" in rel else None,
        "CUDA_VERSION": rel.get("CUDA", None),
        "CUDNN_VERSION": rel.get("CUDNN", None),
        "ROS_VERSION": vars.get("ROS_DISTRO", None),  # if ROS installed
    }
    return info

def print_stats_loop(interval=2.0, duration=10.0):
    """
    Periodically fetches dynamic stats and prints them.
    interval: seconds between readings
    duration: how long to run (in seconds)
    """
    end_time = time.time() + duration
    with jtop() as jetson:
        while jetson.ok() and time.time() < end_time:
            stats = jetson.stats  # dict of many telemetry values
            # You can extract what you want. Example:
            info_line = {
                "cpu_usage": stats.get("CPU", None),
                "gpu_usage": stats.get("GPU", None),
                "memory_used": stats.get("RAM", None),
                "memory_total": stats.get("RAM_TOTAL", None),
                "temperature_cpu": stats.get("Temp CPU", None),
                "temperature_gpu": stats.get("Temp GPU", None),
                "fan_speed": stats.get("fan", None),
                "uptime": stats.get("uptime", None),
                "power_current": stats.get("power cur", None),
                "power_avg": stats.get("power avg", None),
            }
            print(info_line)
            time.sleep(interval)

def main():
    print("==== Board Info ====")
    board_info = get_board_info()
    for k, v in board_info.items():
        print(f"{k}: {v}")
    print("\n==== Dynamic Stats ====")
    print_stats_loop(interval=2.0, duration=20.0)

if __name__ == "__main__":
    main()

