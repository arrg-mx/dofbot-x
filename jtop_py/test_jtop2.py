import json
from jtop import jtop

with jtop() as jetson:
    # Continuously read and print stats while jetson.ok() is True
    if jetson.ok():
        # Access and print various system statistics
        #print("CPU Usage:", jetson.cpu['usage'])
        #print("GPU Usage:", jetson.gpu['usage'])
        #print("Memory Usage:", jetson.memory['used'] / jetson.memory['total'] * 100)
        #print("Temperature (GPU):", jetson.temperature['GPU'])
        #print("Power (Total):", jetson.power['total'])
        # You can also access more detailed information
        print("Board Info:")
        board_info = json.dumps(jetson.board)
        print(board_info)
        print(f"Stats [{jetson.stats['time']}], UpTime: {jetson.stats['uptime']}")
        #stats_info = json.dumps(jetson.stats)
        #print(stats_info) # Provides a comprehensive dictionary of all stats
        print(jetson.stats)
        print("Disk:")
        print(jetson.disk)
        print("==========================")
        print(jetson.json(stats=False))
